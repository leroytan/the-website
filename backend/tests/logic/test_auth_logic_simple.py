from unittest.mock import Mock, patch

import pytest
from api.logic.auth_logic import AuthLogic
from api.router.models import LoginRequest, SignupRequest
from api.storage.models import EmailVerificationStatus, User
from fastapi import HTTPException


class TestAuthLogicSimple:
    """Simple tests for AuthLogic that work with the actual API"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_create_assert_user_authorized_success(self):
        """Test creating assert_user_authorized function that succeeds"""
        user_id = 123
        assert_func = AuthLogic.create_assert_user_authorized(user_id)

        # Should not raise exception when correct user_id is passed
        assert_func(123)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_create_assert_user_authorized_failure(self):
        """Test creating assert_user_authorized function that fails"""
        user_id = 123
        assert_func = AuthLogic.create_assert_user_authorized(user_id)

        # Should raise HTTPException when wrong user_id is passed
        with pytest.raises(HTTPException) as exc_info:
            assert_func(456)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Unauthorized action"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_handle_login_user_not_found(self):
        """Test login with non-existent user (with mocked password verification)"""
        login_data = LoginRequest(
            email="nonexistent@example.com", password="password123"
        )

        with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
            # Mock session that returns None for user
            mock_session = Mock()
            mock_session.execute.return_value.scalar_one_or_none.return_value = None
            mock_engine.return_value = mock_session

            # Mock password verification to avoid bcrypt issues
            with patch(
                "api.logic.auth_logic.AuthService.verify_password"
            ) as mock_verify:
                mock_verify.return_value = False

                with pytest.raises(HTTPException) as exc_info:
                    AuthLogic.handle_login(login_data)

                assert exc_info.value.status_code == 401
                assert "Incorrect email or password" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_handle_signup_user_already_exists(self):
        """Test signup with existing user"""
        signup_data = SignupRequest(
            email="existing@example.com",
            password="password123",
            name="Existing User",
            intends_to_be_tutor=False,
            gender="male",
        )

        # Create mock existing user
        mock_existing_user = Mock(spec=User)
        mock_existing_user.email_verification_status = EmailVerificationStatus.VERIFIED

        with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
            # Mock session that returns existing user
            mock_session = Mock()
            mock_session.execute.return_value.scalar_one_or_none.return_value = (
                mock_existing_user
            )
            mock_engine.return_value = mock_session

            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.handle_signup(signup_data, "https://example.com")

            assert exc_info.value.status_code == 409
            assert exc_info.value.detail == "User already exists"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_current_user_success(self):
        """Test getting current user successfully"""
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.token_version = 1

        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    # Mock token verification
                    mock_token_data = Mock()
                    mock_token_data.email = "test@example.com"
                    mock_token_data.token_version = 1
                    mock_verify.return_value = mock_token_data

                    # Mock session and query
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )
                    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user

                    credentials_exception = HTTPException(
                        status_code=401, detail="Invalid credentials"
                    )

                    result = AuthLogic.get_current_user(
                        "valid_token", credentials_exception
                    )

                    assert result == mock_user
                    mock_verify.assert_called_once_with("valid_token")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_current_user_no_token(self):
        """Test getting current user with no token"""
        credentials_exception = HTTPException(
            status_code=401, detail="Invalid credentials"
        )

        with pytest.raises(HTTPException) as exc_info:
            AuthLogic.get_current_user(None, credentials_exception)

        assert exc_info.value.status_code == 401

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_current_user_no_email(self):
        """Test getting current user with token but no email"""
        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            # Mock token verification with no email
            mock_token_data = Mock()
            mock_token_data.email = None
            mock_verify.return_value = mock_token_data

            credentials_exception = HTTPException(
                status_code=401, detail="Invalid credentials"
            )

            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.get_current_user("valid_token", credentials_exception)

            assert exc_info.value.status_code == 401

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_current_user_not_found(self):
        """Test getting current user when user not found"""
        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    # Mock token verification
                    mock_token_data = Mock()
                    mock_token_data.email = "test@example.com"
                    mock_token_data.token_version = 1
                    mock_verify.return_value = mock_token_data

                    # Mock session and query
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )
                    mock_session.execute.return_value.scalar_one_or_none.return_value = None

                    credentials_exception = HTTPException(
                        status_code=401, detail="Invalid credentials"
                    )

                    with pytest.raises(HTTPException) as exc_info:
                        AuthLogic.get_current_user("valid_token", credentials_exception)

                    assert exc_info.value.status_code == 401

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_current_user_token_version_mismatch(self):
        """Test getting current user with token version mismatch"""
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.token_version = 2  # Different from token

        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    # Mock token verification
                    mock_token_data = Mock()
                    mock_token_data.email = "test@example.com"
                    mock_token_data.token_version = 1  # Different from user
                    mock_verify.return_value = mock_token_data

                    # Mock session and query
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )
                    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user

                    credentials_exception = HTTPException(
                        status_code=401, detail="Invalid credentials"
                    )

                    with pytest.raises(HTTPException) as exc_info:
                        AuthLogic.get_current_user("valid_token", credentials_exception)

                    assert exc_info.value.status_code == 401
                    assert "TOKEN_VERSION_MISMATCH" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_refresh_tokens_success(self):
        """Test refreshing tokens successfully"""
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.token_version = 1

        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    with patch(
                        "api.logic.auth_logic.AuthService.create_token_pair"
                    ) as mock_create:
                        # Mock token verification
                        mock_token_data = Mock()
                        mock_token_data.email = "test@example.com"
                        mock_token_data.token_version = 1
                        mock_verify.return_value = mock_token_data

                        # Mock session and query
                        mock_session = Mock()
                        mock_session_class.return_value.__enter__.return_value = (
                            mock_session
                        )
                        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user

                        # Mock token creation
                        mock_new_tokens = Mock()
                        mock_create.return_value = mock_new_tokens

                        result = AuthLogic.refresh_tokens("valid_refresh_token")

                        assert result == mock_new_tokens
                        mock_verify.assert_called_once_with(
                            "valid_refresh_token", is_refresh=True
                        )

    @pytest.mark.unit
    @pytest.mark.logic
    def test_refresh_tokens_user_not_found(self):
        """Test refreshing tokens when user not found"""
        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    # Mock token verification
                    mock_token_data = Mock()
                    mock_token_data.email = "test@example.com"
                    mock_token_data.token_version = 1
                    mock_verify.return_value = mock_token_data

                    # Mock session and query
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )
                    mock_session.execute.return_value.scalar_one_or_none.return_value = None

                    with pytest.raises(HTTPException) as exc_info:
                        AuthLogic.refresh_tokens("valid_refresh_token")

                    assert exc_info.value.status_code == 401
                    assert exc_info.value.detail == "User not found"

    @pytest.mark.unit
    @pytest.mark.logic
    def test_refresh_tokens_token_version_mismatch(self):
        """Test refreshing tokens with token version mismatch"""
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.token_version = 2  # Different from token

        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            with patch("api.logic.auth_logic.StorageService.engine") as mock_engine:
                with patch("api.logic.auth_logic.Session") as mock_session_class:
                    # Mock token verification
                    mock_token_data = Mock()
                    mock_token_data.email = "test@example.com"
                    mock_token_data.token_version = 1  # Different from user
                    mock_verify.return_value = mock_token_data

                    # Mock session and query
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = (
                        mock_session
                    )
                    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user

                    with pytest.raises(HTTPException) as exc_info:
                        AuthLogic.refresh_tokens("valid_refresh_token")

                    assert exc_info.value.status_code == 401
                    assert "TOKEN_VERSION_MISMATCH" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_refresh_tokens_invalid_token(self):
        """Test refreshing tokens with invalid token"""
        with patch("api.logic.auth_logic.AuthService.verify_token") as mock_verify:
            # Mock token verification failure
            mock_verify.side_effect = ValueError("Invalid token")

            with pytest.raises(HTTPException) as exc_info:
                AuthLogic.refresh_tokens("invalid_token")

            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == "Invalid refresh token"
