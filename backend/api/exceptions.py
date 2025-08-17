class TableEmptyError(Exception):
    """Exception raised when the table is empty."""

    def __init__(self, table: str):
        super().__init__(f"Table '{table}' is empty.")


class UserNotFoundError(Exception):
    """Exception raised when the user with a certain email and a specific type is not found."""

    def __init__(self, query: dict, userType: str):
        super().__init__(f"{userType} with the following details not found: {query}")


class UserAlreadyExistsError(Exception):
    """Exception raised when the user with a certain email and a specific type already exists."""

    def __init__(self, email: str, userType: str):
        super().__init__(
            f"User with email '{email}' and type '{userType}' already exists."
        )
        self.email = email
        self.userType = userType
