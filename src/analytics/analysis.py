"""
Analytics Module

This module contains pure analytical functions used to analyse habit data.
These functions do not interact with the database directly and operate only
on provided data structures.

Implemented analytics:
- Longest streak calculation
- Current streak calculation
- Shortest streak calculation
- Average streak calculation
- Active habits detection
- Habit performance aggregation
"""

from datetime import date


def _group_by_period(entries, frequency):
    """
    Groups entries by logical period.

    Daily frequency → group by date
    Weekly frequency → group by ISO week number
    """

    periods = []

    for entry in entries:
        if frequency == "daily":
            key = entry.entry_date

        elif frequency == "weekly":
            iso = entry.entry_date.isocalendar()
            key = (iso.year, iso.week)

        else:
            raise ValueError("Invalid frequency")

        if key not in periods:
            periods.append(key)

    return sorted(periods)


# --------------------------------------------------
# Longest Streak
# --------------------------------------------------

def calculate_longest_streak(entries, frequency="daily"):
    """
    Calculates the longest consecutive streak of habit entries.
    """

    if not entries:
        return 0

    periods = _group_by_period(entries, frequency)

    streak = 1
    longest = 1

    for i in range(1, len(periods)):

        if frequency == "daily":
            delta = (periods[i] - periods[i - 1]).days
            consecutive = delta == 1

        else:  # weekly
            prev_year, prev_week = periods[i - 1]
            curr_year, curr_week = periods[i]

            consecutive = (
                (curr_year == prev_year and curr_week == prev_week + 1)
                or
                (curr_year == prev_year + 1 and prev_week >= 52 and curr_week == 1)
            )

        if consecutive:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

    return longest


# --------------------------------------------------
# Current Streak
# --------------------------------------------------

def calculate_current_streak(entries, frequency="daily"):
    """
    Calculates the current active streak.
    """

    if not entries:
        return 0

    periods = _group_by_period(entries, frequency)

    streak = 1

    for i in range(len(periods) - 1, 0, -1):

        if frequency == "daily":
            delta = (periods[i] - periods[i - 1]).days
            consecutive = delta == 1

        else:
            prev_year, prev_week = periods[i - 1]
            curr_year, curr_week = periods[i]

            consecutive = (
                (curr_year == prev_year and curr_week == prev_week + 1)
                or
                (curr_year == prev_year + 1 and prev_week >= 52 and curr_week == 1)
            )

        if consecutive:
            streak += 1
        else:
            break

    return streak


# --------------------------------------------------
# Shortest Streak
# --------------------------------------------------

def calculate_shortest_streak(streaks):
    """
    Returns the shortest streak from a list of streak lengths.
    """

    if not streaks:
        return 0

    return min(streaks)


# --------------------------------------------------
# Average Streak
# --------------------------------------------------

def calculate_average_streak(streaks):
    """
    Calculates the average streak length.
    """

    if not streaks:
        return 0

    return sum(streaks) / len(streaks)


# --------------------------------------------------
# Active Habits
# --------------------------------------------------

def get_current_active_habits(habits, entries_by_habit):
    """
    Returns habits that currently have at least one entry.
    """

    active = []

    for habit in habits:
        if entries_by_habit.get(habit.id):
            active.append(habit)

    return active


# --------------------------------------------------
# Performance Aggregation
# --------------------------------------------------

def aggregate_habit_performance(entries):
    """
    Aggregates habit performance metrics.
    """

    if not entries:
        return {
            "total_entries": 0,
            "average_value": 0
        }

    total_entries = len(entries)
    total_value = sum(e.value for e in entries)

    return {
        "total_entries": total_entries,
        "average_value": total_value / total_entries
    }