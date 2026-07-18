import json
from typing import Any

from pydantic import ValidationError

from app.enums import ToolName
from app.schema import ToolRequest
from app.tool_manager import ToolManager
from app.utils.planner_parser import PlannerParser, resolve_tool_name


FILESYSTEM_PARAMETER_KEYS = {
    "operation",
    "path",
    "destination",
    "content",
}


def _build_request_from_data(data: dict[str, Any]) -> ToolRequest | None:
    """
    Build a ToolRequest from common tool-call JSON shapes.
    """

    if "use_tool" in data:
        decision = PlannerParser.parse(json.dumps(data))
        return decision.tool_request

    if "tool" in data:
        decision = PlannerParser.parse(json.dumps(data))
        return decision.tool_request

    if "tool_name" in data and "parameters" in data:
        return ToolRequest.model_validate(data)

    if "operation" in data and "path" in data:
        return ToolRequest(
            tool_name=ToolName.FILESYSTEM,
            parameters={
                key: value
                for key, value in data.items()
                if key in FILESYSTEM_PARAMETER_KEYS
            },
        )

    tool_request = data.get("tool_request")

    if isinstance(tool_request, dict):
        return ToolRequest.model_validate(
            normalize_nested_tool_request(tool_request)
        )

    return None


def normalize_nested_tool_request(
    tool_request: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize nested tool_request payloads.
    """

    normalized = dict(tool_request)
    tool_name = normalized.get("tool_name")

    if isinstance(tool_name, str):
        resolved = resolve_tool_name(tool_name)
        if resolved is not None:
            normalized["tool_name"] = resolved.value

    parameters = normalized.get("parameters")

    if not isinstance(parameters, dict):
        promoted = {
            key: value
            for key, value in normalized.items()
            if key not in {"tool_name", "parameters"}
        }
        normalized["parameters"] = promoted

    return normalized


def try_execute_tool_json(content: str):
    """
    Execute a tool directly from assistant tool-call JSON.
    """

    text = content.strip()

    if not text.startswith("{"):
        return None

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None

    try:
        request = _build_request_from_data(data)

        if request is None:
            return None

        return ToolManager.execute(request)

    except (ValueError, ValidationError, KeyError):
        return None
