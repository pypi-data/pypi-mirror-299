class NameCombiner:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self) -> str:
        """Returns the full name by combining first and last name."""
        return f"{self.first_name} {self.last_name}"