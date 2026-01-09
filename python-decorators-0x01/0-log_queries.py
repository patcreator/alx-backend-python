import sqlite3
import functools

#### decorator to log SQL queries

def log_queries(func):
    """Decorator that logs SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from keyword arguments or position arguments
        query = kwargs.get('query', None)
        
        # If not found in kwargs, check args (assuming query is first arg after self if method)
        if query is None and args:
            # Try to find a string argument that looks like a SQL query
            for arg in args:
                if isinstance(arg, str) and (arg.upper().startswith('SELECT') or 
                                           arg.upper().startswith('INSERT') or
                                           arg.upper().startswith('UPDATE') or
                                           arg.upper().startswith('DELETE')):
                    query = arg
                    break
        
        # Log the query
        if query:
            print(f"Executing query: {query}")
        else:
            print("No SQL query found to log")
        
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
