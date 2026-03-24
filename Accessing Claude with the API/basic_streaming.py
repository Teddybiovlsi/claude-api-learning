from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"


def add_user_message(messages: list, content: str) -> None:
    messages.append({"role": "user", "content": content})

# Initializing the messages list
messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

stream = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=messages,
    stream=True
)

for event in stream:
    print(event)