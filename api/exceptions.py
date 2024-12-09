class UserNotFoundError(Exception):
    """Exception raised when the user with a certain email and a specific type is not found."""
    def __init__(self, email: str, userType: str):
        super().__init__(f"User with email '{email}' and type '{userType}' not found.")
        self.email = email
        self.userType = userType

class UserAlreadyExistsError(Exception):
    """Exception raised when the user with a certain email and a specific type already exists."""
    def __init__(self, email: str, userType: str):
        super().__init__(f"User with email '{email}' and type '{userType}' not found.")
        self.email = email
        self.userType = userType