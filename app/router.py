from app.state import AgentState

from app.enums import NodeName


def planner_router(state: AgentState) -> str:
    """
    Route execution based on the planner decision.
    """

    decision = state["planner_decision"]

    if decision.use_tool:
        return "tool"

    return NodeName.CHAT.value