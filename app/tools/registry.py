from app.enums import ToolName
from app.tools.base import BaseTool


class ToolRegistry:
    """
    Stores and manages all available tools.
    """

    def __init__(self):

        self._tools: dict[ToolName, BaseTool] = {}

    def register(
        self,
        tool: BaseTool
    ) -> None:
        """
        Register a tool.
        """

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name.value}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(
        self,
        tool_name: ToolName
    ) -> BaseTool:
        """
        Retrieve a registered tool.
        """

        if tool_name not in self._tools:
            raise KeyError(
                f"Tool '{tool_name.value}' is not registered."
            )

        return self._tools[tool_name]

    def exists(
        self,
        tool_name: ToolName
    ) -> bool:

        return tool_name in self._tools

    def list_tools(self) -> list[BaseTool]:

        return list(self._tools.values())

    def list_tool_names(self) -> list[ToolName]:

        return list(self._tools.keys())


tool_registry = ToolRegistry()