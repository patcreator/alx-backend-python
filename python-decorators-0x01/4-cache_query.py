import time
import sqlite3
import functools

# The cache dictionary (provided in the template)
query_cache = {}

# Define the with_db_connection decorator first
def with_db_connection(func):
    """Decorator that automatically opens and closes database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Implement the cache_query decorator
def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments (it's passed as keyword argument 'query')
        query = kwargs.get('query')
        
        # Check if result is already cached
        if query in query_cache:
            print(f"Cache hit for query: {query[:30]}...")  # Show first 30 chars
            return query_cache[query]
        
        # If not cached, execute the function and cache the result
        print(f"Cache miss for query: {query[:30]}...")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
