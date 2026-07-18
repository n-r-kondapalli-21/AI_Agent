from app.chains.planner import invoke_planner

from app.state import AgentState


def planner_node(
    state: AgentState,
) -> AgentState:
    """
    Planner node.

    Decides whether a tool should be used.
    """

    decision = invoke_planner(
        state["messages"]
    )
    return {
        **state,
        "planner_decision": decision,
    }