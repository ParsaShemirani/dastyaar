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


Idea: a new dictionary, containing the name of the new key as the keys,
and the values being the function to call from core_james, etc.
"""