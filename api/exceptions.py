class EmailAlreadyUsedError(Exception):
    """Exception raised when the email is already in use."""
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already in use.")
        self.email = email

class EmailNotFoundError(Exception):
    """Exception raised when the email is not found."""
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' not found.")
        self.email = email