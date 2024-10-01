import litellm
import pytest
import tenacity
import tree

from ldp.agent import Agent, MemoryAgent, ReActAgent
from ldp.alg.optimizer import (
    MemoryOpt,
    Optimizer,
    default_optimizer_factory,
)
from ldp.alg.optimizer.ape import APEOpt, APEScoreFn, Example
from ldp.data_structures import Trajectory, Transition
from ldp.graph.common_ops import FxnOp, LLMCallOp, MemoryOp, PromptOp
from ldp.graph.gradient_estimators import (
    llm_straight_through_estimator as llm_ste,
)
from ldp.graph.gradient_estimators import (
    straight_through_estimator as ste,
)
from ldp.graph.memory import Memory
from ldp.graph.op_utils import CallID, compute_graph, eval_mode
from ldp.graph.ops import GradInType, Op, OpCtx, OpResult
from ldp.llms import LLMModel, append_to_sys


@pytest.mark.parametrize(
    ("agent_cls", "optimizer_cls", "optimizer_kwargs"),
    [
        (MemoryAgent, MemoryOpt, {}),
        (ReActAgent, APEOpt, {"score_fn": APEScoreFn.GRADIENT}),
    ],
)
def test_optimizer_factory(
    agent_cls: type[Agent], optimizer_cls: type[Optimizer], optimizer_kwargs: dict
):
    agent = agent_cls()
    opt = default_optimizer_factory(agent, optimizer_cls, **optimizer_kwargs)
    assert isinstance(opt, optimizer_cls)


class SquaredErrorLoss(Op[int]):
    async def forward(self, y: str, yhat: str) -> int:
        try:
            return (int(y) - int(yhat)) ** 2
        except ValueError:  # For example, yhat may be "I guess the number is 7."
            return 100

    @classmethod
    def backward(
        cls,
        ctx: OpCtx,
        input_args,
        input_kwargs,
        grad_output: tree.Structure,
        call_id: CallID,
    ) -> GradInType:
        try:
            y = int(input_kwargs["y"])
            yhat = int(input_kwargs["yhat"])
        except ValueError:
            loss = ctx.get(call_id, "output").value
            return [], {"y": loss, "yhat": loss}  # Straight-through approximation
        # d/dy of (y - y^)^2 = 2 (y - y^), and d/dy^ of (y - y^)^2 = -2 (y - y^)
        # return  dL/dy,  dL/dy^
        # Note that grad_output is ignored because this is assumed to be a terminal scalar,
        # much like calling loss.backward() in pytorch.
        return [], {
            "y": 2 * (y - yhat),
            "yhat": -2 * (y - yhat),
        }


@pytest.mark.asyncio
async def test_ape_optimizer() -> None:
    sys_prompt_op = PromptOp("Guess a number based on the input word.")
    package_msg_op = FxnOp(append_to_sys)
    llm = LLMModel()
    llm.config["max_retries"] = 3  # we seem to be hitting rate limits frequently
    llm_call_op = LLMCallOp()
    strip_op = FxnOp(lambda x: x.content)
    loss_op = SquaredErrorLoss()

    @compute_graph()
    async def forward(xi_: str, yi_: str) -> OpResult[int]:
        """Perform a forward pass through the model to the resultant SE loss."""
        s = await sys_prompt_op()
        m = await package_msg_op(xi_, s)
        c = await llm_call_op(llm.config, m)
        yh = await strip_op(c)
        return await loss_op(yi_, yh)

    # Sequentially run a forward pass for each (x, y)
    x = ["Hello", "Day", "Bar"]
    y = [str(len(xi)) for xi in x]  # Number to guess should be word's length
    opt = APEOpt(
        llm=llm,
        llm_call_op=llm_call_op,
        prompt_op=sys_prompt_op,
        good_examples=[
            Example(input=x, output=y, score=0) for x, y in zip(x, y, strict=True)
        ],
        score_fn=APEScoreFn.GRADIENT,
    )
    assert opt.trace == [sys_prompt_op.prompt]

    trajectory = Trajectory()
    for i, (xi, yi) in enumerate(zip(x, y, strict=True)):
        loss = await forward(xi, yi)
        if i == 0:
            assert loss.value > 0, (
                "First example's loss should be non-zero - otherwise, no learning"
                " signal."
            )
        # Sets grad_output and grad_input in context, to be used by optimizer
        loss.compute_grads(backward_fns={LLMCallOp: llm_ste, FxnOp: ste})

        # APE in gradient mode is only going to pay attention to the action, so set
        # placeholders for the other attributes
        trajectory.steps.append(
            Transition(
                timestep=0,
                agent_state=None,
                next_agent_state=None,
                observation=[],
                next_observation=Transition.NO_OBSERVATION,
                action=loss,
                reward=0,
                done=False,
            )
        )

    # Run full optimizer step
    for i in range(3):  # Retries
        opt.aggregate([trajectory])
        assert opt.good_examples == [
            Example(input=x, output=y, score=0) for x, y in zip(x, y, strict=True)
        ]

        await opt.update()
        assert not opt.examples, "Expected reset of examples after update."
        assert len(opt.trace) == i + 2, "Expected new prompt to be recorded."

        with eval_mode():
            if (await forward(xi, yi)).value == 0:  # pylint: disable=undefined-loop-variable
                return

    raise AssertionError("Failed to complete optimization after retries.")


