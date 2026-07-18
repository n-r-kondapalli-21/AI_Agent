from app.state import AgentState
from app.tool_manager import ToolManager


class PromptBuilder:
    """
    Builds all prompt variables required by the chat chain.
    """

    @staticmethod
    def build(
        state: AgentState,
    ) -> dict:

        prompt_data = {
            "messages": state.get("messages", []),
            "tool_context": "",
        }

        tool_result = state.get("tool_result")

        if tool_result is not None:

            if tool_result.success:

                formatted = ToolManager.format(
                    tool_result
                )

                prompt_data["tool_context"] = (
                    formatted or ""
                )

            else:

                prompt_data["tool_context"] = (
                    f"Tool execution failed for "
                    f"'{tool_result.tool_name.value}': "
                    f"{tool_result.error}"
                )

        return prompt_data