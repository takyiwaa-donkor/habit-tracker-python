"""
Simple demo script for manually testing habit recording.

This file prints example habit entries to show how the `add_habit`
function behaves. It does not interact with the main application
or database layer.
"""
def add_habit(habit, date):
    print("Habit:", habit)
    print("Date:", date)
    print("Output: Habit recorded successfully.")
    print("---------------------------")

# Demo test cases
print("Test Case 1")
add_habit("Study Python", "2026-03-01")

print("Test Case 2")
add_habit("Exercise", "2026-03-02")