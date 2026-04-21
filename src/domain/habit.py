from dataclasses import dataclass
from typing import Optional


from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    """
    Domain model representing a habit in the Habit Tracking Application.

    This class defines the core attributes and validation rules for a habit.
    A habit may be quantitative (requiring numeric values such as hours,
    kilometers, or liters) or binary (completed/not completed). The model
    also stores the maximum number of entries allowed per tracking period
    (daily or weekly), enabling the controller to enforce habit constraints.

    Attributes:
        id (Optional[int]): Unique identifier for the habit in the database.
        name (str): Human-readable name of the habit.
        frequency (str): Tracking frequency, e.g., "daily" or "weekly".
        is_quantitative (bool): Indicates whether the habit expects numeric
            values (True) or boolean completion values (False).
        max_entries_per_period (int): Maximum number of entries allowed in
            the defined period (e.g., 1 per day, 5 per week).
    """

    id: Optional[int]
    name: str
    frequency: str
    is_quantitative: bool
    max_entries_per_period: int

    def validate_value(self, value):
        """
        Validate that the provided value matches the habit type.

        Quantitative habits require an integer or float.
        Binary habits require a boolean value.

        Args:
            value: The value to validate.

        Raises:
            ValueError: If the value does not match the expected type.
        """
        # Quantitative habits expect numeric values
        if self.is_quantitative:
            if not isinstance(value, (int, float)):
                raise ValueError("Quantitative habit requires numeric value.")
        else:
            # Binary habits expect True/False
            if not isinstance(value, bool):
                raise ValueError("Binary habit requires True/False.")
