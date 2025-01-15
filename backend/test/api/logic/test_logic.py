import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from api.auth.models import TokenData
from api.logic.logic import Logic
from api.router.models import LoginRequest, SignupRequest
from api.exceptions import UserAlreadyExistsError, UserNotFoundError
from api.storage.models import UserType
from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError
from pydantic import BaseModel

class UserStub(BaseModel):
    """
    Stub for Base User model with composite primary key of email and userType
    """
    email: str
    name: str
    userType: UserType
    password_hash: str

class TestLogic(unittest.TestCase):

    # Test Logic for Handle Login
    @patch('api.logic.logic.StorageService.find_one_user')
    @patch('api.auth.auth_service.AuthService.verify_password')
    @patch('api.auth.auth_service.AuthService.create_access_token')
    @patch('api.auth.auth_service.AuthService.create_refresh_token')
    def test_handle_login_valid_credentials(self, mock_create_refresh_token, mock_create_access_token, mock_verify_password, mock_find_one_user):
        # Arrange
        login_data = LoginRequest(email="test@example.com", password="valid_password", userType=UserType.CLIENT)
        # Return a UserStub instead of a dict
        mock_find_one_user.return_value = UserStub(
            email="test@example.com",
            name="Test User",
            userType=UserType.CLIENT,
            password_hash="hashed_password"
        )
        mock_verify_password.return_value = True
        mock_create_access_token.return_value = "valid_access_token"
        mock_create_refresh_token.return_value = "valid_refresh_token"
        
        # Act
        tokens = Logic.handle_login(login_data)

        # Assert
        self.assertEqual(tokens, {"access_token": "valid_access_token", "refresh_token": "valid_refresh_token"})
        mock_find_one_user.assert_called_once_with({"email": "test@example.com", "userType": UserType.CLIENT})
        mock_verify_password.assert_called_once_with("valid_password", "hashed_password")
        mock_create_access_token.assert_called_once()

    @patch('api.logic.logic.StorageService.find_one_user')
    @patch('api.auth.auth_service.AuthService.verify_password')
    def test_handle_login_invalid_credentials(self, mock_verify_password, mock_find_one_user):
        # Arrange
        login_data = LoginRequest(email="test@example.com", password="wrong_password", userType=UserType.CLIENT)
        mock_find_one_user.return_value = UserStub(
            email="test@example.com",
            name="Test User",
            userType=UserType.CLIENT,
            password_hash="hashed_password"
        )
        mock_verify_password.return_value = False  # Invalid password

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            Logic.handle_login(login_data)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Incorrect email or password")

    @patch('api.logic.logic.StorageService.find_one_user')
    def test_handle_login_user_not_found(self, mock_find_one_user):
        # Arrange
        login_data = LoginRequest(email="nonexistent@example.com", password="password", userType=UserType.CLIENT)
        mock_find_one_user.side_effect = UserNotFoundError(query={"email": "nonexistent@example.com", "userType": UserType.CLIENT})

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            Logic.handle_login(login_data)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Incorrect email or password")

    # Test Logic for Handle Signup
    @patch('api.logic.logic.StorageService.create_user')
    @patch('api.auth.auth_service.AuthService.hash_password')
    @patch('api.auth.auth_service.AuthService.create_access_token')
    @patch('api.auth.auth_service.AuthService.create_refresh_token')
    def test_handle_signup_new_user(self, mock_create_refresh_token, mock_create_access_token, mock_hash_password, mock_create_user):
        # Arrange
        signup_data = SignupRequest(email="newuser@example.com", password="secure_password", name="New User", userType=UserType.CLIENT)
        mock_hash_password.return_value = "hashed_password"
        mock_create_user.return_value = UserStub(
            email="newuser@example.com",
            name="New User",
            userType=UserType.CLIENT,
            password_hash="hashed_password"
        )
        mock_create_access_token.return_value = "valid_access_token"
        mock_create_refresh_token.return_value = "valid_refresh_token"

        # Act
        tokens = Logic.handle_signup(signup_data)

        # Assert
        self.assertEqual(tokens, {"access_token": "valid_access_token", "refresh_token": "valid_refresh_token"})
        mock_create_user.assert_called_once_with(
            email="newuser@example.com", name="New User", password_hash="hashed_password", userType=UserType.CLIENT
        )
        mock_hash_password.assert_called_once_with("secure_password")
        mock_create_access_token.assert_called_once()

    @patch('api.logic.logic.StorageService.create_user')
    @patch('api.auth.auth_service.AuthService.hash_password')
    def test_handle_signup_user_already_exists(self, mock_hash_password, mock_create_user):
        # Arrange
        signup_data = SignupRequest(email="existinguser@example.com", password="secure_password", name="Existing User", userType=UserType.CLIENT)
        mock_create_user.side_effect = UserAlreadyExistsError(email="existinguser@example.com", userType=UserType.CLIENT)

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            Logic.handle_signup(signup_data)
        self.assertEqual(context.exception.status_code, 400)  # 409 would be a better choice for conflict
        self.assertEqual(context.exception.detail, "User with email 'existinguser@example.com' and type 'UserType.CLIENT' already exists.")

    # Test Logic for Get Current User
    @patch('api.auth.auth_service.AuthService.verify_token')
    @patch('api.logic.logic.StorageService.find_one_user')
    def test_get_current_user_valid(self, mock_find_one_user, mock_verify_token):
        # Arrange
        token = "valid_token"
        mock_verify_token.return_value = TokenData(email="test@example.com", userType=UserType.CLIENT)
        mock_find_one_user.return_value = UserStub(
            email="test@example.com",
            name="Test User",
            userType=UserType.CLIENT,
            password_hash="hashed_password"
        )

        # Act
        user = Logic.get_current_user(token)

        # Assert
        self.assertEqual(user.email, "test@example.com")
        mock_find_one_user.assert_called_once_with({"email": "test@example.com", "userType": UserType.CLIENT})

    @patch('api.auth.auth_service.AuthService.verify_token')
    def test_get_current_user_invalid_token(self, mock_verify_token):
        # Arrange
        token = "invalid_token"
        mock_verify_token.side_effect = JWTError("Invalid token")

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            Logic.get_current_user(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

if __name__ == '__main__':
    unittest.main()
