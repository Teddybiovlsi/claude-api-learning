"""
utils.py — Shared helper utilities for the text editor tool demo.

Covers:
  - Message construction helpers (add_user_message, add_assistant_message)
  - Claude API wrapper (chat)
  - Response parsing (text_from_message)
  - TextEditorTool class (view, str_replace, create, insert, undo_edit)
  - Tool dispatch helpers (run_tool, run_tools)
  - Tool schema builder (get_text_edit_schema)
"""

import json
import os
import shutil
from typing import Optional, List

from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

# Load .env before creating the client so ANTHROPIC_API_KEY is available
load_dotenv()

# ---------------------------------------------------------------------------
# Client — shared across all helpers
# ---------------------------------------------------------------------------

client = Anthropic()
model = "claude-sonnet-4-5"


# ---------------------------------------------------------------------------
# Message construction helpers
# ---------------------------------------------------------------------------


def add_user_message(messages: list, message) -> None:
    """Append a user-role message to the conversation history.

    Args:
        messages: The running list of conversation turns.
        message: Either a raw string or an Anthropic ``Message`` object.
                 When a ``Message`` is passed its ``.content`` block is used.
    """
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages: list, message) -> None:
    """Append an assistant-role message to the conversation history.

    Args:
        messages: The running list of conversation turns.
        message: Either a raw string or an Anthropic ``Message`` object.
                 When a ``Message`` is passed its ``.content`` block is used.
    """
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


# ---------------------------------------------------------------------------
# Claude API wrapper
# ---------------------------------------------------------------------------


def chat(
    messages: list,
    system: Optional[str] = None,
    temperature: float = 1.0,
    stop_sequences: list = [],
    tools: Optional[list] = None,
) -> Message:
    """Send a conversation to the Claude API and return the response.

    Args:
        messages: Full conversation history in the Anthropic messages format.
        system: Optional system prompt string.
        temperature: Sampling temperature (0.0–1.0). Defaults to 1.0.
        stop_sequences: Optional list of strings that stop generation early.
        tools: Optional list of tool schemas made available to the model.

    Returns:
        An Anthropic ``Message`` object containing the model's response.
    """
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    return client.messages.create(**params)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def text_from_message(message: Message) -> str:
    """Extract and join all plain-text blocks from a model response.

    Args:
        message: An Anthropic ``Message`` object returned by the API.

    Returns:
        A single string with all text content blocks joined by newlines.
        Returns an empty string when the response contains no text blocks.
    """
    return "\n".join(
        block.text for block in message.content if block.type == "text"
    )


# ---------------------------------------------------------------------------
# TextEditorTool
# ---------------------------------------------------------------------------


