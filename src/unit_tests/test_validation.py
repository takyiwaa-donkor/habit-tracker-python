"""
Unit tests for validating habit value rules.
"""

from domain.habit import Habit
import pytest

def test_invalid_quantitative_value():
    """Quantitative habits should reject non‑numeric values."""
    habit = Habit(None, "Water", "daily", True, 5)

    with pytest.raises(ValueError):
        habit.validate_value("invalid")