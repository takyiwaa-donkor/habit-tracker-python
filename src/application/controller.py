"""
Controller module for the Habit Tracking Application.

This module defines the HabitController class, which acts as the
intermediate layer between the user interface (CLI or UI layer),
the domain models, and the persistence layer (repository).

Responsibilities:
    - Initializing predefined habits when the database is empty
    - Retrieving all habits from the repository
    - Validating and recording new habit entries
    - Enforcing entry limits based on habit frequency (daily/weekly)
    - Delegating streak calculations to the analytics module
    - Providing access to habit entries for reporting and analysis
    - Generating dummy data for testing and demonstration

The controller ensures that business rules are applied consistently
and that the application logic remains separate from storage and
presentation concerns.
"""

from datetime import date, timedelta
import logging

from domain.habit import Habit
from domain.habit_entry import HabitEntry
from analytics.analysis import calculate_longest_streak


class HabitController:
    """
        Controller class responsible for managing habit operations.

        This class acts as the business logic layer between the user interface
        and the persistence layer. It coordinates habit creation, validation,
        entry recording, streak calculations, and data retrieval.

        Responsibilities:
            - Initialize predefined habits when the database is empty
            - Retrieve all habits from the repository
            - Validate and record new habit entries
            - Enforce daily or weekly entry limits
            - Delegate streak calculations to the analytics module
            - Provide access to habit entries for reporting
            - Generate dummy data for testing and demonstration

        The controller ensures that all habit-related rules and constraints
        are applied consistently across the application.
        """

    def __init__(self, repository):
        self.repository = repository

        # Create predefined habits only if database is empty
        existing = {h.name for h in self.repository.get_all_habits()}

        predefined = [
            # Daily
            Habit(None, "Water Intake", "daily", True, 5),
            Habit(None, "Exercise (Walking)", "daily", True, 1),
            Habit(None, "Sleep", "daily", True, 1),
            Habit(None, "Reading", "daily", True, 1),
            Habit(None, "Meditation", "daily", True, 3),

            # Weekly
            Habit(None, "Water Intake", "weekly", True, 7),
            Habit(None, "Exercise (Walking)", "weekly", True, 5),
            Habit(None, "Sleep", "weekly", True, 7),
            Habit(None, "Reading", "weekly", True, 7),
            Habit(None, "Meditation", "weekly", True, 5),
        ]

        for habit in predefined:
            if habit.name not in existing:
                self.repository.add_habit(habit)

    # -------------------------

    def list_habits(self):
        return self.repository.get_all_habits()

    # -------------------------

    def record_entry(self, habit_id, value):
        habits = self.repository.get_all_habits()
        habit = next((h for h in habits if h.id == habit_id), None)

        if not habit:
            raise ValueError("Habit ID not found.")

        habit.validate_value(value)

        today = date.today()
        entries = self.repository.get_entries_by_habit(habit_id)

        # Count entries in current period
        if habit.frequency == "daily":
            count = sum(1 for e in entries if e.entry_date == today)
        else:
            count = sum(
                1 for e in entries
                if e.entry_date.isocalendar()[1] == today.isocalendar()[1]
            )

        if count >= habit.max_entries_per_period:
            raise ValueError("Entry limit reached for this period.")

        entry = HabitEntry(None, habit_id, today, value)
        self.repository.add_habit_entry(entry)

        logging.info("Entry recorded for habit ID %s", habit_id)

    # -------------------------

    def get_longest_streak(self, habit_id):
        habits = self.repository.get_all_habits()
        habit = next((h for h in habits if h.id == habit_id), None)

        if not habit:
            raise ValueError("Habit ID not found.")

        entries = self.repository.get_entries_by_habit(habit_id)
        return calculate_longest_streak(entries, habit.frequency)

    def get_current_streak(self, habit_id):

        habits = self.repository.get_all_habits()

        habit = next((h for h in habits if h.id == habit_id), None)

        if habit is None:
            raise ValueError("Habit ID not found.")

        entries = self.repository.get_entries_by_habit(habit_id)

        from analytics.analysis import calculate_current_streak

        return calculate_current_streak(entries, habit.frequency)

    def get_entries_by_habit(self, habit_id):

        habits = self.repository.get_all_habits()

        habit = next((h for h in habits if h.id == habit_id), None)

        if habit is None:
            raise ValueError("Habit ID not found.")

        return self.repository.get_entries_by_habit(habit_id)

    from datetime import date, timedelta
    from domain.habit_entry import HabitEntry

    def generate_dummy_data(self, weeks=4):

        habits = self.repository.get_all_habits()

        for habit in habits:

            for i in range(weeks * 7):
                entry_date = date.today() - timedelta(days=i)

                entry = HabitEntry(None, habit.id, entry_date, 1)

                self.repository.add_habit_entry(entry)


