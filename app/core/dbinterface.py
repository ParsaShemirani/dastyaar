from mysql.connector import connect, Error
from typing import Dict, List, Any, Optional, Union, Tuple
from app.core.exceptions import DatabaseError


class MySQLInterface:
    """
    Provides MySQL connection and helper methods for executing
    read and write operations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the database connection.

        Args:
            config: MySQL connection parameters.
        """
        self.config = config
        self.connection = None

    def _ensure_connection(self):
        """Ensures there is an active connection, creating one if needed."""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = connect(**self.config)
        except Error as e:
            raise DatabaseError(f"Error connecting to database: {e}")

    def execute_read(
        self,
        query: str,
        params: Optional[Union[Dict, List, Tuple]] = None,
        fetch_one: bool = False
    ) -> Union[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Executes a SELECT query and returns the results.

        Args:
            query: SQL SELECT statement with placeholders.
            params: Parameters to bind to the query.
            fetch_one: If True, return a single record; otherwise return all rows.

        Returns:
            A single row as a dict if fetch_one is True, an empty dict if no row found,
            or a list of row dicts for multiple records.

        Raises:
            DatabaseError: If the query execution fails.
        """
        self._ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                return row
            return cursor.fetchall()
        except Error as e:
            raise DatabaseError(f"Error executing read query: {e}")
        finally:
            cursor.close()

    def execute_write(
        self,
        query: str,
        params: Union[Dict, List, Tuple, List[Union[Dict, List, Tuple]]],
        many: bool = False
    ) -> int:
        """
        Executes an INSERT, UPDATE, or DELETE statement.

        Args:
            query: SQL statement with placeholders.
            params: Parameters for the statement, or a list of parameter sets for batch.
            many: If True, execute batch operation with executemany.

        Returns:
            The number of affected rows.

        Raises:
            DatabaseError: If the write operation fails.
        """
        self._ensure_connection()
        cursor = self.connection.cursor()
        try:
            if many:
                cursor.executemany(query, params)  # type: ignore[arg-type]
            else:
                cursor.execute(query, params)      # type: ignore[arg-type]
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Error executing write query: {e}")
        finally:
            cursor.close()

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __del__(self):
        """Ensures the connection is closed when the object is destroyed."""
        self.close()


# Example usage

if __name__ == "__main__":
    # Example MySQL configuration (replace with your own settings)
    config = {
        "host": "localhost",
        "user": "root",
        "password": "your_password",
        "database": "your_database",
    }

    # Initialize the database interface
    db = MySQLInterface(config=config)

    # Example: Insert a new user
    try:
        insert_query = "INSERT INTO users (name) VALUES (%s)"
        inserted_rows = db.execute_write(insert_query, params=("Alice",))
        print(f"Inserted rows: {inserted_rows}")
    except DatabaseError as e:
        print(f"Insert failed: {e}")

    # Example: Read users
    try:
        select_query = "SELECT id, name FROM users"
        users = db.execute_read(select_query)
        print("Users:", users)
    except DatabaseError as e:
        print(f"Select failed: {e}")

    # Example: Fetch a single user
    try:
        select_one_query = "SELECT id, name FROM users WHERE name = %s"
        user = db.execute_read(select_one_query, params=("Alice",), fetch_one=True)
        print("Fetched user:", user)
    except DatabaseError as e:
        print(f"Fetch one failed: {e}")
    finally:
        db.close()
