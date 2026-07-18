from langchain_core.messages import AIMessage

from app.builders.prompt_builder import PromptBuilder

from app.chains.chat import get_chat_chain

from app.state import AgentState

from app.utils.response_formatter import format_user_response



def chat_node(
    state: AgentState
) -> AgentState:

    prompt_data = PromptBuilder.build(
        state
    )

    response = get_chat_chain().invoke(
        prompt_data
    )

    content = format_user_response(
        response.content,
        state.get("tool_result"),
    )

    return {
        **state,
        "messages": [
            *state["messages"],
            AIMessage(
                content=content
            )
        ]
    }