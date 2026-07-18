from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.state import AgentState

from app.nodes.planner import planner_node
from app.nodes.tool import tool_node
from app.nodes.chat import chat_node

from app.router import planner_router


builder = StateGraph(AgentState)

# ---------------------------------------------------------
# Nodes
# ---------------------------------------------------------

builder.add_node(
    "planner",
    planner_node,
)

builder.add_node(
    "tool",
    tool_node,
)

builder.add_node(
    "chat",
    chat_node,
)

# ---------------------------------------------------------
# Edges
# ---------------------------------------------------------

builder.add_edge(
    START,
    "planner",
)

builder.add_conditional_edges(
    "planner",
    planner_router,
)

builder.add_edge(
    "tool",
    "chat",
)

builder.add_edge(
    "chat",
    END,
)

graph = builder.compile()