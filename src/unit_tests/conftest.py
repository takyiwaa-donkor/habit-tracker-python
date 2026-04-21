import os
import pytest
from persistence.database import DB_PATH, get_connection
from persistence.repository import Repository
from application.controller import HabitController


@pytest.fixture
def controller(tmp_path, monkeypatch):
    """
        Provide a HabitController instance backed by a temporary test database.

        This fixture:
        - Redirects the database path to a temporary file
        - Creates fresh tables for habits and habit entries
        - Returns a controller using a clean Repository instance
        """
    # Redirect DB to a temporary file for each test
    test_db = tmp_path / "test.db"
    monkeypatch.setattr("persistence.database.DB_PATH", str(test_db))

    # Create empty tables
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            frequency TEXT,
            is_quantitative INTEGER,
            max_entries_per_period INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE habit_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            entry_date TEXT,
            value REAL
        )
    """)

    conn.commit()
    conn.close()

    repo = Repository()
    return HabitController(repo)
