from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"


def add_user_message(messages: list, content: str) -> None:
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages: list, content: str) -> None:
    messages.append({"role": "assistant", "content": content})


def chat_with_model(messages: list, stop_sequences: list = None) -> str:
    if stop_sequences is None:
        stop_sequences = []

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=messages,
        stop_sequences=stop_sequences
    )
    return response.content[0].text

messages = []

prompt = """
Generate three different sample AWS CLI commands. Each should be very short
"""

# 1. user 問一次就夠了
add_user_message(messages, prompt)

add_assistant_message(messages, "Here are three commands in a single block without any comments or explanations:\n```bash")
text = chat_with_model(messages, stop_sequences=["```"])

print(text)