import mysql.connector
from mysql.connector import Error
from typing import Optional

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': 'localhost',  # Docker container host
            'port': 3306,         # Default MySQL port
            'user': 'root',       # Default MySQL user
            'password': 'Admin2025',  # Your MySQL password from Docker
            'database': 'crypto_umg_db'  # Your database name from Docker
        }

    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute an update query (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing update: {e}")
            return False

# Example usage:
if __name__ == "__main__":
    db = DatabaseConnection()
    if db.connect():
        # Example query
        results = db.execute_query("SELECT VERSION()")
        if results:
            print(f"MySQL Version: {results[0][0]}")
        db.disconnect() 