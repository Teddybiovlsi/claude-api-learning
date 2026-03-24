from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"

def add_user_message(messages: list, content: str) -> None:
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages: list, content: str) -> None:
    messages.append({"role": "assistant", "content": content})


def chat_with_model(messages: list, system_prompt: str = None) -> str:
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages
    }

    if system_prompt:
        params["system"] = system_prompt

    response = client.messages.create(**params)

    return response.content[0].text

if __name__ == "__main__":
    messages = []
    system_prompt = "You are a helpful assistant that provides concise answers to user questions."
    add_user_message(messages, "What is the capital of France?")
    reply = chat_with_model(messages, system_prompt)
    print(reply)