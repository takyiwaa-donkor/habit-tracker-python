**Overview**
This Habit Tracking Application enables users to record recurring behaviours such as Water Intake, Exercise, Sleep, Reading, and Meditation.
The system evolved from a simple CLI tracker into a fully functional analytics platform with persistent storage, streak calculations, and detailed reporting.

The architecture is built around:

- Layered modular design

- SQLite persistence

- Object‑oriented domain modelling

- Functional analytics

- Extensive testing (pytest + manual)

The project was developed across three phases: Conception → Implementation → Finalization, each documented in detail.

**Key Features**
Habit Management
- Predefined habits with configurable units (liters, hours, minutes, etc.)

- Daily and weekly tracking

- Multiple entries per day for quantitative habits

- Validation for numeric and binary habits

Analytics Engine
- longest_streak()

- current_streak()

- streak_statistics()

- daily_report()

- weekly_report()

- monthly_report()

- habit_leaderboard()

Data Persistence
- SQLite database (habit.db)

- Transactional integrity

- Efficient querying for streaks and reports

- Repository pattern for clean data access

CLI Interface
- 11‑option interactive menu

- Clear navigation and input validation

- Real‑time analytics and reporting

**System Architecture**
The application follows a strict layered architecture:

Presentation Layer (CLI)
    ↓
Controller Layer (HabitController)
    ↓
Domain Layer (Habit, HabitEntry)
    ↓
Analytics Layer (analysis.py)
    ↓
Persistence Layer (repository.py, database.py)
    ↓
SQLite Database (habit.db)

Why this architecture?
- Clear separation of concerns

- Easy to extend (GUI, web app, mobile app)

- Independent testing of each layer

- No circular dependencies

- Scalable for long‑term data growth

**Data Model**
Core Entities
- Habit → static definition (name, frequency, validation rules)

- HabitEntry → time‑specific record (value, unit, timestamp)

This one‑to‑many structure ensures:

- Normalized data

- Efficient historical queries

- Accurate streak calculations

Storage
SQLite chosen for:

- zero‑configuration setup

- full SQL support

- transactional integrity

- seamless Python integration

**Analytics and Reporting**
The system provides a full analytics suite:

- Longest streak

- Current streak

- Max/min/average streak

- Daily completion report

- Weekly performance summary

- Monthly trend analysis

- Habit leaderboard

Dummy data covering 30+ days was generated to validate analytics and ensure realistic performance.

**Testing**
Testing included:

- Automated tests (pytest)

- Manual CLI testing

- Database read/write validation

- Edge case handling:

   - skipped days

   - overlapping entries

   - multi‑entry habits

   - invalid input

All analytics functions were implemented, tested, and integrated successfully.

**How to Run the Application**
Install Python 3.10+

Navigate to the project folder:

Code
cd habit_tracker
Run the application:

Code
python main.py
SQLite initializes automatically on first run.

**Repository Structure**
habit-tracker/
│
├── main.py
├── cli.py
├── controller.py
├── database.py
├── repository.py
├── models/
│   ├── habit.py
│   └── habit_entry.py
├── analytics/
│   └── analysis.py
├── data/
│   └── habit.db
├── tests/
│   └── test_cases.py
└── docs/
    ├── HabitTracker_Abstract.pdf
    ├── HabitTracker_Phase1.pdf
    ├── HabitTracker_Phase2.pdf
    ├── HabitTracker_FinalReport.pdf
    └── HabitTracker_UserManual.pdf
    
**Progress vs Original Plan**
Planned (Phase 1):

Simple CLI tracker

Basic habit recording

No persistence

Achieved (Final Version):

Full SQLite integration

Modular multi‑layer architecture

Complete analytics engine

Daily/weekly/monthly reports

Leaderboard + streak statistics

Robust input validation

Extensive testing

The system grew far beyond the initial concept, becoming a scalable productivity tool.

**Future Improvements**
Graphical User Interface (GUI)

User‑defined habits

Data visualization (charts, graphs)

Mobile or web version

Notification reminders

Cloud synchronization
