import json
import ast


def format_conversation_log(conversation_list):
    """
    Takes a conversation log list and returns a pretty-printed JSON string.
    
    Args:
        conversation_list (list): The conversation log as a list of dictionaries.
        
    Returns:
        str: A formatted JSON string representing the conversation.
    """
    return json.dumps(conversation_list, indent=2, ensure_ascii=False)

# Example usage:


conversation_log = [{'role': 'system', 'content': [{'type': 'input_text', 'text': 'Use the two functions, search_files_description as well as open_file to help the user.\nYou will need to import them first from their appropriate modules.\n\nYou will use the \'push_code\' function to interact with the python temrinal \n\nExample:\n\nUser: Please open the video of me dropping febreeze soap and water off the patio\n\nAssistant: I will go ahead and do that for you! Let me search for the video and then open it.\n\nFunction call ("push_code"): codestr: """from app.tools.mysql.filebase.functions import search_files_description\\nfrom app.tools.mac_commands.functions import open_file\\nresult = search_files_description(\'picture of my sister samira and I on top of the playground at central park\')\\nprint(result[0][\'description\'])"""\n\nFunction call output: \'This is me and my sister Samira at Central Park and we are both smiling as a picture is being taken of us together. We are on top of the play structure.\'\n\nFunction call ("push_code"): codestr: """open_file(result[0][\'name\'])"""\n\nFunction call output: \'\'\n\nAssistant: I have opened the picture for you.\n\n'}]}, {'role': 'user', 'content': [{'type': 'input_text', 'text': 'Please open the image of my aunt sara at san rafael park'}]}, {'type': 'function_call', 'id': 'fc_68411b711c5481999922d950750e6e7b0d0b0e0136b256da', 'call_id': 'call_GdledE1tM4w6ahEdcLiZHwaH', 'name': 'push_code', 'arguments': '{"code_str":"from app.tools.mysql.filebase.functions import search_files_description\\nfrom app.tools.mac_commands.functions import open_file\\nresult = search_files_description(\'image of my aunt sara at san rafael park\')\\nprint(result[0][\'description\'])"}'}, {'type': 'function_call_output', 'call_id': 'call_GdledE1tM4w6ahEdcLiZHwaH', 'output': "'In this image, my Aunt Sarah is standing on the shore of the San Rafael Park.'"}, {'type': 'function_call', 'id': 'fc_68411b7401048199b3649fa76d3484e60d0b0e0136b256da', 'call_id': 'call_M6WuxZZiiMDsgoqMGIhEdiLZ', 'name': 'push_code', 'arguments': '{"code_str":"open_file(result[0][\'name\'])"}'}, {'type': 'function_call_output', 'call_id': 'call_M6WuxZZiiMDsgoqMGIhEdiLZ', 'output': "''"}, {'id': 'msg_68411b752550819986b22a2886ff229f0d0b0e0136b256da', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'I have opened the image of your Aunt Sara at San Rafael Park. Enjoy!'}]}, {'id': 'msg_68411b76c2e08199893111bf74c5ba7b0d0b0e0136b256da', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'If you need anything else, feel free to ask!'}]}, {'id': 'msg_68411b77a49081999fbe5773019eade60d0b0e0136b256da', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'If you need help with anything else, just let me know!'}]}, {'id': 'msg_68411b7874dc8199acb551371ec152a20d0b0e0136b256da', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'If you have any other requests or need assistance, feel free to ask!'}]}]
james = f"{conversation_log}"

import re

def estimate_token_count(prompt: str) -> int:
    """
    Estimates the number of tokens in a prompt by splitting on whitespace and punctuation.
    
    Args:
        prompt (str): The input text prompt.
    
    Returns:
        int: Estimated number of tokens.
    """
    # Split prompt by whitespace and punctuation (basic tokenizer)
    tokens = re.findall(r"\w+|[^\w\s]", prompt)
    return len(tokens)

# Example usage:

print(estimate_token_count(james))  # Roughly counts tokens


print(format_conversation_log(conversation_log))



