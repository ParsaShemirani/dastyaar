from flask import Flask, request, jsonify
import sqlite3

# Converters for bin/hex
def convert_binary_to_hex(obj):
    if isinstance(obj, bytes):
        return {"_type": "hex", "data": obj.hex()}
    elif isinstance(obj, list):
        return [convert_binary_to_hex(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_binary_to_hex(value) for key, value in obj.items()}
    else:
        return obj
    
def convert_hex_to_binary(obj):
    if isinstance(obj, dict):
        if obj.get("_type") == "hex" and "data" in obj:
            return bytes.fromhex(obj["data"])
        else:
            return {key: convert_hex_to_binary(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_hex_to_binary(item) for item in obj]
    else:
        return obj


# Database read/write
def db_execute_read(database_path, query, params=[], fetch_one=False):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        if fetch_one:
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
    finally:
        cursor.close()
        connection.close()

def db_execute_write(database_path, query, params=[], many=False):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()



# Main app
def create_app():
    app = Flask(__name__)

    @app.route("/execute_read", methods=['POST'])
    def execute_read():
        data = dict(request.get_json())
        data = convert_hex_to_binary(obj=data)
        
        result = db_execute_read(
            database_path=data['database_path'],
            query=data['query'],
            params=data['params'],
            fetch_one=data['fetch_one']
        )
        result = convert_binary_to_hex(obj=result)
        return jsonify(result)
    
    @app.route("/execute_write", methods=['POST'])
    def execute_write():
        data = dict(request.get_json())
        data = convert_hex_to_binary(obj=data)

        result = db_execute_write(
            database_path=data['database_path'],
            query=data['query'],
            params=data['params'],
            many=data['many']
        )
        print(result)
        return jsonify(
            {"affected_rows": result}
        )
    
    return app

    