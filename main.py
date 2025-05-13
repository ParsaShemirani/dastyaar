from app.core.conversation import Conversation
from app.core.printer import print_message
from app.core.ai_processor import process as process_ai
from app.agents.journaler import system_prompt


def main():
    conversation = Conversation(system_prompt)
    print_message("initiator")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        conversation.add_user_message(user_input)
        process_ai(conversation)

if __name__ == "__main__":
    main()