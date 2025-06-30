from mac_client import console
import os
import json
import ast
import base64

CHUNK_SIZE = 8192
SERVER_TRANSFER_DIR = '/home/parsa/transfer/'

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    temp_file_dir = os.path.join(SERVER_TRANSFER_DIR, file_name)
    status_path = os.path.join(temp_file_dir, "status.json")

    binarystatus = console.push_code(f"""\
import os
import json

os.makedirs("{temp_file_dir}", exist_ok=True)

if not os.path.exists("{status_path}"):
    status = {{
        "file_name": "{file_name}",
        "received_offsets": [],
        "total_chunks": None
    }}
else:
    with open("{status_path}", 'r') as f:
        status = json.load(f)

print(status)
""")
    stringstatus = binarystatus.decode('utf-8')
    status = ast.literal_eval(stringstatus)
    received_offsets = set(status['received_offsets'])

    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE

    with open(file_path, 'rb') as f:
        for i in range(total_chunks):
            offset = i * CHUNK_SIZE
            if offset in received_offsets:
                continue

            f.seek(offset)
            chunk_data = f.read(CHUNK_SIZE)
            chunk_name = f"{offset:08x}"
            chunk_path = os.path.join(temp_file_dir, chunk_name)

            console.push_code(f"""\
status["total_chunks"] = {total_chunks}
import base64
encoded_data = "{base64.b64encode(chunk_data).decode('ascii')}"
chunk_data = base64.b64decode(encoded_data)

with open("{chunk_path}", "wb") as chunk_file:
    chunk_file.write(chunk_data)

status['received_offsets'].append({offset})
with open("{status_path}", 'w') as sf:
    json.dump(status, sf)

""")








def james():
            console.push_code(f"""\
with open("{chunk_path}", "wb") as chunk_file:
    chunk_file.write(GOOZ MAN!!!)
""")
            
            console.push_code(f"""
{chunk_data}
""")
            
            jamesie = f"""this is some random text and then:{chunk_data} that was it"""
            print("JAMESIE INCOMING!\n\n\n")

            result = console.push_code(f"""\
import base64
encoded_data = "{base64.b64encode(chunk_data).decode('ascii')}"
guzcheh = base64.b64decode(encoded_data)
""")
            print(result)


"""
from mac_client.file_transfer import upload_file
upload_file('/Users/parsashemirani/Main/Inbox/VID_20141228_211947.mp4')
"""