[
  {
    "role": "system",
    "content": [
      {
        "type": "input_text",
        "text": "Use the two functions, search_files_description as well as open_file to help the user.\nYou will need to import them first from their appropriate modules.\n\nYou will use the 'push_code' function to interact with the python temrinal \n\nExample:\n\nUser: Please open the video of me dropping febreeze soap and water off the patio\n\nAssistant: I will go ahead and do that for you! Let me search for the video and then open it.\n\nFunction call (\"push_code\"): codestr: \"\"\"from app.tools.mysql.filebase.functions import search_files_description\\nfrom app.tools.mac_commands.functions import open_file\\nresult = search_files_description('picture of my sister samira and I on top of the playground at central park')\\nprint(result[0]['description'])\"\"\"\n\nFunction call output: 'This is me and my sister Samira at Central Park and we are both smiling as a picture is being taken of us together. We are on top of the play structure.'\n\nFunction call (\"push_code\"): codestr: \"\"\"open_file(result[0]['name'])\"\"\"\n\nFunction call output: ''\n\nAssistant: I have opened the picture for you.\n\n"
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "please open the video of the garbage disposal system i made my dad recorded me"
      }
    ]
  },
  {
    "id": "msg_6840b8a1f2b08199a77994a2837598d80535436df60d86ea",
    "role": "assistant",
    "content": [
      {
        "type": "output_text",
        "text": "I will search for the video of the garbage disposal system that your dad recorded. Please hold on a moment while I do that."
      }
    ]
  },
  {
    "type": "function_call",
    "id": "fc_6840b8a3d7f881998d5a4942068c63fc0535436df60d86ea",
    "call_id": "call_ZLWDlugPqF8CsNKaKTBVpsvA",
    "name": "push_code",
    "arguments": "{\"code_str\":\"from app.tools.mysql.filebase.functions import search_files_description\\nresult = search_files_description('video of the garbage disposal system my dad recorded')\\nresult\"}"
  },
  {
    "type": "function_call_output",
    "call_id": "call_ZLWDlugPqF8CsNKaKTBVpsvA",
    "output": "'[{\\'id\\': 103, \\'name\\': \\'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4\\', \\'ts\\': datetime.datetime(2012, 1, 8, 11, 24, 25), \\'ts_precision\\': \\'second\\', \\'extension\\': \\'mp4\\', \\'size\\': 13840809, \\'hash\\': b\\'}\\\\xb1\\\\xaeQ7f+\\\\xf7\\\\xe6$I\\\\xdah\\\\x80\\\\xeep\\\\x0bS\\\\xa7\\\\x02\\\\xc5w\\\\x98\\\\x90W\\\\xc64j\\\\xdc\\\\xa0{\\\\xbf\\', \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \"This is a video of me showing my experiment design for a garbage disposal using chairs. My dad is recording me and I show how my garbage disposal mechanism works. It\\'s in the living room of the house and I\\'m sitting on the couch while I tip the mechanism over for it to dump the garbage.\", \\'relevance\\': 27.969091415405273}, {\\'id\\': 94, \\'name\\': \\'analog_map_encyclopedia_three_search-v1-86a157cf6da042b06b7383e8ec2df3bc6bc0f2b7a727975a8f0fbf174b0c19f5.MP4\\', \\'ts\\': datetime.datetime(2025, 5, 19, 9, 33, 39), \\'ts_precision\\': None, \\'extension\\': \\'mp4\\', \\'size\\': 7315196196, \\'hash\\': b\"\\\\x86\\\\xa1W\\\\xcfm\\\\xa0B\\\\xb0ks\\\\x83\\\\xe8\\\\xec-\\\\xf3\\\\xbck\\\\xc0\\\\xf2\\\\xb7\\\\xa7\\'\\\\x97Z\\\\x8f\\\\x0f\\\\xbf\\\\x17K\\\\x0c\\\\x19\\\\xf5\", \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \"I\\'m talking about the three things which I had my interest in, being the watch face analog and the map and compass and the encyclopedia. I recorded this video after buying the encyclopedia the previous day and I\\'m talking about the benefits of it in comparison to the search query program which I\\'m writing which has its own benefits, but these three things are unique and I talk about that in the video.\", \\'relevance\\': 5.621547698974609}, {\\'id\\': 93, \\'name\\': \\'250519_1024-v1-27d315d66fd7be1539907fc45e9640531dee8831525ce6d9251187fe828f8230.mp3\\', \\'ts\\': datetime.datetime(2025, 5, 19, 10, 24, 30), \\'ts_precision\\': None, \\'extension\\': \\'mp3\\', \\'size\\': 13598010, \\'hash\\': b\"\\'\\\\xd3\\\\x15\\\\xd6o\\\\xd7\\\\xbe\\\\x159\\\\x90\\\\x7f\\\\xc4^\\\\x96@S\\\\x1d\\\\xee\\\\x881R\\\\\\\\\\\\xe6\\\\xd9%\\\\x11\\\\x87\\\\xfe\\\\x82\\\\x8f\\\\x820\", \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \"In this audio file I talk about the three things that I recently came on to, being the analog watch face and map and compass and encyclopedia, and it\\'s recorded by the Sony voice recorder for my ZV-E10 camera.\", \\'relevance\\': 3.8096132278442383}]'"
  },
  {
    "type": "function_call",
    "id": "fc_6840b8a684e48199a72dcc6d01b16d7f0535436df60d86ea",
    "call_id": "call_d1pycTLEXjHvCnRKd6nbafWQ",
    "name": "push_code",
    "arguments": "{\"code_str\":\"from app.tools.mac_commands.functions import open_file\\nopen_file('video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4')\"}"
  },
  {
    "type": "function_call_output",
    "call_id": "call_d1pycTLEXjHvCnRKd6nbafWQ",
    "output": "''"
  },
  {
    "id": "msg_6840b8a9ac5881999f7cca2f6c87dc480535436df60d86ea",
    "role": "assistant",
    "content": [
      {
        "type": "output_text",
        "text": "I have opened the video of the garbage disposal system that your dad recorded. Enjoy watching!"
      }
    ]
  }
]