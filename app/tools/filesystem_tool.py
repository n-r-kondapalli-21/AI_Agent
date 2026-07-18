import shutil
from datetime import datetime
from pathlib import Path

from app.enums import ToolName
from app.schema import (
    FileSystemResult,
    ToolMetadata,
    ToolResult,
)
from app.tools.base import BaseTool


class FileSystemTool(BaseTool):
    """
    Read, write, create, update, rename, copy, move, delete,
    and list files and folders on the local filesystem.
    """

    def __init__(self):

        super().__init__(

            name=ToolName.FILESYSTEM,

            metadata=ToolMetadata(

                description=(
                    "Read, write, create, update, rename, copy, move, delete, "
                    "and list files and folders on the local filesystem."
                ),

                usage=[
                    "The user wants to create a file.",
                    "The user wants to read a file.",
                    "The user wants to modify a file.",
                    "The user wants to append text to a file.",
                    "The user wants to delete a file or folder.",
                    "The user wants to rename, copy, or move a file.",
                    "The user wants to create or remove directories.",
                    "The user wants to list the contents of a directory.",
                    "The user asks about file existence or file information.",
                ],

                parameters={
                    "operation": (
                        "create | read | write | append | update | delete | "
                        "rename | copy | move | mkdir | rmdir | list | exists | info"
                    ),
                    "path": "Target file or directory path",
                    "destination": "Destination path (copy/move/rename only)",
                    "content": "Text content (write/append/update only)",
                },

                examples=[
                    "Create a file named notes.txt.",
                    "Read config.py.",
                    "Append 'Hello World' to log.txt.",
                    "Rename report.docx to report_old.docx.",
                    "Copy data.csv to backup/data.csv.",
                    "Delete temp.txt.",
                    "Create a folder named projects.",
                    "List files in D:/My_Ai_Agent.",
                    "Check if requirements.txt exists.",
                ],
            ),
        )

    def run(
        self,
        operation: str,
        path: str,
        destination: str | None = None,
        content: str | None = None,
    ) -> ToolResult:

        try:

            resolved_path = Path(path).expanduser().resolve()
            resolved_destination = (
                Path(destination).expanduser().resolve()
                if destination
                else None
            )

            result = self._execute(
                operation=operation.lower().strip(),
                path=resolved_path,
                destination=resolved_destination,
                content=content,
            )

            return ToolResult(
                success=True,
                tool_name=self.name,
                content=result,
            )

        except Exception as e:

            return ToolResult(
                success=False,
                tool_name=self.name,
                content=None,
                error=str(e),
            )

    def _execute(
        self,
        operation: str,
        path: Path,
        destination: Path | None,
        content: str | None,
    ) -> FileSystemResult:

        if operation == "create":
            return self._create(path, content)

        if operation == "read":
            return self._read(path)

        if operation == "write":
            return self._write(path, content or "")

        if operation == "append":
            return self._append(path, content or "")

        if operation == "update":
            return self._write(path, content or "")

        if operation == "delete":
            return self._delete(path)

        if operation == "rename":
            return self._rename(path, destination)

        if operation == "copy":
            return self._copy(path, destination)

        if operation == "move":
            return self._move(path, destination)

        if operation == "mkdir":
            return self._mkdir(path)

        if operation == "rmdir":
            return self._rmdir(path)

        if operation == "list":
            return self._list(path)

        if operation == "exists":
            return self._exists(path)

        if operation == "info":
            return self._info(path)

        raise ValueError(
            f"Unsupported operation '{operation}'. "
            "Use create, read, write, append, update, delete, rename, "
            "copy, move, mkdir, rmdir, list, exists, or info."
        )

    def _create(
        self,
        path: Path,
        content: str | None,
    ) -> FileSystemResult:

        if path.exists():
            raise FileExistsError(f"File already exists: {path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content or "", encoding="utf-8")

        return FileSystemResult(
            operation="create",
            path=str(path),
            message=f"Created file: {path}",
        )

    def _read(self, path: Path) -> FileSystemResult:

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        file_content = path.read_text(encoding="utf-8")

        return FileSystemResult(
            operation="read",
            path=str(path),
            content=file_content,
            message=f"Read file: {path}",
        )

    def _write(
        self,
        path: Path,
        content: str,
    ) -> FileSystemResult:

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return FileSystemResult(
            operation="write",
            path=str(path),
            message=f"Wrote to file: {path}",
        )

    def _append(
        self,
        path: Path,
        content: str,
    ) -> FileSystemResult:

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("a", encoding="utf-8") as file:
            file.write(content)

        return FileSystemResult(
            operation="append",
            path=str(path),
            message=f"Appended to file: {path}",
        )

    def _delete(self, path: Path) -> FileSystemResult:

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        if path.is_dir():
            shutil.rmtree(path)
            message = f"Deleted directory: {path}"
        else:
            path.unlink()
            message = f"Deleted file: {path}"

        return FileSystemResult(
            operation="delete",
            path=str(path),
            message=message,
        )

    def _rename(
        self,
        path: Path,
        destination: Path | None,
    ) -> FileSystemResult:

        if destination is None:
            raise ValueError("destination is required for rename.")

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        path.rename(destination)

        return FileSystemResult(
            operation="rename",
            path=str(path),
            destination=str(destination),
            message=f"Renamed {path} to {destination}",
        )

    def _copy(
        self,
        path: Path,
        destination: Path | None,
    ) -> FileSystemResult:

        if destination is None:
            raise ValueError("destination is required for copy.")

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        destination.parent.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            shutil.copytree(path, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(path, destination)

        return FileSystemResult(
            operation="copy",
            path=str(path),
            destination=str(destination),
            message=f"Copied {path} to {destination}",
        )

    def _move(
        self,
        path: Path,
        destination: Path | None,
    ) -> FileSystemResult:

        if destination is None:
            raise ValueError("destination is required for move.")

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(destination))

        return FileSystemResult(
            operation="move",
            path=str(path),
            destination=str(destination),
            message=f"Moved {path} to {destination}",
        )

    def _mkdir(self, path: Path) -> FileSystemResult:

        path.mkdir(parents=True, exist_ok=True)

        return FileSystemResult(
            operation="mkdir",
            path=str(path),
            message=f"Created directory: {path}",
        )

    def _rmdir(self, path: Path) -> FileSystemResult:

        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        shutil.rmtree(path)

        return FileSystemResult(
            operation="rmdir",
            path=str(path),
            message=f"Removed directory: {path}",
        )

    def _list(self, path: Path) -> FileSystemResult:

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        entries = sorted(path.iterdir(), key=lambda item: item.name.lower())
        listing = []

        for entry in entries:
            entry_type = "directory" if entry.is_dir() else "file"
            listing.append(f"{entry.name} ({entry_type})")

        return FileSystemResult(
            operation="list",
            path=str(path),
            message=f"Listed {len(listing)} entries in {path}",
            details={"entries": listing},
        )

    def _exists(self, path: Path) -> FileSystemResult:

        exists = path.exists()
        entry_type = None

        if exists:
            entry_type = "directory" if path.is_dir() else "file"

        return FileSystemResult(
            operation="exists",
            path=str(path),
            message=f"Path {'exists' if exists else 'does not exist'}: {path}",
            details={
                "exists": exists,
                "type": entry_type,
            },
        )

    def _info(self, path: Path) -> FileSystemResult:

        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime).isoformat(sep=" ", timespec="seconds")

        details = {
            "name": path.name,
            "absolute_path": str(path),
            "type": "directory" if path.is_dir() else "file",
            "size_bytes": stat.st_size,
            "modified": modified,
        }

        return FileSystemResult(
            operation="info",
            path=str(path),
            message=f"Retrieved info for: {path}",
            details=details,
        )

    def format_for_prompt(
        self,
        result: ToolResult,
    ) -> str:

        if (
            not result.success
            or result.content is None
        ):
            return ""

        fs_result: FileSystemResult = result.content

        lines = [
            "File System Operation Result",
            "",
            f"Operation: {fs_result.operation}",
            f"Path: {fs_result.path}",
        ]

        if fs_result.destination:
            lines.append(f"Destination: {fs_result.destination}")

        lines.append(f"Message: {fs_result.message}")

        if fs_result.content is not None:
            lines.extend([
                "",
                "Content:",
                fs_result.content,
            ])

        if fs_result.details:
            lines.append("")
            lines.append("Details:")

            for key, value in fs_result.details.items():
                if isinstance(value, list):
                    lines.append(f"{key}:")
                    for item in value:
                        lines.append(f"  - {item}")
                else:
                    lines.append(f"{key}: {value}")

        return "\n".join(lines)
