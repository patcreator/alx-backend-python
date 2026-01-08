#!/usr/bin/python3
"""
4-stream_ages.py
Computes the average age of users using generators (memory-efficient)
"""

import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that yields user ages one by one
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="ALX_prodev"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:   
            yield age

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")


def calculate_average_age():
    """
    Calculates and prints the average age using the generator
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():   
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("Average age of users: 0")


if __name__ == "__main__":
    calculate_average_age()
