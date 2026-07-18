from app.state import AgentState
from app.tool_manager import ToolManager


def tool_node(
    state: AgentState,
) -> AgentState:
    """
    Generic tool execution node.

    Executes whichever tool the planner selected.
    """

    decision = state.get("planner_decision")

    if (
        decision is None
        or decision.tool_request is None
    ):
        return state

    tool_result = ToolManager.execute(
        decision.tool_request
    )

    return {
        **state,
        "tool_result": tool_result,
    }