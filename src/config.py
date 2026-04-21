"""
Configure global logging for the Habit Tracking Application.

Sets the log file, logging level, and message format used across the app.
"""
import logging

logging.basicConfig(
    filename="habit_tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)