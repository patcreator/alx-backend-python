#!/usr/bin/python3
"""
1-batch_processing.py
Fetches and processes users in batches using generators
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []

        for row in cursor:  
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")


def batch_processing(batch_size):
    """
    Processes batches and prints users older than 25
    """
    for batch in stream_users_in_batches(batch_size):  
      
        for user in batch:  
            if user["age"] > 25:
                print(user)
