import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from api.auth.auth_service import AuthService
from api.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt

class TestAuthService(unittest.TestCase):

    @patch('bcrypt.hashpw')
    def test_hash_password(self, mock_hashpw):
        # Mock bcrypt's hashpw method
        mock_hashpw.return_value = b"$2b$12$mockedhashvalue"

        password = "password123"
        hashed_password = AuthService.hash_password(password)

        # Check that bcrypt.hashpw was called with correct arguments
        mock_hashpw.assert_called_once_with(password.encode("utf-8"), MagicMock())
        self.assertEqual(hashed_password, "$2b$12$mockedhashvalue")

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

        data = {"user_id": 1, "role": "admin"}
        expires_delta = timedelta(minutes=30)
        token = AuthService.create_access_token(data, expires_delta)

        # Check if the mock was called correctly
        mock_encode.assert_called_once()
        self.assertEqual(token, "mocked_jwt_token")

        # Check that the token includes the expiration time
        to_encode = data.copy()
        expire_time = datetime.now() + expires_delta
        to_encode.update({"exp": expire_time})

    @patch('api.auth.auth_service.jwt.decode')
    def test_verify_token(self, mock_decode):
        # Mock the JWT decode
        mock_decode.return_value = {"user_id": 1, "role": "admin", "exp": datetime.now() + timedelta(minutes=30)}

        token = "mocked_jwt_token"
        payload = AuthService.verify_token(token)

        # Check if jwt.decode was called correctly
        mock_decode.assert_called_once_with(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        self.assertEqual(payload["user_id"], 1)
        self.assertEqual(payload["role"], "admin")

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

        data = {"user_id": 1, "role": "admin"}
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
