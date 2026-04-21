"""
Unit tests for longest‑streak and current‑streak calculations.
"""
from datetime import datetime
from domain.habit_entry import HabitEntry
from analytics.analysis import calculate_longest_streak, calculate_current_streak


def make_entries(date_strings):
    """Convert a list of YYYY‑MM‑DD strings into HabitEntry objects."""
    entries = []
    for d in date_strings:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        entries.append(HabitEntry(id=None, habit_id=1, entry_date=dt, value=1))
    return entries


def test_longest_streak_simple():
    """Three consecutive days → longest streak = 3."""
    entries = make_entries(["2026-03-01", "2026-03-02", "2026-03-03"])
    assert calculate_longest_streak(entries, "daily") == 3


def test_longest_streak_with_gap():
    """Gap breaks streak → longest streak = 2."""
    entries = make_entries(["2026-03-01", "2026-03-02", "2026-03-04"])
    assert calculate_longest_streak(entries, "daily") == 2


def test_current_streak_active():
    """Current streak should count most recent consecutive days."""
    entries = make_entries(["2026-03-01", "2026-03-02", "2026-03-03"])
    assert calculate_current_streak(entries, "daily") == 3


def test_current_streak_broken():
    """Gap before last date → current streak = 1."""
    entries = make_entries(["2026-03-01", "2026-03-02", "2026-03-05"])
    assert calculate_current_streak(entries, "daily") == 1
