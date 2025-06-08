        query = """
            SELECT 
                version_number 
            FROM files 
            WHERE hash = %s
        """
        result = filebase_instance.execute_read(query, [hash_value], fetch_one=True)
        if result is None:
            return 0
        return result['version_number']


def get_version_number()