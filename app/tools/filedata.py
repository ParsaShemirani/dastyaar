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

    def filld_basename(self):
        self.basename = file_functions.extract_basename_from_file_path(
            file_path=self.file_path
        )

    def filld_rootname(self):
        self.rootname = file_functions.extract_rootname_from_basename(
            basename=self.basename
        )

    def filld_extension(self):
        self.extension = file_functions.get_file_extension(
            file_path=self.file_path
        )
    
    def filld_version_number(self):
        if self.basename == f"{self.rootname}.{self.extension}":
            self.version_number = 1
        else:
            hash_from_basename = file_functions.extract_hash_from_basename(
                basename=self.basename
            )
            parent_version = filebase_functions.get_version_number_via_hash(
                hash=hash_from_basename
            )
            self.version_number = parent_version + 1

    def filld_name(self):
        self.name = file_functions.generate_new_filename(
            rootname=self.rootname,
            version_number=self.version_number,
            hash=self.hash,
            extension=self.extension
        )

    def filld_size(self):
        self.size = file_functions.get_file_size(
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

    def generate_file_dict(self):
        file_dict = {}
        for col in self.files_table_columns:
            if hasattr(self,col):
                file_dict[col] = getattr(self, col)
        return file_dict