from app.tools.registry import tool_registry

from app.tools.search_tool import DuckDuckGoSearchTool

from app.tools.calculator_tool import CalculatorTool

from app.tools.filesystem_tool import FileSystemTool


class ToolLoader:
    """
    Loads and registers all tools.
    """

    @staticmethod
    def load_tools() -> None:

        tool_registry.register(DuckDuckGoSearchTool())
        tool_registry.register(CalculatorTool())
        tool_registry.register(FileSystemTool())