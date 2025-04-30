


def print_message(role,assistant_output = None):
    if role == "assistant":
        text = assistant_output.output[0].content[0].text
        print("\n" + "=" * 80)
        print("Assistant:")
        print(text)
        print("=" * 80 + "\n")
    

    if role == "user":
        print("-" * 80)
    
    if role == "initiator":
        print("\n" + "=" * 80)
        print("AI Assistant (Type 'exit' to quit, 'savemessages' to save conversation)")
        print("=" * 80)