from app.core.processor import printer

from app.core.processor import messages_appender
print("✅ JAMES IMPORTED")  
from app.agents.bill_entry_getter import response as bill_responder

from app.core.processor import response_handler



#Messages to test, to be moved somewhere else for handling.




def main():
    print("Tonyjames")

    history = [
        {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": "You are a helpful assistant. Use get_entries(...) to fetch notes from the database."
                }
            ]
        }
    ]


    while True:
        printer("initiator",None)

        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        history = messages_appender(None,"user_message",history,user_input,None)

        #Call AI assistant
        main_response = bill_responder(history)

        processed = response_handler(main_response,history)
        
        history = processed[0]
        to_continue = processed[1]

        if to_continue == False:
            printer("assistant",processed[0])

        else:
            iterations = 0
            while to_continue == True and iterations < 3:
                follow_up_response = bill_responder(history)
                processed = response_handler(follow_up_response,history)
                history = processed[0]
                to_continue = processed[1]
                iterations += 1
                print("Iterations:")
                print(iterations)














if __name__ == "__main__":
    main()