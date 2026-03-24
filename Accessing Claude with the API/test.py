from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"


def add_user_message(messages: list, content: str) -> None:
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages: list, content: str) -> None:
    messages.append({"role": "assistant", "content": content})


def chat_with_model(messages: list) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=messages
    )
    return response.content[0].text


def main():
    messages = []
    questions = [
        "What is quantum computing? Answer in one sentence",
        "Write another sentence that expands on the previous answer",
    ]

    for question in questions:
        add_user_message(messages, question)
        reply = chat_with_model(messages)
        print(reply)
        add_assistant_message(messages, reply)


if __name__ == "__main__":
    main()
