from dotenv import load_dotenv
from anthropic import Anthropic

from helpers import (
    get_current_datetime,
    get_current_datetime_schema
)

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

messages = []
messages.append({
    "role": "user",
    "content": "What is the exact time, formatted as HH:MM:SS?"
})

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)

messages.append({
    "role": "assistant",
    "content": response.content
})

# print(get_current_datetime(**response.content[0].input))

messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[0].id,
        "content": get_current_datetime(**response.content[0].input),
        "is_error": False
    }]
})

response_datetime = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)

print(response_datetime)