def mem_opt_failed(exc: BaseException) -> bool:
    # Sometimes the memory opt fails to converge because the training examples
    # are not informative. Try again
    return isinstance(exc, AssertionError) and "should be less than" in str(exc)


@pytest.mark.flaky(reruns=3, only_on=[litellm.exceptions.APIConnectionError])
@pytest.mark.asyncio
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    retry=tenacity.retry_if_exception(mem_opt_failed),
)
async def test_memory_optimizer() -> None:
    x = ["Hello", "Day", "Bar"]
    y = [str(len(xi)) for xi in x]

    mem_op = MemoryOp()
    # seed with one memory to show example
    await mem_op.memory_model.add_memory(
        Memory(query="Great", output=str(len("Great")), value=1.0)
    )
    package_msg_op = FxnOp(
        lambda mems, xi: append_to_sys(
            "Previous attempts:\n"
            + "\n\n".join(str(m) for m in mems)
            + f"\n-----\n\n{xi}",
            "Guess a number based on the input word.",
        )
    )
    # this is flaky, so use a smarter model
    llm_config = {"model": "gpt-4-turbo", "temperature": 0.0, "max_retries": 3}
    llm_call_op = LLMCallOp()
    strip_op = FxnOp(lambda x: x.content)
    loss_op = SquaredErrorLoss()

    async def reward_fn(target: str, result: OpResult) -> float:
        # MemoryOp works with rewards, not gradients. So instead of
        # backproping through the loss, we compute a non-differentiable
        # reward.
        loss = (await loss_op(target, result)).value
        if loss == 0:
            # positive reward if it got it right
            return 1.0
        return -loss

    opt = MemoryOpt(memory_op=mem_op, output_op=llm_call_op)

    trajectory = Trajectory()
    for xi, yi in zip(x, y, strict=True):
        async with compute_graph():
            mems = await mem_op(xi)
            msg = await package_msg_op(mems, xi)
            c = await llm_call_op(llm_config, msg)
            yh = await strip_op(c)

            reward = await reward_fn(yi, yh)
        yh.compute_grads()

        # MemoryOpt is only going to look at action and reward, so set placeholders
        # for the other values
        trajectory.steps.append(
            Transition(
                timestep=0,
                agent_state=None,
                next_agent_state=None,
                observation=Transition.NO_OBSERVATION,
                next_observation=Transition.NO_OBSERVATION,
                action=yh,
                reward=reward,
                done=False,
            )
        )

    opt.aggregate([trajectory])
    await opt.update()

    assert (
        len(mem_op.memory_model.memories) == 4
    ), "Incorrect number of stored memories after optimization step."
    assert (
        not opt.example_buffer
    ), "MemoryOpt buffer should be empty after applying update"

    x_eval, y_eval = xi, yi  # pylint: disable=undefined-loop-variable
    async with compute_graph():
        with eval_mode():
            mems = await mem_op(x_eval)
            msg = await package_msg_op(mems, x_eval)
            print(msg)
            assert len(msg.value) > 1, "Message should have multiple memories."
            # check that Input appears a few times (from memories)
            assert msg.value[-1].content, "unexpected message content"
            assert (
                msg.value[-1].content.count("Input") > 2
            ), "Input should appear multiple times in the response."

            c = await llm_call_op(llm_config, msg)
            yh = await strip_op(c)
            loss = await loss_op(y_eval, yh)

    assert (
        loss.value < 100
    ), f"Loss ({loss.value:.3f}) should be less than 100 after training."
