#!/usr/bin/python3
"""
1-batch_processing.py
Batch processing users using generators
"""

seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """
    Generator yielding users in batches
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []

    for row in cursor:            # Loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Process each batch and print users older than 25
    """
    for batch in stream_users_in_batches(batch_size):   # Loop 2
        for user in batch:                              # Loop 3
            if user["age"] > 25:
                print(user)
