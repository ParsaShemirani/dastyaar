from server.sqliteinterface import SQLiteInterface
from server.read_filebase import get_all_via_id
filebase_db = SQLiteInterface('/home/parsa/serverfiles/filebase_test.db')



def upsert_file(file_dict):
    if '_id' in file_dict:
        file_id = file_dict['_id']

        filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}
        if not filtered_dict:
            return
            
        current_record = get_all_via_id(file_id=file_id)
        if not current_record:
            raise ValueError(f"No record found with id: {file_id}")
            
        columns_to_update = {}
        for key, value in filtered_dict.items():
            if key not in current_record or current_record[key] is None:
                columns_to_update[key] = value
        if not columns_to_update:
            return
            
        set_clauses = []
        values = []
        
        for key, value in columns_to_update.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        set_clause = ', '.join(set_clauses)
        
        query = f"""
        UPDATE files
        SET {set_clause}
        WHERE id = ?
        """
        
        values.append(file_id)
        
        filebase_db.execute_write(
            query=query,
            params=values,
            many=False
        )
        
    else:
        filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}
        if not filtered_dict:
            return
            
        columns = ', '.join(filtered_dict.keys())
        placeholders = ', '.join(['?'] * len(filtered_dict))
        query = f"""
        INSERT INTO files 
             ({columns})
        VALUES 
             ({placeholders})
        """
        values = list(filtered_dict.values())
        
        filebase_db.execute_write(
             query=query,
             params=values,
             many=False
        )