from typing import Any

from pydantic import ValidationError

from app.enums import ToolName
from app.schema import PlannerDecision, ToolRequest
from app.utils.json_parser import JsonParser


TOOL_ALIASES: dict[str, ToolName] = {
    "search": ToolName.SEARCH,
    "calculator": ToolName.CALCULATOR,
    "filesystem": ToolName.FILESYSTEM,
    "file_system": ToolName.FILESYSTEM,
    "file-system": ToolName.FILESYSTEM,
    "files": ToolName.FILESYSTEM,
}


TOOL_PARAMETER_KEYS: dict[ToolName, set[str]] = {
    ToolName.SEARCH: {"query", "max_results"},
    ToolName.CALCULATOR: {"expression"},
    ToolName.FILESYSTEM: {
        "operation",
        "path",
        "destination",
        "content",
    },
}


def resolve_tool_name(name: str) -> ToolName | None:
    """
    Map planner tool names and aliases to a registered ToolName.
    """

    normalized = name.lower().strip().replace(" ", "_")
    return TOOL_ALIASES.get(normalized)


def normalize_tool_request(data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize tool request payloads before validation.
    """

    tool_request = data.get("tool_request")

    if not isinstance(tool_request, dict):
        return data

    tool_name = tool_request.get("tool_name")

    if isinstance(tool_name, str):
        resolved = resolve_tool_name(tool_name)
        if resolved is not None:
            tool_request["tool_name"] = resolved.value

    parameters = tool_request.get("parameters")

    if not isinstance(parameters, dict):
        tool_request["parameters"] = {}
        return data

    if "operation" in parameters and "path" in parameters:
        return data

    promoted = {
        key: value
        for key, value in tool_request.items()
        if key not in {"tool_name", "parameters"}
    }

    if promoted:
        tool_request["parameters"] = {
            **promoted,
            **parameters,
        }

    return data


def _build_tool_request(data: dict[str, Any]) -> ToolRequest:
    """
    Build a ToolRequest from flat planner JSON.
    """

    tool_name_value = data.get("tool")

    if not isinstance(tool_name_value, str):
        raise ValueError("Flat tool payload is missing a valid 'tool' field.")

    tool_name = resolve_tool_name(tool_name_value)

    if tool_name is None:
        raise ValueError(f"Unknown tool name: {tool_name_value}")

    allowed_keys = TOOL_PARAMETER_KEYS[tool_name]
    parameters = {
        key: value
        for key, value in data.items()
        if key in allowed_keys
    }

    if not parameters:
        raise ValueError(
            f"No parameters found for tool '{tool_name.value}'."
        )

    return ToolRequest(
        tool_name=tool_name,
        parameters=parameters,
    )


class PlannerParser:
    """
    Parse planner responses in multiple JSON formats.
    """

    @staticmethod
    def parse(text: str) -> PlannerDecision:
        """
        Convert an LLM planner response into a PlannerDecision.
        """

        data = JsonParser.to_dict(text)

        if "use_tool" in data:
            normalized = normalize_tool_request(data)
            return PlannerDecision.model_validate(normalized)

        if "tool" in data:
            return PlannerDecision(
                use_tool=True,
                tool_request=_build_tool_request(data),
                reasoning="Detected flat tool-call JSON from planner.",
            )

        raise ValueError(
            "Planner response did not match the expected decision format."
        )

    @staticmethod
    def parse_or_fallback(text: str) -> PlannerDecision:
        """
        Parse planner output, returning a safe fallback on failure.
        """

        try:
            return PlannerParser.parse(text)
        except (ValueError, ValidationError):
            return PlannerDecision(
                use_tool=False,
                tool_request=None,
                reasoning="Failed to parse planner decision, proceeding without tool.",
                final_answer=None,
            )
