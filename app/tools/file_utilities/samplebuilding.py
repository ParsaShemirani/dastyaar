#from app.tools.file_utilities import core_james
import core_james
def generate_sha_hash_dict(file_dict):
    file_path= file_dict['file_path']
    result = core_james.generate_sha_hash(file_path=file_path)
    file_dict['hash'] = result
    return file_dict

def get_created_time_dict(file_dict):
    file_path= file_dict['file_path']
    result = core_james.get_created_time(file_path=file_path)
    file_dict['ts'] = result
    return file_dict

def generate_new_filename_dict(file_dict):
    file_path= file_dict['file_path']
    version_number = file_dict['version_number']
    hash = file_dict['hash']
    result = core_james.generate_new_filename(
        file_path=file_path,
        version_number=version_number,
        hash=hash
    )
    file_dict['name'] = result
    return file_dict

def generate_new_file_path_dict(file_dict):
    file_path= file_dict['file_path']
    new_name = file_dict['name']
    result = core_james.generate_new_file_path(file_path=file_path,new_name=new_name)
    file_dict['new_file_name'] = result
    return file_dict


"""
Logical outline:
Function takes file_dict as parameter.
Then, it extracts the relevant values that are needed for the core_james function.
Then, it assigns 'result' as the return of the core_james funciton with those parameters.
It then assings the appropriate new key value pair in the file_dict, updating it.
It then returns the new file_dict.


Idea: a new dictionary. The keys are functions from core_james.
The value is another dictionary, one key value being the dictionary value
of file_dict that the result will be assigned to,
the other being a list of the parameters that the core_james function needs.
"""

file_function_reference = {
    'generate_new_file_path': {
        'parameters': ['file_path','name'],
        'result_key': 'new_file_path'
    },
    'get_created_time': {
        'parameters': ['file_path'],
        'result_key': 'ts'
    },
    'get_modified_time': {
        'parameters': ['file_path'],
        'result_key': 'ts'
    },
    'generate_sha_hash': {
        'parameters': ['file_path'],
        'result_key': 'hash'
    },
    'get_file_extension': {
        'parameters': ['file_path'],
        'result_key': 'extension'
    },
    'get_file_size': {
        'parameters': ['file_path'],
        'result_key': 'size'
    },
    'generate_new_filename': {
        'parameters': ['file_path','version_number','hash'],
        'result_key': 'name'
    },
    'generate_first_filename': {
        'parameters': ['file_path','version_number','hash'],
        'result_key': 'name'
    },
    'extract_voice_rec_ts': {
        'parameters': ['file_path'],
        'result_key': 'ts'
    }
}

def develop_file_dict(file_dict, core_function):
    arguments = {}
    func = getattr(core_james, core_function)
    result_key = file_function_reference[core_function]['result_key']
    for param in file_function_reference[core_function]['parameters']:
        arguments[param] = file_dict[param]

    result = func(**arguments)
    file_dict[result_key] = result

    return file_dict

random_sha256_hash = b'\xa3\x1f\x9c\x4b\x7d\x8e\x2a\x0c\xf6\x93\xfe\x5d\x14\x27\xbd\x8e\x19\x60\x42\xea\x88\x7f\x11\xcd\x33\x84\x56\x2a\x70\x9b\xfd\xcb'

#example_gaming
file_dict = {
    'file_path': '/Users/parsa/jamietown.mp4',
    'version_number': 1,
    'hash': b'\xa3\x1f\x9c\x4b\x7d\x8e\x2a\x0c\xf6\x93\xfe\x5d\x14\x27\xbd\x8e\x19\x60\x42\xea\x88\x7f\x11\xcd\x33\x84\x56\x2a\x70\x9b\xfd\xcb'
}

timid = develop_file_dict(file_dict=file_dict, core_function='generate_first_filename')
print("JAMIE")
print(timid)