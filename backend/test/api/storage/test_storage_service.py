import unittest
from unittest.mock import MagicMock, patch

from api.exceptions import (TableEmptyError, UserAlreadyExistsError,
                            UserNotFoundError)
from api.storage.models import Base, Client, Tutor, UserType
from api.storage.storage_service import StorageService
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists


class TestStorageService(unittest.TestCase):
    def setUp(self):
        """
        Prepare clean database state before each test
        Equivalence Partition: Test setup and database preparation
        """
        # Use an in-memory SQLite database for testing
        self.mock_engine = create_engine('sqlite:///:memory:', echo=False)
        
        # Patch the engine and database_exists method to avoid affecting production DB
        patch('api.storage.connection.engine', self.mock_engine).start()
        patch('sqlalchemy_utils.database_exists', MagicMock(return_value=False)).start()

        # Clear existing data before each test
        Base.metadata.create_all(self.mock_engine)  # Create tables in the mock database
        StorageService.init_db(self.mock_engine)  # Initialize the mock database

    def test_create_client_user_successful(self):
        """
        Equivalence Partition: Valid client user creation
        Boundary: First user creation with valid client parameters
        """
        user = StorageService.create_user(
            email="test_client@example.com",
            name="Test Client",
            password_hash="hashed_password",
            userType=UserType.CLIENT,
        )
        
        self.assertEqual(user.email, "test_client@example.com")
        self.assertEqual(user.name, "Test Client")
        self.assertIsInstance(user, Client)

    def test_create_tutor_user_successful(self):
        """
        Equivalence Partition: Valid tutor user creation
        Boundary: First user creation with valid tutor parameters
        """
        user = StorageService.create_user(
            email="test_tutor@example.com",
            name="Test Tutor",
            password_hash="hashed_password",
            userType=UserType.TUTOR
        )
        
        self.assertEqual(user.email, "test_tutor@example.com")
        self.assertEqual(user.name, "Test Tutor")
        self.assertIsInstance(user, Tutor)

    def test_create_user_duplicate_email(self):
        """
        Equivalence Partition: Duplicate user creation attempt
        Boundary: Attempting to create a user with an existing email
        """
        # First creation should succeed
        StorageService.create_user(
            email="duplicate@example.com",
            name="First User",
            password_hash="hashed_password",
            userType=UserType.CLIENT
        )
        
        # Second creation with same email should raise UserAlreadyExistsError
        with self.assertRaises(UserAlreadyExistsError):
            StorageService.create_user(
                email="duplicate@example.com",
                name="Second User",
                password_hash="another_hash",
                userType=UserType.CLIENT
            )

    def test_create_user_invalid_type(self):
        """
        Equivalence Partition: Invalid user type
        Boundary: Attempting to create user with unsupported user type
        """
        with self.assertRaises(ValueError):
            StorageService.create_user(
                email="invalid@example.com",
                name="Invalid User",
                password_hash="hashed_password",
                userType="invalid_type"
            )

    def test_find_one_user_exists(self):
        """
        Equivalence Partition: User exists
        Boundary: Finding a user by existing criteria
        """
        # First create a user
        created_user = StorageService.create_user(
            email="find@example.com",
            name="Find User",
            password_hash="hashed_password",
            userType=UserType.CLIENT
        )
        
        # Then find the user
        found_user = StorageService.find_one_user({"email": "find@example.com"})
        
        self.assertEqual(found_user.email, created_user.email)
        self.assertEqual(found_user.name, created_user.name)

    def test_find_one_user_not_found(self):
        """
        Equivalence Partition: User does not exist
        Boundary: Searching for a non-existent user
        """
        with self.assertRaises(UserNotFoundError):
            StorageService.find_one_user({"email": "nonexistent@example.com"})

    def test_find_one_user_empty_query(self):
        """
        Equivalence Partition: Empty query
        Boundary: Handling an empty query dictionary
        """
        with self.assertRaises(TableEmptyError):  # Assuming this is the expected behavior
            StorageService.find_one_user({})

if __name__ == '__main__':
    unittest.main()