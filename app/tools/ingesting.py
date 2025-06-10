from app.tools.filedata import FileData

def ingest_standard(file_path):
    file_object = FileData(file_path=file_path)
    print('james')

    file_object.filld_hash()

    print('timidman')
    print(file_object.hash)

    if file_object.is_unique == False:
        print("File already exists in database")
        exit()

    file_object.filld_version_number()
    file_object.filld_size()
    file_object.filld_extension()
    file_object.filld_ts()
    file_object.filld_name()

    print(file_object.hash)
    print(file_object.version_number)
    print(file_object.size)
    print(file_object.extension)
    print(file_object.ts)
    print(file_object.name)




