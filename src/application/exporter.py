"""
Exporter module for the Habit Tracking Application.

This module provides functionality for exporting habit data, analytics,
and reports into external formats. It acts as a utility layer that
retrieves data from the controller or repository and transforms it into
structured output suitable for saving, sharing, or external analysis.

Responsibilities:
    - Exporting habit lists, entries, and streak statistics
    - Generating formatted output (e.g., CSV, JSON, text summaries)
    - Preparing analytics data for external reporting tools
    - Ensuring consistent formatting across all exported files
    - Supporting integration with future UI or reporting extensions

The exporter isolates all output-related logic from the core application,
making the system easier to maintain, extend, and integrate with other
tools or platforms.
"""

import csv
from persistence.repository import get_all_habits


def export_habits_to_csv(filename="habits_export.csv"):
    habits = get_all_habits()

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Frequency"])

        for habit in habits:
            writer.writerow([habit.id, habit.name, habit.frequency])