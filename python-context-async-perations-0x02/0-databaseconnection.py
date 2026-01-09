
import sqlite3

class DatabaseConnection:
    """Custom class-based context manager for database connections."""
    
    def __init__(self, database_name):
        """Initialize the context manager with database name."""
        self.database_name = database_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection when entering the context."""
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection when exiting the context."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # Return False to propagate any exceptions that occurred
        return False


# Use the context manager to execute a query
with DatabaseConnection('users.db') as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
