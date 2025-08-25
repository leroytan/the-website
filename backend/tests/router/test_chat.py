import json
from unittest.mock import AsyncMock, Mock, patch

import pytest
from api.exceptions import ConsecutiveMessageError


class TestChatRouter:
    """Test cases for chat router"""

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch("api.router.chat.RouterAuthUtils.get_current_user")
    @patch("api.router.chat.RouterAuthUtils.get_jwt")
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
    @patch("api.router.chat.ChatLogic.get_or_create_private_chat")
    @patch("api.router.chat.RouterAuthUtils.get_current_user")
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
    @patch("api.router.chat.ChatLogic.get_private_chat_history")
    @patch("api.router.chat.RouterAuthUtils.get_current_user")
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
        result = await get_chat_messages(
            id=789, user=mock_user, created_before="2023-01-01", limit=25
        )

        # Verify result
        assert result == mock_history
        mock_get_history.assert_called_once_with(789, 123, "2023-01-01", 25)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch("api.router.chat.ChatLogic.mark_chat_as_read")
    @patch("api.router.chat.RouterAuthUtils.get_current_user")
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

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    @patch("api.router.chat.RouterAuthUtils.get_user_from_jwt")
    @patch("api.router.chat.ChatLogic.handle_private_message")
    async def test_websocket_consecutive_message_limit(
        self, mock_handle_private_message, mock_get_user_from_jwt
    ):
        """Test websocket endpoint for consecutive message limit"""
        # Mock user
        mock_user = Mock(id=123)
        mock_get_user_from_jwt.return_value = mock_user

        # Mock websocket with regular Mock instead of AsyncMock to avoid unawaited coroutines
        mock_websocket = Mock()
        mock_websocket.accept = AsyncMock()
        mock_websocket.receive_text = AsyncMock()
        mock_websocket.send_text = AsyncMock()

        # Create a simple context manager mock that doesn't use AsyncMock
        class MockMutex:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

        mock_mutex = MockMutex()

        # Mock ChatLogic.mutex and active_connections
        with patch("api.router.chat.ChatLogic.mutex", mock_mutex):
            with patch("api.router.chat.ChatLogic.active_connections", {}):
                # Make handle_private_message an async function that raises ConsecutiveMessageError
                async def mock_handle_side_effect(*args, **kwargs):
                    raise ConsecutiveMessageError()

                mock_handle_private_message.side_effect = mock_handle_side_effect

                # Import the function
                from api.router.chat import websocket_endpoint
                from fastapi import WebSocketDisconnect

                # Mock WebSocketDisconnect to be raised on second receive_text call
                mock_websocket.receive_text.side_effect = [
                    json.dumps({"chat_id": 1, "content": "test message"}),
                    WebSocketDisconnect(),
                ]

                # Call the websocket endpoint
                try:
                    await websocket_endpoint(mock_websocket, "some_token")
                except WebSocketDisconnect:
                    pass  # Expected when websocket disconnects

                # Verify that an error message was sent
                expected_error = {
                    "id": -1,
                    "chat_id": 1,
                    "sender": "System",
                    "content": "You cannot send more than 3 consecutive messages in a locked chat.",
                    "message_type": "text_message",
                    "created_at": mock_websocket.send_text.call_args[0][
                        0
                    ],  # We'll check this dynamically
                    "updated_at": mock_websocket.send_text.call_args[0][
                        0
                    ],  # We'll check this dynamically
                    "sent_by_user": False,
                    "is_flagged": False,
                    "is_error": True,
                }

                # Get the actual call and parse the JSON
                actual_call = mock_websocket.send_text.call_args[0][0]
                actual_error = json.loads(actual_call)

                # Check that the error message has the correct structure
                assert actual_error["id"] == -1
                assert actual_error["chat_id"] == 1
                assert actual_error["sender"] == "System"
                assert (
                    actual_error["content"]
                    == "You cannot send more than 3 consecutive messages in a locked chat."
                )
                assert actual_error["message_type"] == "text_message"
                assert actual_error["sent_by_user"] == False
                assert actual_error["is_flagged"] == False
                assert actual_error["is_error"] == True
                # Check that timestamps are present and valid
                assert "created_at" in actual_error
                assert "updated_at" in actual_error
