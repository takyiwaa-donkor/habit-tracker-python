## Habit Tracker — Python Console Application
A modular Python application for tracking daily habits, analysing streaks,
and generating performance reports using SQLite-backed persistent storage.

## Overview
The Habit Tracker helps users build consistency by recording daily behaviours and providing meaningful analytics such as streaks, weekly summaries, and leaderboards.
The system follows a clean, layered architecture and includes:

### A full test suite

### Documentation (Final Report, User Manual, Reflections)

### Four weeks of predefined test data

### A fully interactive CLI

This README provides a technical overview.
Full details are available in the Final Report and User Manual included in the repository.

## Key Features
### Predefined daily habits (Water Intake, Exercise, Sleep, Reading, Meditation)

### Record habit values with unit selection

### SQLite persistent storage

### Streak analytics:

#### Current streak

#### Longest streak

#### Minimum & average streaks

### Daily, weekly, and monthly reports

### ASCII progress bars with colour indicators

### Habit leaderboard

### Modular architecture (UI → Controller → Domain → Persistence → Analytics)

### Automated tests using pytest

## Project Architecture
habit_tracker/
│
├── .venv/               # Virtual environment (excluded from version control)
│
├── analytics/           # Streak calculations, reporting logic
│   └── analysis.py
│
├── application/         # Controllers & orchestration
│   ├── controller.py
│   └── exporter.py
│
├── docs/                # Final Report, User Manual, Reflections
│
├── domain/              # Core domain models
│   ├── habit.py
│   ├── habit_entry.py
│   └── period.py
│
├── persistence/         # Database + repository abstraction
│   ├── database.py
│   └── repository.py
│
├── screenshots/         # Images used in README and User Manual
│
├── unit_tests/          # Automated test suite
│   ├── test_habits.py
│   ├── test_repository.py
│   ├── test_analytics.py
│   └── test_streaks.py
│
├── architecture.puml    # UML diagram
├── config.py            # Configuration settings
├── database.py          # Legacy DB file (if still needed)
├── environment.yml      # Conda environment definition
├── .gitignore
├── habit.db             # SQLite database
├── habit_tracker.log    # Application logs
├── habit_tracker_auto_units.py
├── habits.db            # Additional SQLite database
├── main.py              # CLI entry point
├── pytest.ini           # Pytest configuration
├── README.md
└── requirements.txt


![Main Menu](screenshots/12_project_structure.png)

## Installation
Clone the repository:
https://github.com/takyiwaa-donkor/habit_tracker

### Install dependencies:
pip install -r requirements.txt

### Run the application:
python main.py

## Screenshots
### Main Menu
![Main Menu](screenshots/01_main%20menu.png)
### Habit List
![Main Menu](screenshots/02_view_habits.png)

## Recording Habits
Show how the user interacts with the app.

### Example: Meditation Entry
![Main Menu](screenshots/13_record_meditation.png)

### Example: Water Intake Entry 
![Main Menu](screenshots/14_record_water%20intake.png)

## Analytics and Streaks
### Longest Streak
![04_longest_streak.png](screenshots/04_longest_streak.png)

### Current Streak
![05_current_streak.png](screenshots/05_current_streak.png)

### Streak Statistics
![06_streak_stats.png](screenshots/06_streak_stats.png)

## Reports

### Daily Report
![08_daily_report.png](screenshots/08_daily_report.png)

### Weekly Report
![09_weekly_report.png](screenshots/09_weekly_report.png)

### Monthly Report
![10_monthly_report.png](screenshots/10_monthly_report.png)

### Habit Leaderboard
![11_habit_leaderboard.png](screenshots/11_habit_leaderboard.png)

## Testing

The project includes a full pytest suite covering:

- Habit creation, editing, deletion  
- Repository operations  
- Analytics functions (longest streak, current streak, statistics)  
- Streak calculations  
- Input validation  
- Dummy dataset validation  

### Run tests

To execute the full test suite, run:

### ```bash
pytest unit_tests

## unit_test

### Example Test Results
![15_test_results.png](screenshots/15_test_results.png)

## Documentation
The docs/ folder contains:

### Final Report — development process, system architecture, evaluation

### User Manual — step‑by‑step instructions for using the CLI

### Reflections — learning outcomes, challenges, and future improvements

These documents provide full context for academic assessment and portfolio review.

## Future Improvements
User-defined habits

### GUI (Tkinter / PyQt)

### Web version (Flask / FastAPI)

### Data visualisation charts

### Export to CSV/PDF

### Mobile app integration

## License
MIT License — created for educational purposes.
Author: Takyiwaa Donkor



























