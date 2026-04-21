from datetime import date


class Period:
    """
        Represents a tracking period for a habit (daily or weekly).

    Attributes:
        reference_date (date): Date used to determine the period.
        frequency (str): Either "daily" or "weekly".
        """

    def __init__(self, reference_date: date, frequency: str):
        self.reference_date = reference_date
        self.frequency = frequency

    def key(self):
        """
               Return the period identifier:
               - Daily habits → the exact date
               - Weekly habits → ISO week number
               """
        if self.frequency == "daily":
            return self.reference_date
        elif self.frequency == "weekly":
            return self.reference_date.isocalendar()[1]