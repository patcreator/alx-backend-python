import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries

def log_queries(func):
    """Decorator that logs SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Log the query with timestamp
        print(f"[{timestamp}] Executing query: {kwargs['query']}")
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
