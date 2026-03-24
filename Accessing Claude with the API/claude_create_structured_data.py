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

# Adding a user message that prompts the model to generate a very short event bridge rule in json format
add_user_message(messages, "Generate a very short event bridge rule as json")

# This technique is useful when you want to generate structured data like json, yaml, csv, etc. 
# By adding a stop sequence that indicates the end of the structured data, 
# you can ensure that the model generates only the desired output without any additional text.
add_assistant_message(messages, "```json")

# By adding the stop sequence "```", 
# we are telling the model to stop generating text once it encounters that sequence. 
# This way, we can ensure that the model generates only the JSON output without any additional text or explanations
text = chat_with_model(messages, stop_sequences=["```"])
print(text)