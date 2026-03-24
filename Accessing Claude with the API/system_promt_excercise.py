from system_promt import add_user_message, add_assistant_message, chat_with_model

def main():
    messages = []
    system_prompt = """
    You are the assistant to help me know the python programming language.
    First, you will ask me what I want to learn about python, then you will provide me with a concise answer and a code example.
    After that, you will ask me if I want to learn more about python,
    if I say yes, you will ask me what I want to learn about python, then you will provide me with additional information and examples.
    If I say no, you will end the conversation by saying "Have a great day!".
    """
    add_user_message(messages, "Write a python function that checks if a string is a duplicate of another string.")
    reply = chat_with_model(messages, system_prompt)
    print(reply)
    add_assistant_message(messages, reply)

if __name__ == "__main__":
    main()