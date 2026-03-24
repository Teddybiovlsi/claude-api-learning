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

# 2. 第一次 call
add_assistant_message(messages, "aws")
text1 = chat_with_model(messages, stop_sequences=["aws"])

# 3. 把結果存回去，繼續 prefill 下一個
add_assistant_message(messages, "aws" + text1 + "\naws")
text2 = chat_with_model(messages, stop_sequences=["aws"])

# 4. 把結果存回去，繼續 prefill 下一個
add_assistant_message(messages, "aws" + text2 + "\naws")
text3 = chat_with_model(messages, stop_sequences=["aws"])

# 5. 最後把三個結果印出來
commands = [
    "aws" + text1.strip(),
    "aws" + text2.strip(),
    "aws" + text3.strip(),
]

for i, cmd in enumerate(commands, 1):
    print(f"Command {i}: {cmd}")