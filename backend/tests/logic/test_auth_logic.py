import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from api.logic.auth_logic import AuthLogic
from api.router.models import LoginRequest, SignupRequest, ForgotPasswordRequest, ResetPasswordRequest, VerifyPasswordResetTokenRequest, EmailConfirmationRequest
from api.storage.models import User, EmailVerificationStatus
from api.auth.models import TokenData, TokenPair
from api.common.constants import AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS

class TestLogic:
    """Test cases for Logic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_login_success(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test successful login"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.password_hash = "hashed_password"
        mock_user.email_verification_status = EmailVerificationStatus.VERIFIED
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock password verification
            mock_auth_service.verify_password.return_value = True
            
            # Mock token creation
            mock_token_pair = Mock()
            mock_auth_service.create_token_pair.return_value = mock_token_pair
            
            # Create login request
            login_request = LoginRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"]
            )
            
            # Test the method
            result = AuthLogic.handle_login(login_request)
            
            assert result == mock_token_pair
            mock_auth_service.verify_password.assert_called_once_with(
                sample_user_data["password"], "hashed_password"
            )

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_login_user_not_found(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test login with non-existent user"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = None
            
            # Create login request
            login_request = LoginRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"]
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_login(login_request)
            
            assert exc_info.value.status_code == 401
            assert "Incorrect email or password" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_login_wrong_password(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test login with wrong password"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.password_hash = "hashed_password"
        mock_user.email_verification_status = EmailVerificationStatus.VERIFIED
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock password verification to return False
            mock_auth_service.verify_password.return_value = False
            
            # Create login request
            login_request = LoginRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"]
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_login(login_request)
            
            assert exc_info.value.status_code == 401
            assert "Incorrect email or password" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_login_pending_verification(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test login with pending email verification"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with pending verification
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.password_hash = "hashed_password"
        mock_user.email_verification_status = EmailVerificationStatus.PENDING
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock password verification
            mock_auth_service.verify_password.return_value = True
            
            # Create login request
            login_request = LoginRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"]
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_login(login_request)
            
            assert exc_info.value.status_code == 403
            assert "EMAIL_NOT_VERIFIED" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_login_waitlisted(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test login with waitlisted user"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with waitlisted status
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.password_hash = "hashed_password"
        mock_user.email_verification_status = EmailVerificationStatus.WAITLISTED
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock password verification
            mock_auth_service.verify_password.return_value = True
            
            # Create login request
            login_request = LoginRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"]
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_login(login_request)
            
            assert exc_info.value.status_code == 403
            assert "USER_WAITLISTED" in str(exc_info.value.detail)



    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    @patch('api.logic.auth_logic.GmailEmailService')
    def test_handle_signup_success_pending_verification(self, mock_email_service, mock_auth_service, mock_storage_service, sample_user_data):
        """Test successful signup with pending verification"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = None
            
            # Mock password hashing
            mock_auth_service.hash_password.return_value = "hashed_password"
            
            # Mock email confirmation token creation
            mock_auth_service.create_email_confirmation_token.return_value = "confirmation_token"
            
            # Mock email service methods
            mock_email_service.create_email_confirmation_link.return_value = "confirmation_link"
            mock_email_service.send_email_confirmation_email.return_value = None
            
            # Create signup request with regular email (needs verification)
            signup_request = SignupRequest(
                email="test@regular.com",
                password=sample_user_data["password"],
                name=sample_user_data["name"],
                intends_to_be_tutor=False
            )
            
            # Test the method
            result = AuthLogic.handle_signup(signup_request, "http://localhost:3000")
            
            assert result["status"] == "pending_verification"
            assert "Account created successfully" in result["message"]

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_signup_user_already_exists(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test signup with existing user"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock existing user
        mock_existing_user = Mock()
        mock_existing_user.email_verification_status = EmailVerificationStatus.VERIFIED
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_existing_user
            
            # Create signup request
            signup_request = SignupRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"],
                name=sample_user_data["name"],
                intends_to_be_tutor=False
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_signup(signup_request, "http://localhost:3000")
            
            assert exc_info.value.status_code == 409
            assert "User already exists" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_handle_signup_integrity_error(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test signup with database integrity error"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = None
            mock_session.add.side_effect = IntegrityError("", "", "")
            
            # Mock password hashing
            mock_auth_service.hash_password.return_value = "hashed_password"
            
            # Create signup request
            signup_request = SignupRequest(
                email=sample_user_data["email"],
                password=sample_user_data["password"],
                name=sample_user_data["name"],
                intends_to_be_tutor=False
            )
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_signup(signup_request, "http://localhost:3000")
            
            assert exc_info.value.status_code == 409
            assert "User already exists" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_get_current_user_success(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test getting current user with valid token"""
        # Mock token verification
        mock_token_data = TokenData(email=sample_user_data["email"], token_version=0)
        mock_auth_service.verify_token.return_value = mock_token_data
        
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock credentials exception
            credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
            
            # Test the method
            result = AuthLogic.get_current_user("valid_token", credentials_exception)
            
            assert result == mock_user
            mock_auth_service.verify_token.assert_called_once_with("valid_token")

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_get_current_user_token_version_mismatch(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test getting current user with token version mismatch"""
        # Mock token verification
        mock_token_data = TokenData(email=sample_user_data["email"], token_version=1)
        mock_auth_service.verify_token.return_value = mock_token_data
        
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with different token version
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.token_version = 0  # Different from token version
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock credentials exception
            credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
            
            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.get_current_user("valid_token", credentials_exception)
            
            assert exc_info.value.status_code == 401
            assert "TOKEN_VERSION_MISMATCH" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_refresh_tokens_success(self, mock_auth_service, mock_storage_service, sample_user_data):
        """Test successful token refresh"""
        # Mock token verification
        mock_token_data = TokenData(email=sample_user_data["email"], token_version=0)
        mock_auth_service.verify_token.return_value = mock_token_data
        
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = sample_user_data["email"]
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock token creation
            mock_token_pair = Mock()
            mock_auth_service.create_token_pair.return_value = mock_token_pair
            
            # Test the method
            result = AuthLogic.refresh_tokens("valid_refresh_token")
            
            assert result == mock_token_pair
            mock_auth_service.verify_token.assert_called_once_with("valid_refresh_token", is_refresh=True)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    @patch('api.logic.auth_logic.GmailEmailService')
    def test_forgot_password_success(self, mock_email_service, mock_auth_service, mock_storage_service):
        """Test successful forgot password request"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = "test@example.com"
        mock_user.token_version = 0
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock token creation
            mock_auth_service.create_password_reset_token.return_value = "reset_token"
            
            # Mock email service methods
            mock_email_service.create_reset_link.return_value = "reset_link"
            mock_email_service.send_password_reset_email.return_value = "success"
            
            # Create forgot password request
            forgot_password_request = ForgotPasswordRequest(email="test@example.com")
            
            # Test the method
            result = AuthLogic.forgot_password("http://localhost:3000", forgot_password_request)
            
            assert "message" in result
            assert "reset link has been sent" in result["message"]

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    def test_forgot_password_user_not_found(self, mock_storage_service):
        """Test forgot password with non-existent user"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = None
            
            # Create forgot password request
            forgot_password_request = ForgotPasswordRequest(email="nonexistent@example.com")
            
            # Test the method
            result = AuthLogic.forgot_password("http://localhost:3000", forgot_password_request)
            
            assert "message" in result
            assert "reset link has been sent" in result["message"]

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_reset_password_success(self, mock_auth_service, mock_storage_service):
        """Test successful password reset"""
        # Mock the database session
        mock_session = Mock()
        mock_storage_service.engine = Mock()
        
        # Mock token verification
        mock_token_data = TokenData(email="test@example.com", token_version=0)
        mock_auth_service.verify_password_reset_token.return_value = mock_token_data
        
        # Create a mock user with proper attributes
        mock_user = Mock()
        mock_user.email = "test@example.com"
        mock_user.token_version = 0
        mock_user.password_reset_token = "valid_reset_token_that_is_long_enough_for_validation_32_chars"
        mock_user.password_reset_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        # Mock the session context manager
        with patch('api.logic.auth_logic.Session') as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
            
            # Mock password hashing
            mock_auth_service.hash_password.return_value = "new_hashed_password"
            
            # Create reset password request with valid token
            reset_password_request = ResetPasswordRequest(
                reset_token="valid_reset_token_that_is_long_enough_for_validation_32_chars",
                new_password="newpassword123"
            )
            
            # Test the method
            result = AuthLogic.reset_password(reset_password_request)
            
            assert "message" in result
            assert "Password successfully updated" in result["message"]

    @pytest.mark.unit
    @pytest.mark.logic
    @patch('api.logic.auth_logic.StorageService')
    @patch('api.logic.auth_logic.AuthService')
    def test_reset_password_invalid_token(self, mock_auth_service, mock_storage_service):
        """Test password reset with invalid token"""
        # Mock token verification to raise exception
        mock_auth_service.verify_password_reset_token.side_effect = ValueError("Invalid token")
        
        # Create reset password request with invalid token
        reset_password_request = ResetPasswordRequest(
            reset_token="invalid_token_that_is_long_enough_for_validation_32_chars",
            new_password="newpassword123"
        )
        
        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            AuthLogic.reset_password(reset_password_request)
        
        assert exc_info.value.status_code == 400
        assert "Invalid reset token" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_create_assert_user_authorized(self):
        """Test creating assert user authorized function"""
        # Test the method
        assert_user_authorized = AuthLogic.create_assert_user_authorized(123)
        
        # Should not raise exception for correct user ID
        assert_user_authorized(123)
        
        # Should raise exception for wrong user ID
        with pytest.raises(HTTPException) as exc_info:
            assert_user_authorized(456)
        
        assert exc_info.value.status_code == 403
        assert "Unauthorized action" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    @patch('api.logic.auth_logic.AuthService')
    async def test_handle_google_login_signup_success(self, mock_auth_service):
        """Test successful Google login/signup"""
        # Mock Google authentication
        mock_token_pair = Mock()
        mock_auth_service.authenticate_google_user = AsyncMock(return_value=mock_token_pair)
        
        # Test the method
        result = await AuthLogic.handle_google_login_signup("mock_auth_code")
        
        assert result == mock_token_pair
        mock_auth_service.authenticate_google_user.assert_called_once_with("mock_auth_code")

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    @patch('api.logic.auth_logic.AuthService')
    async def test_handle_google_login_signup_failure(self, mock_auth_service):
        """Test Google login/signup failure"""
        # Mock Google authentication to raise exception
        mock_auth_service.authenticate_google_user = AsyncMock(side_effect=Exception("Google auth failed"))
        
        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            await AuthLogic.handle_google_login_signup("mock_auth_code")
        
        assert exc_info.value.status_code == 400
        assert "Google authentication failed" in str(exc_info.value.detail) 