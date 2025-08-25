from datetime import timedelta
from unittest.mock import Mock, patch

import httpx
import pytest
from api.auth.auth_service import AuthService
from api.auth.models import TokenData, TokenPair
from api.storage.models import User
from jose import JWTError


class TestAuthService:
    """Test cases for AuthService"""

    @pytest.mark.unit
    @pytest.mark.auth
    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrongpassword", hashed) is False

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_password(self):
        """Test password verification"""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)

        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrongpassword", hashed) is False

        with pytest.raises(ValueError):
            AuthService.verify_password("", hashed)

        with pytest.raises(ValueError):
            AuthService.verify_password(password, "")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_create_token_pair(self):
        """Test token pair creation"""
        token_data = TokenData(email="test@example.com", token_version=0)
        token_pair = AuthService.create_token_pair(token_data)

        assert isinstance(token_pair, TokenPair)
        assert token_pair.access_token is not None
        assert token_pair.refresh_token is not None
        assert len(token_pair.access_token) > 0
        assert len(token_pair.refresh_token) > 0

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_token_valid(self):
        """Test valid token verification"""
        token_data = TokenData(email="test@example.com", token_version=0)
        token_pair = AuthService.create_token_pair(token_data)

        verified_data = AuthService.verify_token(token_pair.access_token)

        assert verified_data.email == token_data.email
        assert verified_data.token_version == token_data.token_version

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_token_invalid(self):
        """Test invalid token verification"""
        with pytest.raises(JWTError):
            AuthService.verify_token("invalid_token")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_token_expired(self):
        """Test expired token verification"""
        token_data = TokenData(email="test@example.com", token_version=0)
        # Create token with very short expiration
        access_token = AuthService.create_access_token(
            token_data, expires_delta=timedelta(seconds=1)
        )

        # Wait for token to expire
        import time

        time.sleep(2)

        # Test with the expired token
        with pytest.raises(JWTError):
            AuthService.verify_token(access_token)

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_refresh_token(self):
        """Test refresh token verification"""
        token_data = TokenData(email="test@example.com", token_version=0)
        token_pair = AuthService.create_token_pair(token_data)

        verified_data = AuthService.verify_token(
            token_pair.refresh_token, is_refresh=True
        )

        assert verified_data.email == token_data.email
        assert verified_data.token_version == token_data.token_version

    @pytest.mark.unit
    @pytest.mark.auth
    def test_create_password_reset_token(self):
        """Test password reset token creation"""
        token_data = TokenData(email="test@example.com", token_version=0)
        reset_token = AuthService.create_password_reset_token(
            token_data, token_version=0
        )

        assert reset_token is not None
        assert len(reset_token) > 0

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_password_reset_token(self):
        """Test password reset token verification"""
        token_data = TokenData(email="test@example.com", token_version=0)
        reset_token = AuthService.create_password_reset_token(
            token_data, token_version=0
        )

        verified_data = AuthService.verify_password_reset_token(reset_token)

        assert verified_data.email == token_data.email
        assert verified_data.token_version == token_data.token_version

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_password_reset_token_invalid(self):
        """Test invalid password reset token verification"""
        with pytest.raises(ValueError):
            AuthService.verify_password_reset_token("invalid_token")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_create_email_confirmation_token(self):
        """Test email confirmation token creation"""
        token_data = TokenData(email="test@example.com", token_version=0)
        confirmation_token = AuthService.create_email_confirmation_token(
            token_data, token_version=0
        )

        assert confirmation_token is not None
        assert len(confirmation_token) > 0

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_email_confirmation_token(self):
        """Test email confirmation token verification"""
        token_data = TokenData(email="test@example.com", token_version=0)
        confirmation_token = AuthService.create_email_confirmation_token(
            token_data, token_version=0
        )

        verified_data = AuthService.verify_email_confirmation_token(confirmation_token)

        assert verified_data.email == token_data.email
        assert verified_data.token_version == token_data.token_version

    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_email_confirmation_token_invalid(self):
        """Test invalid email confirmation token verification"""
        with pytest.raises(ValueError):
            AuthService.verify_email_confirmation_token("invalid_token")

    @pytest.mark.unit
    @pytest.mark.auth
    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_authenticate_google_user_success(self, mock_client):
        """Test successful Google authentication"""
        # Mock the responses
        mock_token_response = Mock()
        mock_token_response.json.return_value = {"access_token": "mock_access_token"}
        mock_token_response.raise_for_status.return_value = None

        mock_user_info_response = Mock()
        mock_user_info_response.json.return_value = {
            "email": "test@gmail.com",
            "name": "Test User",
            "sub": "google_user_id",
        }
        mock_user_info_response.raise_for_status.return_value = None

        # Setup the mock client instance
        mock_client_instance = Mock()

        async def mock_post(*args, **kwargs):
            return mock_token_response

        async def mock_get(*args, **kwargs):
            return mock_user_info_response

        mock_client_instance.post = mock_post
        mock_client_instance.get = mock_get
        mock_client.return_value = mock_client_instance

        # Mock StorageService methods
        with patch("api.auth.auth_service.StorageService") as mock_storage:
            mock_storage.get_user_by_google_id.return_value = None
            mock_storage.get_user_by_email.return_value = None
            mock_storage.create_user.return_value = User(
                email="test@gmail.com",
                name="Test User",
                google_id="google_user_id",
                token_version=0,
            )

            token_pair = await AuthService.authenticate_google_user("mock_auth_code")

            assert isinstance(token_pair, TokenPair)
            assert token_pair.access_token is not None
            assert token_pair.refresh_token is not None

    @pytest.mark.unit
    @pytest.mark.auth
    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_authenticate_google_user_token_exchange_failure(self, mock_client):
        """Test Google authentication with token exchange failure"""
        # Mock the responses
        mock_client_instance = Mock()

        async def mock_post(*args, **kwargs):
            raise httpx.HTTPError("Token exchange failed")

        mock_client_instance.post = mock_post
        mock_client.return_value = mock_client_instance

        with pytest.raises(httpx.HTTPError):
            await AuthService.authenticate_google_user("mock_auth_code")

    @pytest.mark.unit
    @pytest.mark.auth
    def test_token_data_validation(self):
        """Test TokenData model validation"""
        # Valid token data
        token_data = TokenData(email="test@example.com", token_version=0)
        assert token_data.email == "test@example.com"
        assert token_data.token_version == 0

        # Test required fields
        with pytest.raises(Exception):
            TokenData(token_version=0)  # Missing email field
        assert token_data.token_version == 0

        # Test with invalid email
        with pytest.raises(ValueError):
            TokenData(email="invalid-email", token_version=0)

    @pytest.mark.unit
    @pytest.mark.auth
    def test_token_pair_validation(self):
        """Test TokenPair model validation"""
        token_pair = TokenPair(
            access_token="mock_access_token", refresh_token="mock_refresh_token"
        )

        assert token_pair.access_token == "mock_access_token"
        assert token_pair.refresh_token == "mock_refresh_token"
