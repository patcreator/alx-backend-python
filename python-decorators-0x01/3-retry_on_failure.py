import time
import sqlite3
import functools

# Paste the with_db_connection decorator
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

# Implement the retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    """Decorator that retries database operations on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    if attempt < retries:
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed. Last error: {e}")
                        raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
