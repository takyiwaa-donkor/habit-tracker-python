"""
Unit tests for habit creation and entry‑limit behavior.
"""

import os
from persistence.database import initialize_database, DB_NAME
from persistence.repository import add_habit, get_all_habits
from domain.habit import Habit


def setup_module():
    """Reset the database before running tests."""
    # Delete database before test
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    initialize_database()


def test_add_habit():
    """A new habit should be inserted and retrievable."""
    habit = Habit(None, "Test Habit", "daily", False, 1)
    add_habit(habit)

    habits = get_all_habits()
    assert len(habits) == 1
    assert habits[0].name == "Test Habit"

    def test_entry_limit():
        """A habit with a daily limit should allow only one entry per day."""
        habit = Habit(None, "Limit Test", "daily", False, 1)
        add_habit(habit)

        habits = get_all_habits()
        h = habits[-1]

        from application.controller import HabitController
        controller = HabitController()
        # First entry → allowed
        controller.record_entry(h.id, True)

        try:
            controller.record_entry(h.id, True)
            assert False
        except ValueError:
            assert True

