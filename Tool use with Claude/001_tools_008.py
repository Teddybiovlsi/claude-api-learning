from dotenv import load_dotenv
from anthropic import Anthropic

from helpers import (
    add_user_message,
    run_conversation,
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
    batch_tool_schema,
)

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

# ── Example: get current time in multiple formats ────────────────────────────

messages = []
add_user_message(
    messages,
    "What is the current time in HH:MM format? Also, what is the current time in SS format?",
)
run_conversation(client, model, messages, tools=[get_current_datetime_schema])
