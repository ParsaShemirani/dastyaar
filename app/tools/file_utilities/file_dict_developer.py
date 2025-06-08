import core_james

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

def develop_file_dict(file_dict, file_function):
    arguments = {}
    func = getattr(core_james, file_function)
    result_key = file_function_reference[file_function]['result_key']
    for param in file_function_reference[file_function]['parameters']:
        arguments[param] = file_dict[param]
    result = func(**arguments)
    file_dict[result_key] = result
    return file_dict