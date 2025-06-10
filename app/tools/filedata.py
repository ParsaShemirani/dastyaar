#The sun set slowly, painting the sky with hues of orange.

from app.tools import file_functions
from app.tools import filebase_functions
class FileData:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.files_table_columns = [
            'hash','version_number','size','extension','ts','name'
        ]
        
    def filld_hash(self):
        self.hash = file_functions.generate_sha_hash(
            file_path=self.file_path
        )

    def is_unique(self):
        result = filebase_functions.get_file_id_via_hash(
            hash=self.hash
        )
        if result is None:
            return True
        else:
            return False

    def filld_version_number(self):
        filename_hash = file_functions.extract_hash_from_filename(
            file_path=self.file_path
        )
        if filename_hash is None:
            self.version_number = 1
        else: 
            result = filebase_functions.get_version_number_via_hash(
                hash=self.hash
            )
            self.version_number = result + 1
    
    def filld_size(self):
        self.size = file_functions.get_file_size(
            file_path=self.file_path
        )

    def filld_extension(self):
        self.extension = file_functions.get_file_extension(
            file_path=self.file_path
        )

    def filld_ts(self):
        if self.version_number == 1:
            self.ts = file_functions.get_created_time(
                file_path=self.file_path
            )
        else:
            self.ts = file_functions.get_modified_time(
                file_path=self.file_path
            )
    def filld_name(self):
        self.name = file_functions.generate_new_filename(
            file_path=self.file_path,
            version_number=self.version_number,
            hash=self.hash
        )
    
    def generate_file_dict(self):
        file_dict = {}
        for col in self.files_table_columns:
            if hasattr(self,col):
                file_dict[col] = getattr(self, col)

        return file_dict