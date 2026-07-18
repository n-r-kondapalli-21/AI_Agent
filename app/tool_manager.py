from app.schema import (
    ToolRequest,
    ToolResult,
)

from app.tools.registry import tool_registry


class ToolManager:
    """
    Central manager responsible for interacting
    with all registered tools.
    """

    @staticmethod
    def execute(
        request: ToolRequest
    ) -> ToolResult:
        """
        Execute a tool request.
        """

        tool = tool_registry.get(
            request.tool_name
        )

        return tool.run(
            **request.parameters
        )

    @staticmethod
    def format(
        tool_result: ToolResult
    ) -> str:
        """
        Convert a ToolResult into prompt context.
        """

        tool = tool_registry.get(
            tool_result.tool_name
        )

        return tool.format_for_prompt(
            tool_result
        )