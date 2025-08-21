import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, Request, Response
from api.router.auth_utils import RouterAuthUtils
from api.auth.models import TokenPair


class TestRouterAuthUtils:
    """Test cases for RouterAuthUtils class"""

    @pytest.mark.unit
    def test_assert_logged_out_user_not_logged_in(self):
        """Test assert_logged_out when user is not logged in"""
        mock_request = Mock()
        
        with patch.object(RouterAuthUtils, 'get_current_user') as mock_get_user:
            mock_get_user.side_effect = HTTPException(status_code=401, detail="Unauthorized")
            
            # Should not raise an exception
            RouterAuthUtils.assert_logged_out(mock_request)

    @pytest.mark.unit
    def test_assert_logged_out_user_already_logged_in(self):
        """Test assert_logged_out when user is already logged in"""
        mock_request = Mock()
        mock_user = Mock()
        
        with patch.object(RouterAuthUtils, 'get_current_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            # Should raise HTTPException
            with pytest.raises(HTTPException) as exc_info:
                RouterAuthUtils.assert_logged_out(mock_request)
            
            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "User is already logged in"

    @pytest.mark.unit
    def test_assert_logged_out_other_exception(self):
        """Test assert_logged_out when get_current_user raises non-401 exception"""
        mock_request = Mock()
        
        with patch.object(RouterAuthUtils, 'get_current_user') as mock_get_user:
            mock_get_user.side_effect = HTTPException(status_code=500, detail="Internal error")
            
            # Should re-raise the exception
            with pytest.raises(HTTPException) as exc_info:
                RouterAuthUtils.assert_logged_out(mock_request)
            
            assert exc_info.value.status_code == 500

    @pytest.mark.unit
    def test_assert_not_logged_out_user_logged_in(self):
        """Test assert_not_logged_out when user is logged in (has tokens)"""
        mock_request = Mock()
        mock_request.cookies = {
            "access_token": "valid_access_token",
            "refresh_token": "valid_refresh_token"
        }
        
        # Should not raise an exception
        RouterAuthUtils.assert_not_logged_out(mock_request)

    @pytest.mark.unit
    def test_assert_not_logged_out_user_not_logged_in(self):
        """Test assert_not_logged_out when user is not logged in (no tokens)"""
        mock_request = Mock()
        mock_request.cookies = {}
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            RouterAuthUtils.assert_not_logged_out(mock_request)
        
        assert exc_info.value.status_code == 200
        assert exc_info.value.detail == "User is already logged out"

    @pytest.mark.unit
    def test_assert_not_logged_out_partial_tokens(self):
        """Test assert_not_logged_out when only one token is present"""
        mock_request = Mock()
        mock_request.cookies = {"access_token": "valid_access_token"}
        
        # Should not raise an exception when only one token is present
        RouterAuthUtils.assert_not_logged_out(mock_request)

    @pytest.mark.unit
    def test_get_cookie_params_http_origin(self):
        """Test _get_cookie_params with HTTP origin"""
        params = RouterAuthUtils._get_cookie_params("http://localhost:3000")
        
        assert params["domain"] is None
        assert params["httponly"] is True
        assert params["secure"] is False
        assert params["samesite"] == "strict"

    @pytest.mark.unit
    def test_get_cookie_params_https_origin(self):
        """Test _get_cookie_params with HTTPS origin"""
        params = RouterAuthUtils._get_cookie_params("https://example.com")
        
        assert params["domain"] == "example.com"
        assert params["httponly"] is True
        assert params["secure"] is True
        assert params["samesite"] == "strict"

    @pytest.mark.unit
    def test_get_cookie_params_no_protocol(self):
        """Test _get_cookie_params with origin without protocol"""
        params = RouterAuthUtils._get_cookie_params("example.com")
        
        assert params["domain"] == "example.com"
        assert params["httponly"] is True
        assert params["secure"] is True
        assert params["samesite"] == "strict"

    @pytest.mark.unit
    def test_clear_tokens(self):
        """Test clear_tokens method"""
        mock_response = Mock()
        
        RouterAuthUtils.clear_tokens(mock_response, "https://example.com")
        
        # Check that delete_cookie was called twice (for access and refresh tokens)
        calls = mock_response.delete_cookie.call_args_list
        assert len(calls) == 2
        assert calls[0][1]["key"] == "access_token"
        assert calls[1][1]["key"] == "refresh_token"
        
        # Check cookie parameters
        for call in calls:
            kwargs = call[1]
            assert kwargs["domain"] == "example.com"
            assert kwargs["httponly"] is True
            assert kwargs["secure"] is True
            assert kwargs["samesite"] == "strict"

    @pytest.mark.unit
    def test_update_tokens(self):
        """Test update_tokens method"""
        mock_response = Mock()
        mock_tokens = Mock(spec=TokenPair)
        mock_tokens.access_token = "new_access_token"
        mock_tokens.refresh_token = "new_refresh_token"
        
        RouterAuthUtils.update_tokens(mock_tokens, mock_response, "https://example.com")
        
        # Check that set_cookie was called twice (for access and refresh tokens)
        calls = mock_response.set_cookie.call_args_list
        assert len(calls) == 2
        assert calls[0][1]["key"] == "access_token"
        assert calls[0][1]["value"] == "new_access_token"
        assert calls[1][1]["key"] == "refresh_token"
        assert calls[1][1]["value"] == "new_refresh_token"
        
        # Check cookie parameters
        for call in calls:
            kwargs = call[1]
            assert kwargs["domain"] == "example.com"
            assert kwargs["httponly"] is True
            assert kwargs["secure"] is True
            assert kwargs["samesite"] == "strict"

    @pytest.mark.unit
    def test_clear_tokens_http_origin(self):
        """Test clear_tokens with HTTP origin"""
        mock_response = Mock()
        
        RouterAuthUtils.clear_tokens(mock_response, "http://localhost:3000")
        
        # Check that secure is False for HTTP
        calls = mock_response.delete_cookie.call_args_list
        for call in calls:
            kwargs = call[1]
            assert kwargs["secure"] is False
            assert kwargs["domain"] is None

    @pytest.mark.unit
    def test_update_tokens_http_origin(self):
        """Test update_tokens with HTTP origin"""
        mock_response = Mock()
        mock_tokens = Mock(spec=TokenPair)
        mock_tokens.access_token = "new_access_token"
        mock_tokens.refresh_token = "new_refresh_token"
        
        RouterAuthUtils.update_tokens(mock_tokens, mock_response, "http://localhost:3000")
        
        # Check that secure is False for HTTP
        calls = mock_response.set_cookie.call_args_list
        for call in calls:
            kwargs = call[1]
            assert kwargs["secure"] is False
            assert kwargs["domain"] is None

    @pytest.mark.unit
    def test_get_current_user_success(self):
        """Test get_current_user when successful"""
        mock_request = Mock()
        mock_request.cookies = {"access_token": "valid_token"}
        mock_user = Mock()
        
        with patch('api.router.auth_utils.AuthLogic.get_current_user') as mock_get_current_user:
            mock_get_current_user.return_value = mock_user
                
            result = RouterAuthUtils.get_current_user(mock_request)
            assert result == mock_user

    @pytest.mark.unit
    def test_get_current_user_no_access_token(self):
        """Test get_current_user when no access token is present"""
        mock_request = Mock()
        mock_request.cookies = {}
        
        with pytest.raises(HTTPException) as exc_info:
            RouterAuthUtils.get_current_user(mock_request)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    @pytest.mark.unit
    def test_get_current_user_invalid_token(self):
        """Test get_current_user when token is invalid"""
        mock_request = Mock()
        mock_request.cookies = {"access_token": "invalid_token"}
        
        with patch('api.router.auth_utils.AuthLogic.get_current_user') as mock_get_current_user:
            mock_get_current_user.side_effect = HTTPException(status_code=401, detail="Invalid token")
            
            with pytest.raises(HTTPException) as exc_info:
                RouterAuthUtils.get_current_user(mock_request)
            
            assert exc_info.value.status_code == 401
            assert "Invalid token" in exc_info.value.detail

    @pytest.mark.unit
    def test_get_current_user_user_not_found(self):
        """Test get_current_user when user is not found"""
        mock_request = Mock()
        mock_request.cookies = {"access_token": "valid_token"}
        
        with patch('api.router.auth_utils.AuthLogic.get_current_user') as mock_get_current_user:
            mock_get_current_user.side_effect = HTTPException(status_code=401, detail="User not found")
            
            with pytest.raises(HTTPException) as exc_info:
                RouterAuthUtils.get_current_user(mock_request)
            
            assert exc_info.value.status_code == 401
            assert "User not found" in exc_info.value.detail 