"""
Database module for the Habit Tracking Application.

This module handles all low-level SQLite operations, including:
    - Creating required tables
    - Inserting new habit records
    - Retrieving stored records for analytics
    - Querying data for daily, weekly, and monthly reports
    - Fetching entries for streak calculations

It provides a simple abstraction layer so the rest of the application
can interact with the database without writing SQL directly.
"""

import sqlite3


DB_PATH = "habits.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        frequency TEXT NOT NULL,
        is_quantitative INTEGER NOT NULL,
        max_entries_per_period INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        entry_date TEXT NOT NULL,
        value REAL,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
    """)

    conn.commit()
    conn.close()