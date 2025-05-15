from mysql.connector import pooling, Error
from typing import Dict, List, Any, Optional, Union, Tuple
from app.core.exceptions import DatabaseError


class MySQLPoolInterface:
    """
    Provides MySQL connection pooling and helper methods for executing
    read and write operations.
    """

    def __init__(self,
                 config: Dict[str, Any],
                 pool_name: str = "mypool",
                 pool_size: int = 5):
        """
        Initializes the connection pool.

        Args:
            config: MySQL connection parameters.
            pool_name: Name of the connection pool.
            pool_size: Number of connections in the pool.
        """
        self.pool = pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            **config
        )

    def execute_read(
        self,
        query: str,
        params: Optional[Union[Dict, List, Tuple]] = None,
        fetch_one: bool = False
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
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
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                return row if row is not None else {}
            return cursor.fetchall()
        except Error as e:
            raise DatabaseError(f"Error executing read query: {e}")
        finally:
            cursor.close()
            conn.close()


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
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            if many:
                cursor.executemany(query, params)  # type: ignore[arg-type]
            else:
                cursor.execute(query, params)      # type: ignore[arg-type]
            conn.commit()
            return cursor.rowcount
        except Error as e:
            conn.rollback()
            raise DatabaseError(f"Error executing write query: {e}")
        finally:
            cursor.close()
            conn.close()


# Example usage

if __name__ == "__main__":
    # Example MySQL configuration (replace with your own settings)
    config = {
        "host": "localhost",
        "user": "root",
        "password": "your_password",
        "database": "your_database",
    }

    # Initialize the pool interface
    db_pool = MySQLPoolInterface(config=config, pool_name="testpool", pool_size=3)

    # Example: Insert a new user
    try:
        insert_query = "INSERT INTO users (name) VALUES (%s)"
        inserted_rows = db_pool.execute_write(insert_query, params=("Alice",))
        print(f"Inserted rows: {inserted_rows}")
    except DatabaseError as e:
        print(f"Insert failed: {e}")

    # Example: Read users
    try:
        select_query = "SELECT id, name FROM users"
        users = db_pool.execute_read(select_query)
        print("Users:", users)
    except DatabaseError as e:
        print(f"Select failed: {e}")

    # Example: Fetch a single user
    try:
        select_one_query = "SELECT id, name FROM users WHERE name = %s"
        user = db_pool.execute_read(select_one_query, params=("Alice",), fetch_one=True)
        print("Fetched user:", user)
    except DatabaseError as e:
        print(f"Fetch one failed: {e}")