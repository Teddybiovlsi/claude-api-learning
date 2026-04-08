"""
005_text_editor_tool.py — Main entry point for the text editor tool demo.

Demonstrates how Claude can autonomously create, view, and modify files using
the built-in ``str_replace_based_edit_tool`` via a multi-turn conversation loop.

Usage:
    python 005_text_editor_tool.py
"""

from utils import (
    add_assistant_message,
    add_user_message,
    chat,
    get_text_edit_schema,
    model,
    run_tools,
    text_from_message,
)

def run_conversation(messages: list) -> list:
    """Drive a multi-turn conversation until the model stops requesting tool use.

    Each iteration:
      1. Sends the current message history to Claude with the text editor tool.
      2. Appends the assistant reply to the history.
      3. Prints any plain-text content from the reply.
      4. If the model requested tool calls, executes them and feeds the results
         back as a user message before looping again.
      5. Exits the loop when ``stop_reason`` is not ``"tool_use"``.

    Args:
        messages: The initial conversation history.  Modified in-place and
                  also returned for convenience.

    Returns:
        The updated ``messages`` list after the conversation concludes.
    """
    while True:
        response = chat(
            messages,
            tools=[get_text_edit_schema(model)],
        )

        add_assistant_message(messages, response)

        plain_text = text_from_message(response)
        if plain_text:
            print(plain_text)

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages


def main() -> None:
    """Bootstrap the conversation with an initial user prompt and run it."""
    messages = []

    # Replace the string below with the task you want Claude to perform.
    add_user_message(
        messages,
        "Please create a file called hello.txt with the content 'Hello, World!'",
    )

    run_conversation(messages)


if __name__ == "__main__":
    main()
