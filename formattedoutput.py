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


conversation_log =  [{'role': 'system', 'content': [{'type': 'input_text', 'text': '\n\n# Assistant Instructions\n\nYour job is to accomplish the user\'s requests by using a Python interactive session.\n\n* Use the `push_code` function to interact with the session.\n* You will also have access to a list of functions that you can import and utilize.\n\nSend messages to the user with short updates on what you are doing, and answer any questions they ask.\n\n---\n\n# Functions\n\nBelow is the **exact list of functions** available for you to use, with detailed descriptions and usage instructions.\n\n**Important:**\n\n* Use the **exact function names** provided here.\n* Do **not** shorten, abbreviate, or guess alternative function names.\n* Always import functions from their specified module path **before** calling them in the Python session.\n\n---\n\n<open_file> <path>app.tools.mac_commands.functions</path> <description><![CDATA[\nOpen a file using macOS open command.\n\nArgs:\nfilename (str): The name of the file to open\n\nReturns:\nNone\n]]></description>\n<usage_instructions><![CDATA[\nThe filename for a file can be obtained via the mysql database.  \nThe \'name\' column of the file contains its filename, which when inputted into open_file, will open the file on the user\'s computer.  \n]]></usage_instructions>\n</open_file>\n\n---\n\n<search_files_description> <path>app.tools.mysql.filebase.functions</path> <description><![CDATA[\nSearch for all fields of file entries in the mysql database using full text search on the "description" column.\n\nArgs:\nsearch_text (str): The text to search for in file descriptions\n\nReturns:\nList[Dict]: A list of file records matching the search criteria, ordered by relevance\n]]></description>\n<usage_instructions><![CDATA[\n\n\n**Usage example:**\n\n```python\nfrom app.tools.mysql.filebase.functions import search_files_description  \nresults = search_files_description("search query text")  \nprint(results[0]["description"])\n```\n\n**Important:**\n* Always assign the output to a variable, as the function returns an extremely long string. **never** print the whole output or the variable which contains it.\n* If you do results = search_files_description(...), **never** print results! Only print individual elements or parts of elements.\n* Do **not** call or import any function named `search_files` as it does not exist.\n* Always use the exact function name: `search_files_description`.\n]]></usage_instructions>\n</search_files_description>\n\n\n'}]}, {'role': 'user', 'content': [{'type': 'input_text', 'text': 'Open that video of the garbage set up I made that my dad was recording me and it dropped garbage'}]}, {'type': 'function_call', 'id': 'fc_68367934a60481989ae021393b56f2750baf40b6d85b197b', 'call_id': 'call_0bqjvuuEAOt0NnxYBc9vQ2C5', 'name': 'push_code', 'arguments': '{"code_str":"from app.tools.mysql.filebase.functions import search_files_description\\n\\n# Searching for the video related to the garbage setup\\nresults = search_files_description(\'garbage setup video\')\\nresults"}'}, {'type': 'function_call_output', 'call_id': 'call_0bqjvuuEAOt0NnxYBc9vQ2C5', 'output': '\'>>> from app.tools.mysql.filebase.functions import search_files_description\\n>>> \\n>>> # Searching for the video related to the garbage setup\\n>>> results = search_files_description(\\\'garbage setup video\\\')\\n>>> results\\n[{\\\'id\\\': 103, \\\'name\\\': \\\'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4\\\', \\\'ts\\\': datetime.datetime(2012, 1, 8, 11, 24, 25), \\\'ts_precision\\\': \\\'second\\\', \\\'extension\\\': \\\'mp4\\\', \\\'size\\\': 13840809, \\\'hash\\\': b\\\'}\\\\xb1\\\\xaeQ7f+\\\\xf7\\\\xe6$I\\\\xdah\\\\x80\\\\xeep\\\\x0bS\\\\xa7\\\\x02\\\\xc5w\\\\x98\\\\x90W\\\\xc64j\\\\xdc\\\\xa0{\\\\xbf\\\', \\\'parent_id\\\': None, \\\'derivative_of\\\': None, \\\'version_number\\\': 1, \\\'description\\\': "This is a video of me showing my experiment design for a garbage disposal using chairs. My dad is recording me and I show how my garbage disposal mechanism works. It\\\'s in the living room of the house and I\\\'m sitting on the couch while I tip the mechanism over for it to dump the garbage.", \\\'relevance\\\': 16.01902961730957}, {\\\'id\\\': 154, \\\'name\\\': \\\'MVI_0790-v1-4c53202a322e75c8d8bb83b1ede5a1088cd04f47c8168bb8811dcb0dae32eede.AVI\\\', \\\'ts\\\': datetime.datetime(2011, 5, 30, 19, 58, 36), \\\'ts_precision\\\': None, \\\'extension\\\': \\\'avi\\\', \\\'size\\\': 68042764, \\\'hash\\\': b\\\'LS *2.u\\\\xc8\\\\xd8\\\\xbb\\\\x83\\\\xb1\\\\xed\\\\xe5\\\\xa1\\\\x08\\\\x8c\\\\xd0OG\\\\xc8\\\\x16\\\\x8b\\\\xb8\\\\x81\\\\x1d\\\\xcb\\\\r\\\\xae2\\\\xee\\\\xde\\\', \\\'parent_id\\\': None, \\\'derivative_of\\\': None, \\\'version_number\\\': 1, \\\'description\\\': \\\'In this video, I have an obstacle course and my dad tries to hit me with a pillow as I traverse it. It looks like a setup I made and wanted my mom to record it.\\\', \\\'relevance\\\': 4.673060417175293}, {\\\'id\\\': 80, \\\'name\\\': \\\'DSC00911-v1-fbac31a1dff5b9dbb0d4221b0acb400e0e23fa0383d7fe39bbdc56299a32d636.JPG\\\', \\\'ts\\\': datetime.datetime(2025, 4, 22, 0, 16, 2), \\\'ts_precision\\\': None, \\\'extension\\\': \\\'jpg\\\', \\\'size\\\': 7659631, \\\'hash\\\': b\\\'\\\\xfb\\\\xac1\\\\xa1\\\\xdf\\\\xf5\\\\xb9\\\\xdb\\\\xb0\\\\xd4"\\\\x1b\\\\n\\\\xcb@\\\\x0e\\\\x0e#\\\\xfa\\\\x03\\\\x83\\\\xd7\\\\xfe9\\\\xbb\\\\xdcV)\\\\x9a2\\\\xd66\\\', \\\'parent_id\\\': None, \\\'derivative_of\\\': None, \\\'version_number\\\': 1, \\\'description\\\': \\\'My MacBook setup after buying two external monitors from Facebook Marketplace and bringing back my standing desk from the garage.\\\', \\\'relevance\\\': 3.781012773513794}]\''}, {'type': 'function_call', 'id': 'fc_6836793808908198b30ba69501c6cd540baf40b6d85b197b', 'call_id': 'call_wbosIIAc3j0hgYpOCJ9cJ5tl', 'name': 'push_code', 'arguments': '{"code_str":"from app.tools.mac_commands.functions import open_file\\n\\n# Opening the video file related to the garbage setup\\nvideo_filename = \'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4\'\\nopen_file(video_filename)"}'}, {'type': 'function_call_output', 'call_id': 'call_wbosIIAc3j0hgYpOCJ9cJ5tl', 'output': '">>> from app.tools.mac_commands.functions import open_file\\n>>> \\n>>> # Opening the video file related to the garbage setup\\n>>> video_filename = \'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4\'\\n>>> open_file(video_filename)"'}, {'id': 'msg_6836793a7aa0819886b247572c84d4220baf40b6d85b197b', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'The video of the garbage setup has been opened. Enjoy watching! If you need anything else, just let me know.'}]}, {'role': 'user', 'content': [{'type': 'input_text', 'text': 'When was that video recorded'}]}, {'id': 'msg_68367976c21c819880a5a0d38ab87bf10baf40b6d85b197b', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'The video was recorded on **January 8, 2012, at 11:24:25 AM**. If you have any more questions, feel free to ask!'}]}]
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
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "Open that video of the garbage set up I made that my dad was recording me and it dropped garbage"
      }
    ]
  },
  {
    "type": "function_call",
    "id": "fc_68367934a60481989ae021393b56f2750baf40b6d85b197b",
    "call_id": "call_0bqjvuuEAOt0NnxYBc9vQ2C5",
    "name": "push_code",
    "arguments": "{\"code_str\":\"from app.tools.mysql.filebase.functions import search_files_description\\n\\n# Searching for the video related to the garbage setup\\nresults = search_files_description('garbage setup video')\\nresults\"}"
  },
  {
    "type": "function_call_output",
    "call_id": "call_0bqjvuuEAOt0NnxYBc9vQ2C5",
    "output": "'>>> from app.tools.mysql.filebase.functions import search_files_description\\n>>> \\n>>> # Searching for the video related to the garbage setup\\n>>> results = search_files_description(\\'garbage setup video\\')\\n>>> results\\n[{\\'id\\': 103, \\'name\\': \\'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4\\', \\'ts\\': datetime.datetime(2012, 1, 8, 11, 24, 25), \\'ts_precision\\': \\'second\\', \\'extension\\': \\'mp4\\', \\'size\\': 13840809, \\'hash\\': b\\'}\\\\xb1\\\\xaeQ7f+\\\\xf7\\\\xe6$I\\\\xdah\\\\x80\\\\xeep\\\\x0bS\\\\xa7\\\\x02\\\\xc5w\\\\x98\\\\x90W\\\\xc64j\\\\xdc\\\\xa0{\\\\xbf\\', \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \"This is a video of me showing my experiment design for a garbage disposal using chairs. My dad is recording me and I show how my garbage disposal mechanism works. It\\'s in the living room of the house and I\\'m sitting on the couch while I tip the mechanism over for it to dump the garbage.\", \\'relevance\\': 16.01902961730957}, {\\'id\\': 154, \\'name\\': \\'MVI_0790-v1-4c53202a322e75c8d8bb83b1ede5a1088cd04f47c8168bb8811dcb0dae32eede.AVI\\', \\'ts\\': datetime.datetime(2011, 5, 30, 19, 58, 36), \\'ts_precision\\': None, \\'extension\\': \\'avi\\', \\'size\\': 68042764, \\'hash\\': b\\'LS *2.u\\\\xc8\\\\xd8\\\\xbb\\\\x83\\\\xb1\\\\xed\\\\xe5\\\\xa1\\\\x08\\\\x8c\\\\xd0OG\\\\xc8\\\\x16\\\\x8b\\\\xb8\\\\x81\\\\x1d\\\\xcb\\\\r\\\\xae2\\\\xee\\\\xde\\', \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \\'In this video, I have an obstacle course and my dad tries to hit me with a pillow as I traverse it. It looks like a setup I made and wanted my mom to record it.\\', \\'relevance\\': 4.673060417175293}, {\\'id\\': 80, \\'name\\': \\'DSC00911-v1-fbac31a1dff5b9dbb0d4221b0acb400e0e23fa0383d7fe39bbdc56299a32d636.JPG\\', \\'ts\\': datetime.datetime(2025, 4, 22, 0, 16, 2), \\'ts_precision\\': None, \\'extension\\': \\'jpg\\', \\'size\\': 7659631, \\'hash\\': b\\'\\\\xfb\\\\xac1\\\\xa1\\\\xdf\\\\xf5\\\\xb9\\\\xdb\\\\xb0\\\\xd4\"\\\\x1b\\\\n\\\\xcb@\\\\x0e\\\\x0e#\\\\xfa\\\\x03\\\\x83\\\\xd7\\\\xfe9\\\\xbb\\\\xdcV)\\\\x9a2\\\\xd66\\', \\'parent_id\\': None, \\'derivative_of\\': None, \\'version_number\\': 1, \\'description\\': \\'My MacBook setup after buying two external monitors from Facebook Marketplace and bringing back my standing desk from the garage.\\', \\'relevance\\': 3.781012773513794}]'"
  },
  {
    "type": "function_call",
    "id": "fc_6836793808908198b30ba69501c6cd540baf40b6d85b197b",
    "call_id": "call_wbosIIAc3j0hgYpOCJ9cJ5tl",
    "name": "push_code",
    "arguments": "{\"code_str\":\"from app.tools.mac_commands.functions import open_file\\n\\n# Opening the video file related to the garbage setup\\nvideo_filename = 'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4'\\nopen_file(video_filename)\"}"
  },
  {
    "type": "function_call_output",
    "call_id": "call_wbosIIAc3j0hgYpOCJ9cJ5tl",
    "output": "\">>> from app.tools.mac_commands.functions import open_file\\n>>> \\n>>> # Opening the video file related to the garbage setup\\n>>> video_filename = 'video-2012-01-08-11-24-25-v1-7db1ae5137662bf7e62449da6880ee700b53a702c577989057c6346adca07bbf.mp4'\\n>>> open_file(video_filename)\""
  },
  {
    "id": "msg_6836793a7aa0819886b247572c84d4220baf40b6d85b197b",
    "role": "assistant",
    "content": [
      {
        "type": "output_text",
        "text": "The video of the garbage setup has been opened. Enjoy watching! If you need anything else, just let me know."
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "When was that video recorded"
      }
    ]
  }
]