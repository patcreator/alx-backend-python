import sqlite3

class ExecuteQuery:
    """Reusable context manager that executes a query with parameters."""
    
    def __init__(self, database_name, query, params=None):
        """
        Initialize the context manager.
        
        Args:
            database_name: Name of the SQLite database file
            query: SQL query to execute
            params: Parameters for the query (default: None)
        """
        self.database_name = database_name
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Execute the query when entering the context."""
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # Return False to propagate any exceptions
        return False


# Use the context manager with the specified query and parameter
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