class TextEditorTool:
    """Sandboxed file-system text editor exposed as an LLM tool.

    All file operations are restricted to ``base_dir``.  Before every
    destructive edit a timestamped backup is written to ``backup_dir`` so
    that ``undo_edit`` can restore the previous version.

    Args:
        base_dir: Root directory for all file operations.
                  Defaults to the current working directory.
        backup_dir: Directory where backups are stored.
                    Defaults to ``<base_dir>/.backups``.
    """

    def __init__(self, base_dir: str = "", backup_dir: str = "") -> None:
        self.base_dir = base_dir or os.getcwd()
        self.backup_dir = backup_dir or os.path.join(self.base_dir, ".backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_path(self, file_path: str) -> str:
        """Resolve *file_path* relative to ``base_dir`` and verify it stays inside.

        Args:
            file_path: Relative (or absolute) path supplied by the caller.

        Returns:
            The normalised absolute path.

        Raises:
            ValueError: If the resolved path escapes ``base_dir``.
        """
        abs_path = os.path.normpath(os.path.join(self.base_dir, file_path))
        if not abs_path.startswith(self.base_dir):
            raise ValueError(
                f"Access denied: Path '{file_path}' is outside the allowed directory"
            )
        return abs_path

    def _backup_file(self, file_path: str) -> str:
        """Create a timestamped backup copy of an existing file.

        Args:
            file_path: Absolute path of the file to back up.

        Returns:
            The absolute path of the backup file, or an empty string when the
            source file does not exist (nothing to back up).
        """
        if not os.path.exists(file_path):
            return ""
        file_name = os.path.basename(file_path)
        backup_path = os.path.join(
            self.backup_dir,
            f"{file_name}.{os.path.getmtime(file_path):.0f}",
        )
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _restore_backup(self, file_path: str) -> str:
        """Restore the most recent backup over *file_path*.

        Args:
            file_path: Absolute path of the file to restore.

        Returns:
            A success message string.

        Raises:
            FileNotFoundError: When no backups exist for the given file.
        """
        file_name = os.path.basename(file_path)
        backups = [
            f for f in os.listdir(self.backup_dir) if f.startswith(file_name + ".")
        ]
        if not backups:
            raise FileNotFoundError(f"No backups found for {file_path}")

        latest_backup = sorted(backups, reverse=True)[0]
        backup_path = os.path.join(self.backup_dir, latest_backup)
        shutil.copy2(backup_path, file_path)
        return f"Successfully restored {file_path} from backup"

    def _count_matches(self, content: str, old_str: str) -> int:
        """Return the number of non-overlapping occurrences of *old_str* in *content*.

        Args:
            content: The full file text to search.
            old_str: The substring to count.

        Returns:
            Integer occurrence count.
        """
        return content.count(old_str)

    # ------------------------------------------------------------------
    # Public commands
    # ------------------------------------------------------------------

    def view(self, file_path: str, view_range: Optional[List[int]] = None) -> str:
        """Return the contents of a file (or directory listing) with line numbers.

        Args:
            file_path: Path to the file or directory to view (relative to base_dir).
            view_range: Optional ``[start, end]`` 1-based line range.
                        Pass ``-1`` as *end* to read until the last line.

        Returns:
            A string where each line is prefixed with its 1-based line number.
            For directories, returns a newline-separated list of entries.

        Raises:
            FileNotFoundError: When the path does not exist.
            PermissionError: When the process lacks read permission.
            UnicodeDecodeError: When the file contains non-text (binary) content.
            ValueError: When the path escapes ``base_dir``.
        """
        try:
            abs_path = self._validate_path(file_path)

            if os.path.isdir(abs_path):
                try:
                    return "\n".join(os.listdir(abs_path))
                except PermissionError:
                    raise PermissionError(
                        "Permission denied. Cannot list directory contents."
                    )

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")

            if view_range:
                start, end = view_range
                if end == -1:
                    end = len(lines)
                lines = lines[start - 1 : end]
                result = [f"{i}: {line}" for i, line in enumerate(lines, start)]
            else:
                result = [f"{i}: {line}" for i, line in enumerate(lines, 1)]

            return "\n".join(result)

        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                "utf-8",
                b"",
                0,
                1,
                "File contains non-text content and cannot be displayed.",
            )
        except (ValueError, PermissionError, FileNotFoundError):
            raise
        except Exception as e:
            raise type(e)(str(e))

    def str_replace(self, file_path: str, old_str: str, new_str: str) -> str:
        """Replace exactly one occurrence of *old_str* with *new_str* in a file.

        A backup is created before the file is modified so the change can be
        undone with :meth:`undo_edit`.

        Args:
            file_path: Path to the target file (relative to base_dir).
            old_str: The exact text to find and replace.
            new_str: The replacement text.

        Returns:
            A success message string.

        Raises:
            FileNotFoundError: When the file does not exist.
            ValueError: When *old_str* is not found or matches more than once.
            PermissionError: When the process lacks write permission.
        """
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()

            match_count = self._count_matches(content, old_str)

            if match_count == 0:
                raise ValueError(
                    "No match found for replacement. Please check your text and try again."
                )
            elif match_count > 1:
                raise ValueError(
                    f"Found {match_count} matches for replacement text. "
                    "Please provide more context to make a unique match."
                )

            self._backup_file(abs_path)
            new_content = content.replace(old_str, new_str)

            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            return "Successfully replaced text at exactly one location."

        except (ValueError, PermissionError, FileNotFoundError):
            raise
        except Exception as e:
            raise type(e)(str(e))

    def create(self, file_path: str, file_text: str) -> str:
        """Create a new file at *file_path* with the given content.

        Intermediate parent directories are created automatically.

        Args:
            file_path: Destination path for the new file (relative to base_dir).
            file_text: The initial content to write into the file.

        Returns:
            A success message string.

        Raises:
            FileExistsError: When the file already exists.
            ValueError: When the path escapes ``base_dir``.
            PermissionError: When the process lacks write permission.
        """
        try:
            abs_path = self._validate_path(file_path)

            if os.path.exists(abs_path):
                raise FileExistsError(
                    "File already exists. Use str_replace to modify it."
                )

            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(file_text)

            return f"Successfully created {file_path}"

        except (ValueError, PermissionError, FileExistsError):
            raise
        except Exception as e:
            raise type(e)(str(e))

    def insert(self, file_path: str, insert_line: int, new_str: str) -> str:
        """Insert *new_str* after the given 1-based line number.

        Pass ``insert_line=0`` to insert before the first line.
        A backup is created before modification.

        Args:
            file_path: Path to the target file (relative to base_dir).
            insert_line: 1-based line number after which *new_str* is inserted.
                         Use ``0`` to prepend to the file.
            new_str: The text to insert (a trailing newline is added automatically).

        Returns:
            A success message string.

        Raises:
            FileNotFoundError: When the file does not exist.
            IndexError: When *insert_line* is out of range.
            ValueError: When the path escapes ``base_dir``.
            PermissionError: When the process lacks write permission.
        """
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            self._backup_file(abs_path)

            with open(abs_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Ensure new_str starts on its own line when the file has no trailing newline
            if lines and not lines[-1].endswith("\n"):
                new_str = "\n" + new_str

            if insert_line == 0:
                lines.insert(0, new_str + "\n")
            elif 0 < insert_line <= len(lines):
                lines.insert(insert_line, new_str + "\n")
            else:
                raise IndexError(
                    f"Line number {insert_line} is out of range. "
                    f"File has {len(lines)} lines."
                )

            with open(abs_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return f"Successfully inserted text after line {insert_line}"

        except (ValueError, PermissionError, FileNotFoundError, IndexError):
            raise
        except Exception as e:
            raise type(e)(str(e))

    def undo_edit(self, file_path: str) -> str:
        """Restore the most recently backed-up version of *file_path*.

        Args:
            file_path: Path of the file to restore (relative to base_dir).

        Returns:
            A success message string from :meth:`_restore_backup`.

        Raises:
            FileNotFoundError: When the file or its backup does not exist.
            ValueError: When the path escapes ``base_dir``.
            PermissionError: When the process lacks write permission.
        """
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            return self._restore_backup(abs_path)

        except (ValueError, FileNotFoundError, PermissionError):
            raise
        except Exception as e:
            raise type(e)(str(e))


# ---------------------------------------------------------------------------
# Tool dispatch helpers
# ---------------------------------------------------------------------------

# Module-level editor instance used by run_tool / run_tools
_text_editor = TextEditorTool()


def run_tool(tool_name: str, tool_input: dict) -> str:
    """Dispatch a single tool call to the appropriate handler.

    Currently only the ``str_replace_editor`` tool is supported.

    Args:
        tool_name: Name of the tool as declared in the schema (e.g.
                   ``"str_replace_editor"``).
        tool_input: Dictionary of arguments provided by the model.

    Returns:
        The string output produced by the tool.

    Raises:
        Exception: When *tool_name* or the ``command`` field is unrecognised.
    """
    if tool_name in ("str_replace_editor", "str_replace_based_edit_tool"):
        command = tool_input["command"]
        if command == "view":
            return _text_editor.view(
                tool_input["path"], tool_input.get("view_range")
            )
        elif command == "str_replace":
            return _text_editor.str_replace(
                tool_input["path"], tool_input["old_str"], tool_input["new_str"]
            )
        elif command == "create":
            return _text_editor.create(tool_input["path"], tool_input["file_text"])
        elif command == "insert":
            return _text_editor.insert(
                tool_input["path"],
                tool_input["insert_line"],
                tool_input["new_str"],
            )
        elif command == "undo_edit":
            return _text_editor.undo_edit(tool_input["path"])
        else:
            raise Exception(f"Unknown text editor command: {command}")
    else:
        raise Exception(f"Unknown tool name: {tool_name}")


def run_tools(message: Message) -> list:
    """Process every tool-use block in *message* and return result blocks.

    Errors are caught per-tool so that one failure does not prevent other
    tool calls in the same response from being executed.

    Args:
        message: The model ``Message`` that contains one or more
                 ``tool_use`` content blocks.

    Returns:
        A list of ``tool_result`` dicts ready to be sent back to the API as
        a user-role message content.
    """
    tool_requests = [block for block in message.content if block.type == "tool_use"]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False,
            }
        except Exception as e:
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True,
            }

        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks


# ---------------------------------------------------------------------------
# Tool schema builder
# ---------------------------------------------------------------------------


def get_text_edit_schema(model_name: str) -> dict:
    """Return the tool schema for the built-in text editor tool.

    The schema type is fixed to ``text_editor_20250728`` which corresponds to
    the ``str_replace_based_edit_tool`` capability.

    Args:
        model_name: The Claude model identifier (reserved for future use —
                    different models may need different schema types).

    Returns:
        A dict containing ``type`` and ``name`` keys accepted by the API.
    """
    return {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool",
    }
