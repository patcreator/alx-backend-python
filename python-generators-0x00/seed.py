#!/usr/bin/python3
"""
seed.py
Sets up the MySQL database and seeds user data
"""

import csv
import mysql.connector
from mysql.connector import Error


# --------------------------------------------------
# Connect to MySQL server
# --------------------------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# --------------------------------------------------
# Create database if it does not exist
# --------------------------------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS ALX_prodev"
    )
    cursor.close()


# --------------------------------------------------
# Connect specifically to ALX_prodev database
# --------------------------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# --------------------------------------------------
# Create table user_data
# --------------------------------------------------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


# --------------------------------------------------
# Insert data from CSV (skip duplicates)
# --------------------------------------------------
def insert_data(connection, data):
    cursor = connection.cursor()

    with open(data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            cursor.execute("""
                SELECT user_id FROM user_data WHERE user_id = %s
            """, (row['user_id'],))

            if cursor.fetchone():
                continue  # Skip if already exists

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (
                row['user_id'],
                row['name'],
                row['email'],
                row['age']
            ))

    connection.commit()
    cursor.close()
