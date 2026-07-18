import json

from app.enums import ToolName
from app.schema import FileSystemResult, ToolResult
from app.tool_manager import ToolManager


def is_raw_tool_json(content: str) -> bool:
    """
    Detect assistant replies that look like raw tool-call JSON.
    """

    text = content.strip()

    if not text.startswith("{"):
        return False

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False

    if not isinstance(data, dict):
        return False

    return (
        "tool" in data
        or (
            "tool_name" in data
            and "parameters" in data
        )
        or (
            "operation" in data
            and "path" in data
        )
    )


def format_user_response(
    content: str,
    tool_result: ToolResult | None,
) -> str:
    """
    Replace raw tool JSON with a natural-language confirmation.
    """

    if not is_raw_tool_json(content):
        return content

    if tool_result is None:
        return (
            "I prepared the requested operation, but the response was returned "
            "in an internal tool format. Please try the request again."
        )

    if not tool_result.success:
        return (
            f"I tried to run the requested tool, but it failed: "
            f"{tool_result.error}"
        )

    if tool_result.tool_name == ToolName.FILESYSTEM:
        return _format_filesystem_response(tool_result)

    formatted = ToolManager.format(tool_result)
    return formatted or "The requested tool operation completed successfully."


def _format_filesystem_response(
    tool_result: ToolResult,
) -> str:

    if tool_result.content is None:
        return "The file operation completed successfully."

    fs_result: FileSystemResult = tool_result.content
    operation = fs_result.operation

    if operation in {"write", "create", "append", "update"}:
        return (
            f"Done. {fs_result.message}. "
            f"The file is saved at `{fs_result.path}`."
        )

    if operation == "read":
        preview = fs_result.content or ""
        if len(preview) > 500:
            preview = preview[:500] + "\n... (truncated)"

        return (
            f"Here is the content of `{fs_result.path}`:\n\n"
            f"```\n{preview}\n```"
        )

    if operation == "list" and fs_result.details:
        entries = fs_result.details.get("entries", [])
        listing = "\n".join(f"- {entry}" for entry in entries)
        return (
            f"Contents of `{fs_result.path}`:\n\n"
            f"{listing}"
        )

    if operation == "exists" and fs_result.details:
        exists = fs_result.details.get("exists", False)
        entry_type = fs_result.details.get("type")

        if exists and entry_type:
            return f"Yes, `{fs_result.path}` exists and is a {entry_type}."
        if exists:
            return f"Yes, `{fs_result.path}` exists."
        return f"No, `{fs_result.path}` does not exist."

    if operation == "info" and fs_result.details:
        details = fs_result.details
        return (
            f"File information for `{fs_result.path}`:\n"
            f"- Type: {details.get('type')}\n"
            f"- Size: {details.get('size_bytes')} bytes\n"
            f"- Modified: {details.get('modified')}"
        )

    return fs_result.message
