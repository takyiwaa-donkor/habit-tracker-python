"""
Unit tests for enforcing entry limits in the Habit Tracking Application.

Verifies that the controller prevents users from recording more entries
than allowed within a habit's tracking period.
"""

import pytest
from application.controller import HabitController
from persistence.repository import Repository
from domain.habit import Habit


def test_entry_limit(controller):
    """A habit with a daily limit should allow only one entry per day."""
    repo: Repository = controller.repository

    # Create a habit that only allows ONE entry per day
    test_habit = Habit(
        id=None,
        name="Limit Test",
        frequency="daily",
        is_quantitative=True,   # <-- FIXED
        max_entries_per_period=1
    )

    # Insert habit into DB
    repo.add_habit(test_habit)

    # Reload habits to get the real DB ID
    habits = controller.list_habits()
    habit = next(h for h in habits if h.name == "Limit Test")

    # First entry → allowed
    controller.record_entry(habit.id, 1)

    # Second entry → MUST raise ValueError
    with pytest.raises(ValueError):
        controller.record_entry(habit.id, 1)
