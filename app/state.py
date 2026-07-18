from typing_extensions import TypedDict, NotRequired

from langchain_core.messages import BaseMessage

from app.schema import PlannerDecision, ToolResult


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    messages: list[BaseMessage]

    planner_decision: NotRequired[PlannerDecision]

    tool_result: NotRequired[ToolResult]