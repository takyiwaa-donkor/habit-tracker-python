"""
Habit Tracker (Auto‑Unit Version)

This module implements a self-contained habit tracking system that supports
dynamic unit selection, automatic unit conversion, streak calculations, and
performance analytics without relying on an external database.

Key Features:
    - Predefined habits with multiple allowed units (e.g., gallons/liters,
      km/miles, hours/minutes)
    - Automatic conversion of all past records when the user selects a new unit
    - Recording of habit entries with both displayed and base values
    - Longest streak and current streak calculations based on recorded dates
    - Performance analytics showing completion rate over time
    - In‑memory record storage for simplified testing and demonstration
    - Interactive command-line interface for viewing habits, recording entries,
      generating streaks, and listing all records

This module is designed as a lightweight alternative to the full database-backed
habit tracker, focusing on unit flexibility and simplified data handling.
"""

# habit_tracker_final.py

from datetime import date, timedelta

# === Habits with meaningful units ===
habits = {
    1: {"name": "Water Intake", "frequency": "daily", "unit": "gallons", "options": ["gallons", "liters"]},
    2: {"name": "Exercise (Walking)", "frequency": "daily", "unit": "km", "options": ["km", "miles"]},
    3: {"name": "Sleep", "frequency": "daily", "unit": "hours", "options": ["hours", "minutes"]},
    4: {"name": "Reading", "frequency": "daily", "unit": "hours", "options": ["hours", "minutes"]},
    5: {"name": "Meditation", "frequency": "daily", "unit": "minutes", "options": ["minutes", "hours"]},
}

# === Store all habit records ===
records = []

# === Conversion function ===
def convert_value(value, from_unit, to_unit):
    try:
        value = float(value)
    except ValueError:
        return value
    # Water Intake
    if from_unit == "gallons" and to_unit == "liters":
        return round(value * 3.78541, 2)
    if from_unit == "liters" and to_unit == "gallons":
        return round(value / 3.78541, 2)
    # Walking
    if from_unit == "km" and to_unit == "miles":
        return round(value * 0.621371, 2)
    if from_unit == "miles" and to_unit == "km":
        return round(value / 0.621371, 2)
    # Sleep & Meditation & Reading
    if from_unit == "hours" and to_unit == "minutes":
        return round(value * 60, 2)
    if from_unit == "minutes" and to_unit == "hours":
        return round(value / 60, 2)
    return value

# === Convert all past records to new unit ===
def convert_all_records(habit_id, new_unit):
    habit_info = habits[habit_id]
    for record in records:
        if record["habit_id"] == habit_id:
            record["value"] = convert_value(record["base_value"], habit_info["unit"], new_unit)
            record["unit"] = new_unit

# === View habits ===
def view_habits():
    print("\nID   Name                     Frequency")
    print("---------------------------------------------")
    for hid, info in habits.items():
        print(f"{hid:<5}{info['name']:<25}{info['frequency']}")

# === View all records ===
def view_records():
    print("\nHabit Records:")
    print("Habit Name               Value    Unit    Date")
    print("-----------------------------------------------")
    for record in records:
        habit_name = habits[record["habit_id"]]["name"]
        print(f"{habit_name:<25}{record['value']:<8}{record['unit']:<8}{record['date']}")

# === Record habit (always ask for unit, store date) ===
def record_habit():
    view_habits()
    try:
        habit_id = int(input("\nEnter habit ID: "))
        if habit_id not in habits:
            print("Invalid habit ID.")
            return

        habit_info = habits[habit_id]

        # Always ask unit
        print(f"Available units for {habit_info['name']}: {', '.join(habit_info['options'])}")
        user_unit = input(f"Choose unit [{habit_info['unit']}]: ").strip().lower()
        while user_unit not in habit_info["options"]:
            print(f"Invalid unit. Please choose from: {', '.join(habit_info['options'])}")
            user_unit = input(f"Choose unit [{habit_info['unit']}]: ").strip().lower()

        # Convert all past records to this new unit
        convert_all_records(habit_id, user_unit)

        # Enter value in chosen unit
        value = input(f"Enter value ({user_unit}): ")
        converted_value = convert_value(value, habit_info["unit"], user_unit)

        # Store record with base_value and date
        records.append({
            "habit_id": habit_id,
            "value": converted_value,
            "unit": user_unit,
            "base_value": convert_value(converted_value, user_unit, habit_info["unit"]),
            "date": date.today()
        })

        print(f"Recorded: {habit_info['name']} = {converted_value} {user_unit} on {date.today()}")

    except ValueError:
        print("Please enter a valid number for habit ID.")

# === Longest streak calculation ===
def show_longest_streak(habit_id):
    habit_records = [r for r in records if r["habit_id"] == habit_id]
    if not habit_records:
        print("No records yet.")
        return

    sorted_dates = sorted({r["date"] for r in habit_records})
    longest_streak = 1
    current_streak = 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] == sorted_dates[i-1] + timedelta(days=1):
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 1
    print(f"Longest streak for {habits[habit_id]['name']}: {longest_streak} day(s)")

# === Current streak calculation ===
def show_current_streak(habit_id):
    habit_records = [r for r in records if r["habit_id"] == habit_id]
    if not habit_records:
        print("No records yet.")
        return

    sorted_dates = sorted({r["date"] for r in habit_records}, reverse=True)
    streak = 0
    today = date.today()
    expected_date = today
    for d in sorted_dates:
        if d == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
    print(f"Current streak for {habits[habit_id]['name']}: {streak} day(s)")

# === Habit performance (completion rate) ===
def show_habit_performance(habit_id):
    habit_records = [r for r in records if r["habit_id"] == habit_id]
    if not habit_records:
        print("No records yet.")
        return

    earliest = min(r["date"] for r in habit_records)
    days_passed = (date.today() - earliest).days + 1
    completion_rate = len(habit_records) / days_passed * 100
    print(f"Performance for {habits[habit_id]['name']}: {completion_rate:.2f}%")

# === Main menu ===
def main():
    while True:
        print("\n===================================")
        print("         HABIT TRACKER")
        print("===================================")
        print("1. View Habits")
        print("2. Record Habit")
        print("3. Show Longest Streak")
        print("4. Show Current Streak")
        print("5. Show Habit Performance Streak")
        print("6. Generate Dummy Data")
        print("7. View All Records")
        print("8. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            view_habits()
        elif choice == "2":
            record_habit()
        elif choice in ["3","4","5"]:
            view_habits()
            try:
                hid = int(input("\nEnter habit ID: "))
                if hid not in habits:
                    print("Invalid habit ID.")
                    continue
                if choice == "3":
                    show_longest_streak(hid)
                elif choice == "4":
                    show_current_streak(hid)
                elif choice == "5":
                    show_habit_performance(hid)
            except ValueError:
                print("Please enter a valid number for habit ID.")
        elif choice == "7":
            view_records()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Option not implemented yet.")

if __name__ == "__main__":
    main()