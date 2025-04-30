from app.core.processor import printer

from app.core.processor import messages_appender

from app.agents.bill_entry_getter import response as bill_responder

from app.core.processor import response_handler



#Messages to test, to be moved somewhere else for handling.




def main():

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
        ai_response = bill_responder(history)

        new_history_and_return_status= response_handler(ai_response,history)
        
        history = new_history_and_return_status[0]
        return_status = new_history_and_return_status[1]


        if return_status == False:
            printer("assistant",ai_response)
        else:
            iterations = 0
            while return_status == True and iterations < 3:
                ai_response = bill_responder(history)
                new_history_and_return_status = response_handler(ai_response,history)
                history = new_history_and_return_status[0]
                return_status = new_history_and_return_status[1]
                iterations += 1
                if return_status == False:
                    printer("assistant",ai_response)














if __name__ == "__main__":
    main()