#!/usr/bin/python3
"""
2-lazy_paginate.py
Implements lazy pagination using a generator
"""

seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a single page of users
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads pages of users
    """
    offset = 0

    while True:  # ✅ only ONE loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
