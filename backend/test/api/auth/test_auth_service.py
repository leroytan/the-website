import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from api.auth.auth_service import AuthService
from api.auth.auth_service import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from jose import jwt
import bcrypt

from api.auth.models import TokenData
# UserType is not defined in current models

class TestAuthService(unittest.TestCase):

    @patch('bcrypt.gensalt')  # Mock the gensalt function in bcrypt
    def test_hash_password(self, mock_gensalt):
        # Arrange: Set up the mock to return a fixed salt
        mock_gensalt.return_value = b'$2b$12$8t8fdznCd8IfgnqkIMZq.e'  # Example mock salt
        
        password = "test_password"
        
        # Act: Call the hash_password method
        hashed_password = AuthService.hash_password(password)
        
        # Assert: Check if the result is what you expect
        # We know the salt is fixed, so the hashed password should include this fixed salt and a hash of the password
        expected_hash = bcrypt.hashpw(password.encode("utf-8"), mock_gensalt.return_value).decode()
        
        self.assertEqual(hashed_password, expected_hash)
        mock_gensalt.assert_called_once()  # Ensure gensalt was called once

    @patch('bcrypt.checkpw')
    def test_verify_password(self, mock_checkpw):
        # Mock bcrypt's checkpw method
        mock_checkpw.return_value = True

        plain_password = "password123"
        hashed_password = "$2b$12$mockedhashvalue"
        result = AuthService.verify_password(plain_password, hashed_password)

        # Check that bcrypt.checkpw was called with correct arguments
        mock_checkpw.assert_called_once_with(plain_password.encode(), hashed_password.encode())
        self.assertTrue(result)

        # Test incorrect password
        mock_checkpw.return_value = False
        result = AuthService.verify_password(plain_password, "wronghash")
        self.assertFalse(result)

    @patch('api.auth.auth_service.jwt.encode')
    def test_create_access_token(self, mock_encode):
        # Mock the JWT encoding
        mock_encode.return_value = "mocked_jwt_token"

        data = TokenData(email="user@example.com")
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = AuthService.create_access_token(data, expires_delta)

        # Check if the mock was called correctly
        mock_encode.assert_called_once()
        self.assertEqual(token, "mocked_jwt_token")

    @patch('api.auth.auth_service.jwt.encode')
    def test_create_refresh_token(self, mock_encode):
        # Mock the JWT encoding
        mock_encode.return_value = "mocked_jwt_token"

        data = TokenData(email="user@example.com")
        expires_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        token = AuthService.create_refresh_token(data, expires_delta)

        # Check if the mock was called once
        mock_encode.assert_called_once()
        self.assertEqual(token, "mocked_jwt_token")

    @patch('api.auth.auth_service.jwt.decode')
    def test_verify_token(self, mock_decode):
        # Mock the JWT decode
        mock_decode.return_value = {'email': 'user@example.com', 'exp': datetime.now() + timedelta(minutes=5), 'type': 'access'}

        token = "mocked_jwt_token"
        token_data = AuthService.verify_token(token)

        # Check if jwt.decode was called correctly
        mock_decode.assert_called_once_with(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        self.assertEqual(token_data.email, "user@example.com")

        # Test invalid token (JWT decoding fails)
        mock_decode.side_effect = jwt.ExpiredSignatureError("token has expired")
        with self.assertRaises(jwt.ExpiredSignatureError):
            AuthService.verify_token(token)

    @patch('bcrypt.hashpw')
    def test_hash_password_empty(self, mock_hashpw):
        # Edge case: empty password
        password = ""
        with self.assertRaises(ValueError):
            AuthService.hash_password(password)

    @patch('bcrypt.checkpw')
    def test_verify_password_empty(self, mock_checkpw):
        # Edge case: empty plain or hashed password
        with self.assertRaises(ValueError):
            AuthService.verify_password("", "")

    @patch('api.auth.auth_service.jwt.encode')
    def test_create_access_token_no_expiration(self, mock_encode):
        # Test the create_access_token method with default expiration time
        mock_encode.return_value = "mocked_jwt_token"

        data = TokenData(email="user@example.com")
        token = AuthService.create_access_token(data)

        mock_encode.assert_called_once()
        self.assertEqual(token, "mocked_jwt_token")

    @patch('api.auth.auth_service.jwt.encode')
    def test_create_access_token_invalid_data(self, mock_encode):
        # Edge case: Invalid data input (empty data dictionary)
        data = {}
        with self.assertRaises(ValueError):
            AuthService.create_access_token(data)
            

if __name__ == '__main__':
    unittest.main()
