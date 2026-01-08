
#!/usr/bin/python3
"""
0-stream_users.py
Streams users from the database one by one using a generator
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that yields rows from user_data table one at a time
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

        for row in cursor:   
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")
