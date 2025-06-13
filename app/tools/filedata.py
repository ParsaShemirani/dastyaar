from app.tools import file_functions
from app.tools import filebase_functions
class FileData:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.files_table_columns = [
            'hash','size','extension','version_number','name','ts','ingested_ts'
        ]

    def filld_hash(self):
        self.hash = file_functions.generate_sha_hash(
            file_path=self.file_path
        )

    def filld_size(self):
        self.size = file_functions.get_file_size(
            file_path=self.file_path
        )

    def filld_extension(self):
        self.extension = file_functions.get_file_extension(
            file_path=self.file_path
        )


    def filld_basename(self):
        self.basename = file_functions.extract_basename_from_file_path(
            file_path=self.file_path
        )

    def filld_rootname(self):
        self.rootname = file_functions.extract_rootname_from_basename(
            basename=self.basename
        )

    def filld_hash_from_basename(self):
        self.hash_from_basename = file_functions.extract_hash_from_basename(
            basename=self.basename
        )

    def filld_previous_id(self):
        self.previous_id = filebase_functions.get_file_id_via_hash(
            hash=self.hash_from_basename
        )

    def filld_updated_version_number(self):
        parent_version = filebase_functions.get_version_number_via_hash(
            hash=self.hash_from_basename
        )
        self.version_number = parent_version + 1

    def filld_name(self):
        self.name = file_functions.generate_new_filename(
            rootname=self.rootname,
            version_number=self.version_number,
            hash=self.hash,
            extension=self.extension
        )

    def filld_new_file_path(self):
        self.new_file_path = file_functions.generate_new_file_path(
            file_path=self.file_path,
            new_name=self.name
        )

    def filld_created_ts(self):
        self.ts = file_functions.get_created_time(
            file_path=self.file_path
        )

    def filld_modifed_ts(self):
        self.ts = file_functions.get_modified_time(
            file_path=self.file_path
        )

    def filld_ingested_ts(self):
        self.ingested_ts = file_functions.get_current_time()

    def filld_file_dict(self):
        file_dict = {}
        for col in self.files_table_columns:
            if hasattr(self,col):
                file_dict[col] = getattr(self, col)
        self.file_dict = file_dict
    



    # BATCH FILLD
    
    def filld_standard(self):
        self.filld_hash()
        self.filld_size()
        self.filld_extension()
        self.filld_basename()
        self.filld_rootname()
        self.filld_hash_from_basename()

        if self.hash_from_basename is not None:
            self.filld_previous_id()
            self.filld_updated_version_number()
            self.filld_modifed_ts()
        else:
            self.version_number = 1
            self.filld_created_ts()
        self.filld_ingested_ts()
        self.filld_name()
        self.filld_new_file_path()
        self.filld_file_dict()




    # FILEBASE INVOLVEMENT
    def is_unique(self):
        result = filebase_functions.get_file_id_via_hash(
            hash=self.hash
        )
        if result is None:
            return True
        else:
            return False
        
    def insert_file_dict(self):
        filebase_functions.insert_file(
            file_dict=self.file_dict
        )
        self.file_id = filebase_functions.get_file_id_via_hash(
            hash=self.hash
        )




    # OTHER TABLES RELATED
    def associate_groupings(self):
        if hasattr(self, 'groupings'):
            for grouping in self.groupings:
                filebase_functions.associate_groupings(
                    file_id=self.file_id,
                    grouping_id=grouping
                )

    def associate_previous_id(self):
        if hasattr(self, 'previous_id'):
            filebase_functions.associate_previous_id(
                file_id=self.file_id,
                previous_id=self.previous_id
            )
    
    def associate_description(self):
        if hasattr(self, 'description'):
            filebase_functions.associate_description(
                file_id=self.file_id,
                description=self.description
            )

    def associate_location(self):
        if hasattr(self, 'location_id'):
            filebase_functions.associate_location(
                file_id=self.file_id,
                location_id=self.location_id
            )

    def associate_all(self):
        self.associate_groupings()
        self.associate_previous_id()
        self.associate_description()
        self.associate_location()


    # RENAME | REMOVE
    def rename_file(self):
        file_functions.rename_file(
            file_path=self.file_path,
            new_file_path=self.new_file_path
        )

    def remove_file(self):
        file_functions.remove_file(
            file_path=self.new_file_path
        )



