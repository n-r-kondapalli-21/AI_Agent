from abc import ABC, abstractmethod

from app.enums import ToolName
from app.schema import (
    ToolMetadata,
    ToolResult,
)


class BaseTool(ABC):
    """
    Base class for all tools.
    """

    def __init__(
        self,
        name: ToolName,
        metadata: ToolMetadata,
    ):

        self.name = name

        self.metadata = metadata

    @abstractmethod
    def run(
        self,
        **kwargs,
    ) -> ToolResult:
        """
        Execute the tool.
        """
        raise NotImplementedError

    @abstractmethod
    def format_for_prompt(
        self,
        result: ToolResult,
    ) -> str:
        """
        Convert tool output into prompt context.
        """
        raise NotImplementedError