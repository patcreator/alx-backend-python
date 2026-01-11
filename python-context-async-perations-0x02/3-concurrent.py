import asyncio
import aiosqlite

async def async_fetch_users():
    """Asynchronously fetch all users from the database."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users fetched:", users)
            return users

async def async_fetch_older_users():
    """Asynchronously fetch users older than 40."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40 fetched:", older_users)
            return older_users

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather."""
    # Execute both async functions concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    # results[0] contains all users, results[1] contains users older than 40
    return results

# Run the concurrent queries
if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
