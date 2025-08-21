import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import WebSocket

from api.router.websocket import WebSocketManager


class TestWebSocketManager:
    """Test cases for WebSocketManager"""

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_connect_new_user(self):
        """Test connecting a new user"""
        mock_websocket = AsyncMock()
        user_id = 123
        
        await WebSocketManager.connect(mock_websocket, user_id)
        
        mock_websocket.accept.assert_called_once()
        assert user_id in WebSocketManager.active_connections
        assert mock_websocket in WebSocketManager.active_connections[user_id]

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_connect_existing_user(self):
        """Test connecting an existing user"""
        mock_websocket1 = AsyncMock()
        mock_websocket2 = AsyncMock()
        user_id = 456
        
        # Connect first websocket
        await WebSocketManager.connect(mock_websocket1, user_id)
        
        # Connect second websocket
        await WebSocketManager.connect(mock_websocket2, user_id)
        
        assert user_id in WebSocketManager.active_connections
        assert len(WebSocketManager.active_connections[user_id]) == 2
        assert mock_websocket1 in WebSocketManager.active_connections[user_id]
        assert mock_websocket2 in WebSocketManager.active_connections[user_id]

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_disconnect_user(self):
        """Test disconnecting a user"""
        mock_websocket = AsyncMock()
        user_id = 789
        
        # Connect first
        await WebSocketManager.connect(mock_websocket, user_id)
        assert user_id in WebSocketManager.active_connections
        
        # Disconnect
        await WebSocketManager.disconnect(mock_websocket, user_id)
        assert user_id not in WebSocketManager.active_connections

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_disconnect_nonexistent_user(self):
        """Test disconnecting a non-existent user"""
        mock_websocket = AsyncMock()
        user_id = 999
        
        # Should not raise an error
        await WebSocketManager.disconnect(mock_websocket, user_id)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_send_personal_notification(self):
        """Test sending personal notification"""
        mock_websocket = AsyncMock()
        user_id = 111
        
        # Connect user
        await WebSocketManager.connect(mock_websocket, user_id)
        
        # Send notification
        message = "Test notification"
        await WebSocketManager.send_personal_notification(user_id, message)
        
        mock_websocket.send_text.assert_called_once_with(message)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_send_personal_notification_no_user(self):
        """Test sending personal notification to non-existent user"""
        user_id = 222
        message = "Test notification"
        
        # Should not raise an error
        await WebSocketManager.send_personal_notification(user_id, message)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_broadcast_notification(self):
        """Test broadcasting notification to all users"""
        mock_websocket1 = AsyncMock()
        mock_websocket2 = AsyncMock()
        
        # Connect two users
        await WebSocketManager.connect(mock_websocket1, 333)
        await WebSocketManager.connect(mock_websocket2, 444)
        
        # Broadcast message
        message = "Broadcast message"
        await WebSocketManager.broadcast_notification(message)
        
        mock_websocket1.send_text.assert_called_once_with(message)
        mock_websocket2.send_text.assert_called_once_with(message)

    @pytest.mark.unit
    @pytest.mark.router
    @pytest.mark.asyncio
    async def test_broadcast_notification_no_users(self):
        """Test broadcasting notification when no users are connected"""
        message = "Broadcast message"
        
        # Should not raise an error
        await WebSocketManager.broadcast_notification(message)
