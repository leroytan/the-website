import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone

from api.auth.auth_service import AuthService
from api.auth.models import TokenData
from api.logic.logic import Logic
from api.router.models import EmailConfirmationRequest, SignupRequest
from api.storage.models import User
from fastapi import HTTPException


class TestEmailConfirmation(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_email = "test@example.org"
        self.test_name = "Test User"
        self.test_password = "testpassword123"
        
    def test_create_email_confirmation_token(self):
        """Test creating email confirmation token"""
        token_data = TokenData(email=self.test_email)
        token = AuthService.create_email_confirmation_token(token_data)
        
        # Verify token can be decoded
        decoded_data = AuthService.verify_email_confirmation_token(token)
        self.assertEqual(decoded_data.email, self.test_email)
        
    def test_verify_email_confirmation_token_invalid_type(self):
        """Test that invalid token type raises error"""
        # Create a password reset token instead of email confirmation
        token_data = TokenData(email=self.test_email)
        token = AuthService.create_password_reset_token(token_data)
        
        with self.assertRaises(ValueError):
            AuthService.verify_email_confirmation_token(token)
            
    def test_verify_email_confirmation_token_expired(self):
        """Test that expired token raises error"""
        token_data = TokenData(email=self.test_email)
        # Create token with very short expiration
        token = AuthService.create_email_confirmation_token(
            token_data, 
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        with self.assertRaises(ValueError):
            AuthService.verify_email_confirmation_token(token)
            
    @patch('api.logic.logic.StorageService.engine')
    @patch('api.logic.logic.GmailEmailService.send_email_confirmation_email')
    def test_signup_with_email_confirmation(self, mock_send_email, mock_engine):
        """Test signup process sends confirmation email for non-example.com emails"""
        # Mock session
        mock_session = MagicMock()
        mock_engine.return_value = MagicMock()
        
        # Mock user creation
        mock_user = MagicMock()
        mock_user.token_version = 0
        mock_user.email_verified = False
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        # Create signup request with non-example.com email
        signup_data = SignupRequest(
            email="test@example.org",
            password=self.test_password,
            name=self.test_name,
            intends_to_be_tutor=False
        )
        
        # Mock the session context manager
        with patch('api.logic.logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session_class.return_value.__exit__.return_value = None
            
            # Mock user creation to not raise IntegrityError
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            
            # Mock token creation
            with patch('api.auth.auth_service.AuthService.create_token_pair') as mock_create_tokens:
                mock_create_tokens.return_value = {"access_token": "test", "refresh_token": "test"}
                
                # Execute signup
                result = Logic.handle_signup(signup_data)
                
                # Verify email confirmation was sent
                mock_send_email.assert_called_once()
                call_args = mock_send_email.call_args
                self.assertEqual(call_args[1]['recipient_email'], "test@example.org")
                self.assertEqual(call_args[1]['user_name'], "Test User")
                
                # Verify user was marked as unverified
                self.assertFalse(mock_user.email_verified)
                
    @patch('api.logic.logic.StorageService.engine')
    def test_signup_without_email_confirmation(self, mock_engine):
        """Test signup process doesn't send confirmation for example.com emails"""
        # Mock session
        mock_session = MagicMock()
        mock_engine.return_value = MagicMock()
        
        # Mock user creation
        mock_user = MagicMock()
        mock_user.token_version = 0
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        # Create signup request with example.com email
        signup_data = SignupRequest(
            email="test@example.com",
            password=self.test_password,
            name=self.test_name,
            intends_to_be_tutor=False
        )
        
        # Mock the session context manager
        with patch('api.logic.logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session_class.return_value.__exit__.return_value = None
            
            # Mock user creation to not raise IntegrityError
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            
            # Mock token creation
            with patch('api.auth.auth_service.AuthService.create_token_pair') as mock_create_tokens:
                mock_create_tokens.return_value = {"access_token": "test", "refresh_token": "test"}
                
                # Mock email service to verify it's not called
                with patch('api.logic.logic.GmailEmailService.send_email_confirmation_email') as mock_send_email:
                    # Execute signup
                    result = Logic.handle_signup(signup_data)
                    
                    # Verify email confirmation was NOT sent
                    mock_send_email.assert_not_called()


if __name__ == '__main__':
    unittest.main() 