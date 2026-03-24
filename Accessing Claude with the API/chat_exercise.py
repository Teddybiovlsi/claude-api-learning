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


# Initializing the messages list
messages = []

# Simulating a conversation with the model using the while loop and if user type "exit" then break the loop
while True:
    user_input = input("You: ")
    # If the user types "exit" then break the loop and end the conversation
    if user_input.lower() == "exit":
        print("Have a great day!")
        break

    # Adding the user's input to the messages list
    add_user_message(messages, user_input)

    # Pass the list of messages to the model and get the response
    response = chat_with_model(MODEL, messages)

    # print the response from the model
    print("Claude: " + response)

    # Adding the assistant's response to the messages list
    add_assistant_message(messages, response)