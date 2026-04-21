from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class HabitEntry:
    """
       Represents a single recorded entry for a habit.

    Attributes:
        id (Optional[int]): Database identifier.
        habit_id (int): ID of the related habit.
        entry_date (date): Date when the entry was recorded.
        value (float): Recorded value (1.0 for binary habits).
       """
    id: Optional[int]
    habit_id: int
    entry_date: date
    value: float