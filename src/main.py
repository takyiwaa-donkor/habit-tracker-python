"""
Main CLI module for the Habit Tracking Application.

This module provides:
- The command-line interface
- Habit configuration
- Unit conversion utilities
- Reporting and analytics functions
- Streak calculations
- Leaderboard generation
- Integration with the SQLite database layer

All functions here interact with the persistence layer and present
results to the user through a text-based interface.
"""


from colorama import Fore, Style, init
init(autoreset=True)

from database import create_tables, add_record, get_records, get_records_by_habit

from datetime import date, timedelta

from database import create_tables, add_record, get_records, get_records_by_habit

from database import (
    create_tables,
    add_record,
    get_records,
    get_records_by_habit,
    get_records_today,
    get_records_last_7_days,
    get_records_last_30_days
)

# ==============================
# HABITS CONFIGURATION
# ==============================

habits = {
    1: {"name": "Water Intake", "frequency": "daily", "unit": "gallons", "options": ["gallons", "liters"]},
    2: {"name": "Exercise (Walking)", "frequency": "daily", "unit": "km", "options": ["km", "miles"]},
    3: {"name": "Sleep", "frequency": "daily", "unit": "hours", "options": ["hours", "minutes"]},
    4: {"name": "Reading", "frequency": "daily", "unit": "hours", "options": ["hours", "minutes"]},
    5: {"name": "Meditation", "frequency": "daily", "unit": "minutes", "options": ["minutes", "hours"]},
}

records = []

# ==============================
# UNIT CONVERSION
# ==============================

def convert_value(value, from_unit, to_unit):
    """
        Converts a numeric value from one unit to another.

        Args:
            value (float): The numeric value to convert.
            from_unit (str): The unit the value is currently in.
            to_unit (str): The unit to convert the value into.

        Returns:
            float: The converted value rounded to two decimals.
        """
    value = float(value)

    if from_unit == "gallons" and to_unit == "liters":
        return round(value * 3.785,2)

    if from_unit == "liters" and to_unit == "gallons":
        return round(value / 3.785,2)

    if from_unit == "km" and to_unit == "miles":
        return round(value * 0.621,2)

    if from_unit == "miles" and to_unit == "km":
        return round(value / 0.621,2)

    if from_unit == "hours" and to_unit == "minutes":
        return round(value * 60,2)

    if from_unit == "minutes" and to_unit == "hours":
        return round(value / 60,2)

    return value


# ==============================
# VIEW HABITS
# ==============================

def view_habits():
    """
        Displays all predefined habits with their IDs and frequency.

        This function prints a formatted table of all habits stored in the
        global habits dictionary.
        """
    print("\nID   Name                     Frequency")
    print("---------------------------------------------")

    for hid, info in habits.items():
        print(f"{hid:<5}{info['name']:<25}{info['frequency']}")

# ==============================
# RECORD HABIT
# ==============================

def record_habit():
    """
        Records a new habit entry.

        Workflow:
            - Displays available habits
            - Prompts user for habit ID
            - Validates unit selection
            - Prompts for value
            - Saves the record to the database

        Raises:
            ValueError: If the user enters an invalid habit ID or unit.
        """
    view_habits()

    habit_id = int(input("\nEnter habit ID: "))

    if habit_id not in habits:
        print("Invalid habit")
        return

    habit = habits[habit_id]

    print(f"Available units: {', '.join(habit['options'])}")

    unit = input("Choose unit: ").lower()

    while unit not in habit["options"]:
        print("Invalid unit")
        unit = input("Choose unit again: ").lower()

    value = float(input(f"Enter value ({unit}): "))

    # SAVE TO DATABASE
    add_record(habit_id, value, unit, date.today())

    print(f"Recorded: {habit['name']} = {value} {unit} on {date.today()}")

# ==============================
# VIEW ALL RECORDS
# ==============================

def view_records():
    """
        Displays all stored habit records.

        Retrieves all entries from the database and prints them in a
        readable format. If no records exist, a message is shown.
        """
    print("\nHabit Records")

    data = get_records()

    if not data:
        print("No records found")
        return

    for r in data:

        habit_id, value, unit, record_date = r

        name = habits[habit_id]["name"]

        print(name, value, unit, record_date)

# ==============================
# DAILY REPORT
# ==============================

def daily_report():
    """
        Generates a daily report showing which habits were completed today.

        A habit is considered completed if at least one entry exists for
        the current date.
        """
    print("\nDaily Report")
    print("-------------")

    data = get_records_today()

    completed = {habit_id for habit_id, d in data}

    for hid, habit in habits.items():

        status = "Completed" if hid in completed else "Not completed"

        print(f"{habit['name']:<15} {status}")

# ==============================
# WEEKLY REPORT
# ==============================

def weekly_report():
    """
        Generates a weekly report for the last 7 days.

        Displays:
            - Completion count for each habit
            - Percentage completion
            - A colored progress bar
        """
    print("\nWeekly Report")
    print("-------------")

    data = get_records_last_7_days()

    summary = {}

    for habit_id, record_date in data:

        if habit_id not in summary:
            summary[habit_id] = set()

        summary[habit_id].add(record_date)

    for hid, habit in habits.items():

        completed = len(summary.get(hid, []))

        percent = int((completed / 7) * 100)

        bar = progress_bar(percent)
        print(f"{habit['name']:<15} {bar} ({completed}/7)")


# ==============================
# MONTHLY REPORT
# ==============================

