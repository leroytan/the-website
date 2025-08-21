import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import Request

from api.router.chat import router


class TestChatRouter:
    """Test cases for chat router"""

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch('api.router.chat.RouterAuthUtils.get_current_user')
    @patch('api.router.chat.RouterAuthUtils.get_jwt')
    async def test_get_jwt(self, mock_get_jwt, mock_get_current_user):
        """Test get_jwt endpoint"""
        # Mock user and request
        mock_user = Mock()
        mock_request = Mock()
        mock_get_current_user.return_value = mock_user
        mock_get_jwt.return_value = "test_jwt_token"
        
        # Import the function
        from api.router.chat import get_jwt
        
        # Call the function
        result = await get_jwt(mock_request, mock_user)
        
        # Verify result
        assert result == {"access_token": "test_jwt_token"}
        mock_get_jwt.assert_called_once_with(mock_request)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch('api.router.chat.ChatLogic.get_or_create_private_chat')
    @patch('api.router.chat.RouterAuthUtils.get_current_user')
    async def test_get_or_create_chat(self, mock_get_current_user, mock_get_or_create):
        """Test get_or_create_chat endpoint"""
        # Mock user and chat info
        mock_user = Mock(id=123)
        mock_chat_info = Mock(other_user_id=456)
        mock_get_current_user.return_value = mock_user
        
        # Mock return value
        mock_chat_preview = Mock()
        mock_get_or_create.return_value = mock_chat_preview
        
        # Import the function
        from api.router.chat import get_or_create_chat
        
        # Call the function
        result = await get_or_create_chat(mock_chat_info, mock_user)
        
        # Verify result
        assert result == mock_chat_preview
        mock_get_or_create.assert_called_once_with(123, 456)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch('api.router.chat.ChatLogic.get_private_chat_history')
    @patch('api.router.chat.RouterAuthUtils.get_current_user')
    async def test_get_chat_messages(self, mock_get_current_user, mock_get_history):
        """Test get_chat_messages endpoint"""
        # Mock user
        mock_user = Mock(id=123)
        mock_get_current_user.return_value = mock_user
        
        # Mock return value
        mock_history = {"messages": []}
        mock_get_history.return_value = mock_history
        
        # Import the function
        from api.router.chat import get_chat_messages
        
        # Call the function
        result = await get_chat_messages(id=789, user=mock_user, created_before="2023-01-01", limit=25)
        
        # Verify result
        assert result == mock_history
        mock_get_history.assert_called_once_with(789, 123, "2023-01-01", 25)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch('api.router.chat.ChatLogic.mark_chat_as_read')
    @patch('api.router.chat.RouterAuthUtils.get_current_user')
    async def test_mark_chat_as_read(self, mock_get_current_user, mock_mark_read):
        """Test mark_chat_as_read endpoint"""
        # Mock user
        mock_user = Mock(id=123)
        mock_get_current_user.return_value = mock_user
        
        # Mock return value - the function returns a fixed response, not from ChatLogic
        mock_mark_read.return_value = None
        
        # Import the function
        from api.router.chat import mark_chat_as_read
        
        # Call the function
        result = await mark_chat_as_read(id=789, user=mock_user)
        
        # Verify result
        assert result == {"status": "success", "message": "Chat marked as read."}
        mock_mark_read.assert_called_once_with(789, 123)
