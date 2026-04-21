"""
Unit tests for streak analysis functions.

Covers longest streak and current streak calculations for daily and
weekly habits, including edge cases such as empty lists and broken
streaks.
"""

from analytics.analysis import (
    calculate_longest_streak,
    calculate_current_streak
)

from domain.habit_entry import HabitEntry
from datetime import date

from analytics.analysis import calculate_longest_streak
from domain.habit_entry import HabitEntry
from datetime import date


def test_longest_streak_daily():
    """Longest streak should count consecutive daily entries."""

    entries = [
        HabitEntry(None, 1, date(2024, 1, 1), 1),
        HabitEntry(None, 1, date(2024, 1, 2), 1),
        HabitEntry(None, 1, date(2024, 1, 3), 1)
    ]

    result = calculate_longest_streak(entries, "daily")

    assert result == 3

# Current streak should reflect the most recent consecutive days
def test_current_streak():

    entries = [
        HabitEntry(None, 1, date(2024, 1, 1), 1),
        HabitEntry(None, 1, date(2024, 1, 2), 1),
        HabitEntry(None, 1, date(2024, 1, 3), 1),
    ]

    result = calculate_current_streak(entries, "daily")

    assert result == 3

# Empty list → streak = 0
def test_empty_entries():

    entries = []

    result = calculate_longest_streak(entries, "daily")

    assert result == 0

# Non‑consecutive dates should break the streak
def test_broken_streak():

    entries = [
        HabitEntry(None, 1, date(2024, 1, 1), 1),
        HabitEntry(None, 1, date(2024, 1, 2), 1),
        HabitEntry(None, 1, date(2024, 1, 5), 1),
    ]

    result = calculate_longest_streak(entries, "daily")

    assert result == 2


def test_weekly_streak():
    """Weekly streak should count consecutive ISO week numbers."""
    entries = [
        HabitEntry(None, 1, date(2024, 1, 1), 1),
        HabitEntry(None, 1, date(2024, 1, 8), 1),
        HabitEntry(None, 1, date(2024, 1, 15), 1),
    ]

    result = calculate_longest_streak(entries, "weekly")

    assert result == 3


# Current streak should stop when a gap occurs
def test_current_streak_break():

    entries = [
        HabitEntry(None, 1, date(2024, 1, 1), 1),
        HabitEntry(None, 1, date(2024, 1, 2), 1),
        HabitEntry(None, 1, date(2024, 1, 4), 1),
    ]

    result = calculate_current_streak(entries, "daily")

    assert result == 1