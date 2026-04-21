"""
Repository module for the Habit Tracking Application.

This module provides a high-level abstraction over the low-level
SQLite operations defined in `database.py`. It acts as the data
access layer (DAL), ensuring that the rest of the application
interacts with clean Python functions instead of raw SQL queries.

Responsibilities:
    - Inserting new habit records into the database
    - Retrieving all stored records
    - Fetching records filtered by habit ID
    - Retrieving entries for daily, weekly, and monthly reports
    - Supporting streak calculations by returning ordered date lists
    - Ensuring consistent data access patterns across the application

The repository layer improves maintainability by separating
database logic from business logic, enabling easier testing,
refactoring, and future migration to other storage backends.
"""
import datetime
from datetime import datetime
from persistence.database import get_connection
from domain.habit import Habit
from domain.habit_entry import HabitEntry


class Repository:

    def add_habit(self, habit):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO habits (name, frequency, is_quantitative, max_entries_per_period)
            VALUES (?, ?, ?, ?)
        """, (habit.name, habit.frequency, int(habit.is_quantitative), habit.max_entries_per_period))

        conn.commit()
        conn.close()


    def get_all_habits(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()
        conn.close()

        return [
            Habit(
                id=row[0],
                name=row[1],
                frequency=row[2],
                is_quantitative=bool(row[3]),
                max_entries_per_period=row[4]
            )
            for row in rows
        ]



    def add_habit_entry(self, entry):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO habit_entries (habit_id, entry_date, value)
            VALUES (?, ?, ?)
        """, (entry.habit_id, entry.entry_date, entry.value))

        conn.commit()
        conn.close()

    def get_entries_by_habit(self, habit_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM habit_entries
            WHERE habit_id = ?
            ORDER BY entry_date
        """, (habit_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            HabitEntry(
                id=row[0],
                habit_id=row[1],
                entry_date=datetime.strptime(row[2], "%Y-%m-%d").date(),
                value=row[3]
            )
            for row in rows
        ]