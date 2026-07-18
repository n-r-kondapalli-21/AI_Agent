from enum import Enum


class ToolName(str, Enum):

    SEARCH = "search"
    CALCULATOR = "calculator"

    PYTHON = "python"

    FILESYSTEM = "filesystem"

    PDF_READER = "pdf_reader"

    BROWSER = "browser"

    WIKIPEDIA = "wikipedia"


class NodeName(str, Enum):
    """
    Graph node names.
    """

    PLANNER = "planner"
    CHAT = "chat"
    SEARCH = "search"