from abc import ABC, abstractmethod
from api.storage.models import User

class StorageInterface(ABC):

    @classmethod
    @abstractmethod
    def find_one_user(cls, query: dict) -> User:
        """
        Finds a single user that matches the provided query.

        Args:
            query (dict): The query to match the user against.

        Returns:
            dict: The user data as a dictionary.
        """
        pass

    @classmethod
    @abstractmethod
    def create_user(cls, email: str, name: str, password_hash: str, userType: str) -> User:
        """
        Creates a new user with the provided data.

        Args:
            email (str): The user's email.
            name (str): The user's name.
            password_hash (str): The hashed password.
            userType (str): The user's type.

        Returns:
            User: The newly created user data as a dictionary.
        """
        pass

