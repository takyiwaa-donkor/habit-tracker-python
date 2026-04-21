"""
Lightweight SQLite helper module for storing habit records.

Provides simple functions for connecting to the database, creating the
`records` table, inserting entries, and retrieving daily, weekly, or
monthly records.
"""


import sqlite3

DB_NAME = "habits.db"


# =============================
# CONNECT DATABASE
# =============================

def connect_db():
    return sqlite3.connect(DB_NAME)


# =============================
# CREATE TABLES
# =============================

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        value REAL,
        unit TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# =============================
# ADD RECORD
# =============================

def add_record(habit_id, value, unit, date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO records (habit_id,value,unit,date) VALUES (?,?,?,?)",
        (habit_id, value, unit, date)
    )

    conn.commit()
    conn.close()


# =============================
# GET ALL RECORDS
# =============================

def get_records():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT habit_id,value,unit,date FROM records")

    data = cursor.fetchall()

    conn.close()

    return data

def get_records_by_habit(habit_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date FROM records WHERE habit_id=? ORDER BY date",
        (habit_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

# =============================
# DAILY RECORDS
# =============================

def get_records_today():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_id, date
        FROM records
        WHERE date = date('now')
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# =============================
# WEEKLY RECORDS
# =============================

def get_records_last_7_days():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_id, date
        FROM records
        WHERE date >= date('now','-7 day')
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# =============================
# MONTHLY RECORDS
# =============================

def get_records_last_30_days():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_id, date
        FROM records
        WHERE date >= date('now','-30 day')
    """)

    data = cursor.fetchall()

    conn.close()

    return data