def monthly_report():
    """
        Generates a monthly report for the last 30 days.

        Displays:
            - Completion count for each habit
            - Percentage completion
            - A colored progress bar
        """
    print("\nMonthly Report")
    print("-------------")

    data = get_records_last_30_days()

    summary = {}

    for habit_id, record_date in data:

        if habit_id not in summary:
            summary[habit_id] = set()

        summary[habit_id].add(record_date)

    for hid, habit in habits.items():

        completed = len(summary.get(hid, []))

        percent = int((completed / 30) * 100)

        bar = progress_bar(percent)
        print(f"{habit['name']:<15} {bar} ({completed}/30)")

# ==============================
# HABIT LEADERBOARD
# ==============================

def habit_leaderboard():
    """
        Displays a leaderboard ranking habits by 30-day completion percentage.

        Habits with higher completion percentages appear at the top.
        """
    print("\nHabit Leaderboard")
    print("-----------------")

    data = get_records_last_30_days()

    summary = {}

    for habit_id, record_date in data:

        if habit_id not in summary:
            summary[habit_id] = set()

        summary[habit_id].add(record_date)

    leaderboard = []

    for hid, habit in habits.items():

        completed = len(summary.get(hid, []))

        percent = int((completed / 30) * 100)

        leaderboard.append((habit["name"], percent))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    rank = 1

    for name, percent in leaderboard:

        bar = progress_bar(percent)

        print(f"{rank}. {name:<15} {bar}")

        rank += 1

# ==============================
# LONGEST STREAK
# ==============================

def longest_streak(habit_id):
    """
        Calculates and prints the longest streak for a given habit.

        Args:
            habit_id (int): The ID of the habit.

        A streak is defined as consecutive days with recorded entries.
        """
    dates = get_records_by_habit(habit_id)

    dates = [date.fromisoformat(d) for d in dates]

    if not dates:
        print("No records")
        return

    longest = 1
    current = 1

    for i in range(1, len(dates)):

        if dates[i] == dates[i-1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)

        else:
            current = 1

    print("Longest streak:", longest)


# ==============================
# CURRENT STREAK
# ==============================

def current_streak(habit_id):
    """
        Calculates and prints the current streak for a given habit.

        Args:
            habit_id (int): The ID of the habit.

        The current streak counts backwards from today until a day is missing.
        """
    dates = get_records_by_habit(habit_id)

    dates = [date.fromisoformat(d) for d in dates]
    dates.sort(reverse=True)

    streak = 0
    expected = date.today()

    for d in dates:

        if d == expected:
            streak += 1
            expected -= timedelta(days=1)

        else:
            break

    print("Current streak:", streak)


# ==============================
# STREAK STATISTICS
# ==============================

def streak_statistics(habit_id):
    """
        Computes and prints streak statistics for a habit.

        Args:
            habit_id (int): The ID of the habit.

        Displays:
            - Maximum streak
            - Minimum streak
            - Average streak length
        """
    dates = get_records_by_habit(habit_id)

    dates = [date.fromisoformat(d) for d in dates]

    if not dates:
        print("No records")
        return

    streaks = []
    current = 1

    for i in range(1, len(dates)):

        if dates[i] == dates[i-1] + timedelta(days=1):
            current += 1
        else:
            streaks.append(current)
            current = 1

    streaks.append(current)

    print("Max streak:", max(streaks))
    print("Min streak:", min(streaks))
    print("Average streak:", round(sum(streaks) / len(streaks), 2))

# ==============================
# PROGRESS BAR
# ==============================

def progress_bar(percent):
    """
        Generates a colored progress bar based on a percentage value.

        Args:
            percent (int): Completion percentage (0–100).

        Returns:
            str: A formatted progress bar string with color coding.
        """
    bar_length = 20

    filled = int(bar_length * percent / 100)

    bar = "█" * filled + "░" * (bar_length - filled)

    if percent >= 80:
        color = Fore.GREEN
    elif percent >= 50:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    return f"{color}{bar}{Style.RESET_ALL} {percent}%"


# ==============================
# MAIN MENU
# ==============================

def main():
    """
        Entry point for the Habit Tracking Application.

        Displays the main menu, handles user input, and routes actions to
        the appropriate functions.
        """
    create_tables()  # initializes database

    while True:

        print("\n===============================")
        print("        HABIT TRACKER")
        print("===============================")

        print("1 View Habits")
        print("2 Record Habit")
        print("3 Longest Streak")
        print("4 Current Streak")
        print("5 Streak Statistics")
        print("6 View Records")
        print("7 Daily Report")
        print("8 Weekly Report")
        print("9 Monthly Report")
        print("10 Habit Leaderboard")
        print("11 Exit")

        choice = input("Select option: ")

        if choice == "1":
            view_habits()

        elif choice == "2":
            record_habit()

        elif choice == "3":

            view_habits()
            hid = int(input("Habit ID: "))
            longest_streak(hid)

        elif choice == "4":

            view_habits()
            hid = int(input("Habit ID: "))
            current_streak(hid)

        elif choice == "5":

            view_habits()
            hid = int(input("Habit ID: "))
            streak_statistics(hid)

        elif choice == "6":
            view_records()


        elif choice == "7":

            daily_report()


        elif choice == "8":

            weekly_report()


        elif choice == "9":

            monthly_report()



        elif choice == "10":

            habit_leaderboard()


        elif choice == "11":

            break


if __name__ == "__main__":
    main()