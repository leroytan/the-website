from abc import ABC, abstractmethod

from api.storage.models import User


class StorageInterface(ABC):

    @staticmethod
    @abstractmethod
    def init_db(engine) -> None:
        """
        Initializes the database.
        """
        pass

    @staticmethod
    @abstractmethod
    def find_one_user(query: dict) -> User:
        """
        Finds a single user that matches the provided query.

        Args:
            query (dict): The query to match the user against.

        Returns:
            dict: The user data as a dictionary.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_user(email: str, name: str, password_hash: str, userType: str) -> User:
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

