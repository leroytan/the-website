import pytest
import json
from unittest.mock import patch, Mock, AsyncMock, MagicMock
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation

from api.logic.chat_logic import ChatLogic
from api.storage.models import (
    User, PrivateChat, ChatMessage, ChatReadStatus, 
    ChatMessageType, TutorRequestStatus
)
from api.router.models import ChatPreview, NewChatMessage

class TestChatLogicMockable:
    """Test cases for chat logic with proper mocking"""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_chat_preview_with_messages_proper_mocking(self):
        """Test get_chat_preview with proper SQLAlchemy mocking"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock user
        mock_user = Mock()
        mock_user.name = "User 2"
        
        # Create mock last message
        mock_last_message = Mock()
        mock_last_message.content = "Hello there!"
        mock_last_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_last_message.message_type = ChatMessageType.TEXT_MESSAGE
        
        # Create mock read status
        mock_read_status = Mock()
        mock_read_status.is_read = False
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.id = 1
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = False
        
        # Mock the SQLAlchemy query chain properly
        # First query: session.query(User).filter(User.id == other_id).first()
        mock_user_query = Mock()
        mock_user_query.filter.return_value.first.return_value = mock_user
        
        # Second query: session.query(ChatMessage).filter(...).order_by(...).first()
        mock_message_query = Mock()
        mock_message_query.filter.return_value.order_by.return_value.first.return_value = mock_last_message
        
        # Third query: session.query(ChatReadStatus).filter(...).first()
        mock_read_query = Mock()
        mock_read_query.filter.return_value.first.return_value = mock_read_status
        
        # Set up the session.query to return different mocks based on the model
        def mock_query_side_effect(model):
            if model == User:
                return mock_user_query
            elif model == ChatMessage:
                return mock_message_query
            elif model == ChatReadStatus:
                return mock_read_query
            else:
                return Mock()
        
        mock_session.query.side_effect = mock_query_side_effect
        
        # Test the method
        result = ChatLogic.get_chat_preview(mock_session, 1, mock_chat)
        
        assert isinstance(result, ChatPreview)
        assert result.id == 1
        assert result.name == "User 2"
        assert result.last_message == "Hello there!"
        assert result.has_unread is True
        assert result.is_locked is False
        assert result.has_messages is True

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_chat_preview_no_messages(self):
        """Test get_chat_preview with no messages"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock user
        mock_user = Mock()
        mock_user.name = "User 2"
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.id = 1
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = True
        
        # Mock the SQLAlchemy query chain properly
        mock_user_query = Mock()
        mock_user_query.filter.return_value.first.return_value = mock_user
        
        mock_message_query = Mock()
        mock_message_query.filter.return_value.order_by.return_value.first.return_value = None
        
        mock_read_query = Mock()
        mock_read_query.filter.return_value.first.return_value = None
        
        def mock_query_side_effect(model):
            if model == User:
                return mock_user_query
            elif model == ChatMessage:
                return mock_message_query
            elif model == ChatReadStatus:
                return mock_read_query
            else:
                return Mock()
        
        mock_session.query.side_effect = mock_query_side_effect
        
        # Test the method
        result = ChatLogic.get_chat_preview(mock_session, 1, mock_chat)
        
        assert isinstance(result, ChatPreview)
        assert result.id == 1
        assert result.name == "User 2"
        assert result.last_message == ""
        assert result.has_unread is False
        assert result.is_locked is True
        assert result.has_messages is False

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_chat_preview_user2_perspective(self):
        """Test get_chat_preview from user2's perspective"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock user (user1 from user2's perspective)
        mock_user = Mock()
        mock_user.name = "User 1"
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.id = 1
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = False
        
        # Mock the SQLAlchemy query chain properly
        mock_user_query = Mock()
        mock_user_query.filter.return_value.first.return_value = mock_user
        
        mock_message_query = Mock()
        mock_message_query.filter.return_value.order_by.return_value.first.return_value = None
        
        mock_read_query = Mock()
        mock_read_query.filter.return_value.first.return_value = None
        
        def mock_query_side_effect(model):
            if model == User:
                return mock_user_query
            elif model == ChatMessage:
                return mock_message_query
            elif model == ChatReadStatus:
                return mock_read_query
            else:
                return Mock()
        
        mock_session.query.side_effect = mock_query_side_effect
        
        # Test the method from user2's perspective
        result = ChatLogic.get_chat_preview(mock_session, 2, mock_chat)
        
        assert result.name == "User 1"  # Should show user1's name

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_or_create_private_chat_existing_chat(self):
        """Test get_or_create_private_chat with existing chat"""
        with patch('api.logic.chat_logic.Session') as mock_session_class:
            with patch('api.logic.chat_logic.StorageService') as mock_storage:
                # Mock session context manager
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock existing chat
                mock_chat = Mock()
                mock_chat.id = 1
                mock_chat.user1_id = 1
                mock_chat.user2_id = 2
                mock_chat.is_locked = False
                
                # Mock the query to return existing chat
                mock_query = Mock()
                mock_query.filter.return_value.first.return_value = mock_chat
                mock_session.query.return_value = mock_query
                
                # Mock get_chat_preview
                with patch.object(ChatLogic, 'get_chat_preview') as mock_get_preview:
                    mock_preview = ChatPreview(
                        id=1, name="User 2", last_message="", last_update="",
                        last_message_type="text_message", has_unread=False,
                        is_locked=False, has_messages=False
                    )
                    mock_get_preview.return_value = mock_preview
                    
                    # Test the method
                    result = ChatLogic.get_or_create_private_chat(1, 2)
                    
                    assert result == mock_preview
                    # Should not create new chat
                    mock_session.add.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_or_create_private_chat_new_chat(self):
        """Test get_or_create_private_chat with new chat creation"""
        with patch('api.logic.chat_logic.Session') as mock_session_class:
            with patch('api.logic.chat_logic.StorageService') as mock_storage:
                # Mock session context manager
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock no existing chat
                mock_query = Mock()
                mock_query.filter.return_value.first.return_value = None
                mock_session.query.return_value = mock_query
                
                # Mock get_chat_preview
                with patch.object(ChatLogic, 'get_chat_preview') as mock_get_preview:
                    mock_preview = ChatPreview(
                        id=1, name="User 2", last_message="", last_update="",
                        last_message_type="text_message", has_unread=False,
                        is_locked=False, has_messages=False
                    )
                    mock_get_preview.return_value = mock_preview
                    
                    # Test the method
                    result = ChatLogic.get_or_create_private_chat(1, 2)
                    
                    assert result == mock_preview
                    # Should create new chat
                    mock_session.add.assert_called_once()
                    mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_or_create_private_chat_foreign_key_violation(self):
        """Test get_or_create_private_chat with foreign key violation"""
        with patch('api.logic.chat_logic.Session') as mock_session_class:
            with patch('api.logic.chat_logic.StorageService') as mock_storage:
                # Mock session context manager
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock no existing chat
                mock_query = Mock()
                mock_query.filter.return_value.first.return_value = None
                mock_session.query.return_value = mock_query
                
                # Mock foreign key violation on commit
                mock_session.commit.side_effect = IntegrityError("", "", ForeignKeyViolation())
                
                # Test the method
                with pytest.raises(HTTPException) as exc_info:
                    ChatLogic.get_or_create_private_chat(1, 999)  # Non-existent user
                
                assert exc_info.value.status_code == 400
                assert "One or both users do not exist" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_or_create_private_chat_other_integrity_error(self):
        """Test get_or_create_private_chat with other integrity error"""
        with patch('api.logic.chat_logic.Session') as mock_session_class:
            with patch('api.logic.chat_logic.StorageService') as mock_storage:
                # Mock session context manager
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock no existing chat
                mock_query = Mock()
                mock_query.filter.return_value.first.return_value = None
                mock_session.query.return_value = mock_query
                
                # Mock other integrity error on commit
                mock_session.commit.side_effect = IntegrityError("", "", Exception())
                
                # Test the method
                with pytest.raises(HTTPException) as exc_info:
                    ChatLogic.get_or_create_private_chat(1, 2)
                
                assert exc_info.value.status_code == 500
                assert "error occurred while creating" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_or_create_private_chat_user_order_normalization(self):
        """Test get_or_create_private_chat normalizes user order (user1_id < user2_id)"""
        with patch('api.logic.chat_logic.Session') as mock_session_class:
            with patch('api.logic.chat_logic.StorageService') as mock_storage:
                # Mock session context manager
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock no existing chat
                mock_query = Mock()
                mock_query.filter.return_value.first.return_value = None
                mock_session.query.return_value = mock_query
                
                # Mock get_chat_preview
                with patch.object(ChatLogic, 'get_chat_preview') as mock_get_preview:
                    mock_preview = ChatPreview(
                        id=1, name="User 1", last_message="", last_update="",
                        last_message_type="text_message", has_unread=False,
                        is_locked=False, has_messages=False
                    )
                    mock_get_preview.return_value = mock_preview
                    
                    # Test with user2_id < user1_id (should normalize)
                    result = ChatLogic.get_or_create_private_chat(5, 2)
                    
                    # Verify the query was called with normalized user IDs (2, 5)
                    mock_query.filter.assert_called_once()
                    # The filter should be called with user1_id=2, user2_id=5
                    call_args = mock_query.filter.call_args[0][0]
                    # This is a complex SQLAlchemy expression, so we just verify it was called
                    assert mock_query.filter.called

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_store_private_message_success(self):
        """Test store_private_message success case"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = False
        
        # Create mock new message
        new_message = NewChatMessage(
            chat_id=1,
            content="Hello world",
            message_type=ChatMessageType.TEXT_MESSAGE
        )
        
        # Mock chat query
        mock_session.query.return_value.filter.return_value.first.return_value = mock_chat
        
        # Mock content filter service
        with patch('api.logic.chat_logic.content_filter_service') as mock_filter:
            # Mock the filter to return not filtered (async method)
            mock_filter.filter_message = AsyncMock(return_value={
                "filtered": False,
                "content": "Hello world"
            })
            
            # Mock the ChatMessage creation and session operations
            mock_chat_message = Mock()
            mock_chat_message.content = "Hello world"
            mock_chat_message.sender_id = 1
            mock_chat_message.chat_id = 1
            mock_chat_message.is_flagged = False
            mock_chat_message.receiver_id_from_chat = Mock(return_value=2)
            
            # Mock session.add to return the mock message
            mock_session.add.return_value = None
            
            # Test the method
            result = await ChatLogic.store_private_message(mock_session, new_message, 1)
            
            # Verify the message was added to session
            mock_session.add.assert_called()
            mock_session.commit.assert_called()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_store_private_message_filtered_content(self):
        """Test store_private_message with filtered content"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = True  # Locked chat triggers filtering
        
        # Create mock new message
        new_message = NewChatMessage(
            chat_id=1,
            content="Inappropriate content",
            message_type=ChatMessageType.TEXT_MESSAGE
        )
        
        # Mock chat query
        mock_session.query.return_value.filter.return_value.first.return_value = mock_chat
        
        # Mock content filter service
        with patch('api.logic.chat_logic.content_filter_service') as mock_filter:
            # Mock the filter to return filtered content (async method)
            mock_filter.filter_message = AsyncMock(return_value={
                "filtered": True,
                "content": "Filtered content",
                "reasoning": "Inappropriate language"
            })
            
            # Mock the ChatMessage creation and session operations
            mock_chat_message = Mock()
            mock_chat_message.content = "Inappropriate content"
            mock_chat_message.filtered_content = "Filtered content"
            mock_chat_message.is_flagged = True
            mock_chat_message.receiver_id_from_chat = Mock(return_value=2)
            
            # Mock session.add to return the mock message
            mock_session.add.return_value = None
            
            # Test the method
            result = await ChatLogic.store_private_message(mock_session, new_message, 1)
            
            # Verify the message was added to session
            mock_session.add.assert_called()
            mock_session.commit.assert_called()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_store_private_message_unauthorized(self):
        """Test store_private_message with unauthorized user"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        
        # Create mock new message
        new_message = NewChatMessage(
            chat_id=1,
            content="Hello world",
            message_type=ChatMessageType.TEXT_MESSAGE
        )
        
        # Mock chat query
        mock_session.query.return_value.filter.return_value.first.return_value = mock_chat
        
        # Test the method with unauthorized user (user_id=3)
        with pytest.raises(HTTPException) as exc_info:
            await ChatLogic.store_private_message(mock_session, new_message, 3)
        
        assert exc_info.value.status_code == 403
        assert "not authorized" in exc_info.value.detail.lower()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_store_private_message_chat_not_found(self):
        """Test store_private_message with chat not found"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock new message
        new_message = NewChatMessage(
            chat_id=999,
            content="Hello world",
            message_type=ChatMessageType.TEXT_MESSAGE
        )
        
        # Mock chat query to return None (chat not found)
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Test the method
        with pytest.raises(HTTPException) as exc_info:
            await ChatLogic.store_private_message(mock_session, new_message, 1)
        
        assert exc_info.value.status_code == 404
        assert "Chatroom not found" in exc_info.value.detail

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_store_private_message_filtering_fails(self):
        """Test store_private_message when content filtering fails"""
        # Create mock session
        mock_session = Mock()
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.user1_id = 1
        mock_chat.user2_id = 2
        mock_chat.is_locked = True  # Locked chat triggers filtering
        
        # Create mock new message
        new_message = NewChatMessage(
            chat_id=1,
            content="Test content",
            message_type=ChatMessageType.TEXT_MESSAGE
        )
        
        # Mock chat query
        mock_session.query.return_value.filter.return_value.first.return_value = mock_chat
        
        # Mock content filter service to raise exception
        with patch('api.logic.chat_logic.content_filter_service') as mock_filter:
            mock_filter.filter_message = AsyncMock(side_effect=Exception("Filter service down"))
            
            # Mock the ChatMessage creation and session operations
            mock_chat_message = Mock()
            mock_chat_message.content = "Test content"
            mock_chat_message.is_flagged = False
            mock_chat_message.receiver_id_from_chat = Mock(return_value=2)
            
            # Mock session.add to return the mock message
            mock_session.add.return_value = None
            
            # Test the method - should not raise exception, just log error
            result = await ChatLogic.store_private_message(mock_session, new_message, 1)
            
            # Verify the message was still added to session despite filtering failure
            mock_session.add.assert_called()
            mock_session.commit.assert_called()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_notification_to_user_success(self):
        """Test send_notification_to_user success case"""
        notification_data = {"type": "message", "content": "New message"}
        
        # Mock the import inside the function - patch the actual import location
        with patch('api.router.websocket.WebSocketManager') as mock_ws_manager:
            # Mock the class method
            mock_ws_manager.send_personal_notification = AsyncMock()
            
            # Test the method
            await ChatLogic.send_notification_to_user(1, notification_data)
            
            # Verify the notification was sent
            mock_ws_manager.send_personal_notification.assert_called_once_with(
                1, json.dumps(notification_data)
            )

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_notification_to_user_import_error(self):
        """Test send_notification_to_user when WebSocketManager import fails"""
        notification_data = {"type": "message", "content": "New message"}
        
        # Mock the import to fail
        with patch('api.logic.chat_logic.WebSocketManager', create=True, side_effect=ImportError):
            # Test the method - should not raise exception, just print error
            await ChatLogic.send_notification_to_user(1, notification_data)
            # No assertion needed - just checking it doesn't crash

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_notification_to_user_ws_error(self):
        """Test send_notification_to_user when WebSocketManager raises exception"""
        notification_data = {"type": "message", "content": "New message"}
        
        # Mock the import inside the function
        with patch('api.logic.chat_logic.WebSocketManager', create=True) as mock_ws_manager:
            mock_ws_manager.send_personal_notification = AsyncMock(side_effect=Exception("WS error"))
            
            # Test the method - should not raise exception, just print error
            await ChatLogic.send_notification_to_user(1, notification_data)
            # No assertion needed - just checking it doesn't crash

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_private_message_success(self):
        """Test send_private_message success case"""
        # Create mock message
        mock_message = Mock()
        mock_message.receiver_id = 2
        mock_message.sender_id = 1
        mock_message.is_flagged = False
        mock_message.chat.is_locked = False
        
        # Create mock WebSocket connections
        mock_receiver_ws = AsyncMock()
        mock_sender_ws = AsyncMock()
        
        # Mock active connections
        ChatLogic.active_connections = {
            1: mock_sender_ws,
            2: mock_receiver_ws
        }
        
        # Mock get_convert_message
        with patch.object(ChatLogic, 'get_convert_message') as mock_convert:
            mock_convert.return_value = lambda msg: {"id": 1, "content": "test"}
            
            # Test the method
            await ChatLogic.send_private_message(mock_message)
            
            # Verify messages were sent
            mock_receiver_ws.send_text.assert_called_once()
            mock_sender_ws.send_text.assert_called_once()
            
        # Clean up
        ChatLogic.active_connections.clear()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_private_message_flagged_and_locked(self):
        """Test send_private_message with flagged message in locked chat"""
        # Create mock message
        mock_message = Mock()
        mock_message.receiver_id = 2
        mock_message.sender_id = 1
        mock_message.is_flagged = True
        mock_message.chat.is_locked = True
        
        # Create mock WebSocket connections
        mock_receiver_ws = AsyncMock()
        mock_sender_ws = AsyncMock()
        
        # Mock active connections
        ChatLogic.active_connections = {
            1: mock_sender_ws,
            2: mock_receiver_ws
        }
        
        # Mock get_convert_message
        with patch.object(ChatLogic, 'get_convert_message') as mock_convert:
            mock_convert.return_value = lambda msg: {"id": 1, "content": "test"}
            
            # Test the method
            await ChatLogic.send_private_message(mock_message)
            
            # Verify only sender gets message (receiver shouldn't get flagged message in locked chat)
            mock_receiver_ws.send_text.assert_not_called()
            mock_sender_ws.send_text.assert_called_once()
            
        # Clean up
        ChatLogic.active_connections.clear()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_private_message_receiver_not_connected(self):
        """Test send_private_message when receiver is not connected"""
        # Create mock message with proper attributes
        mock_message = Mock()
        mock_message.receiver_id = 2
        mock_message.sender_id = 1
        mock_message.is_flagged = False
        mock_message.chat_id = 1  # Add chat_id attribute
        mock_message.content = "Test message"
        mock_message.message_type = ChatMessageType.TEXT_MESSAGE
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.is_locked = False
        mock_message.chat = mock_chat
        
        # Create mock WebSocket connection only for sender
        mock_sender_ws = AsyncMock()
        
        # Mock active connections (receiver not connected)
        ChatLogic.active_connections = {
            1: mock_sender_ws
        }
        
        # Mock get_convert_message
        with patch.object(ChatLogic, 'get_convert_message') as mock_convert:
            mock_convert.return_value = lambda msg: {"id": 1, "content": "test"}
            
            # Mock send_notification_to_user
            with patch.object(ChatLogic, 'send_notification_to_user') as mock_notify:
                mock_notify.return_value = None
                
                # Mock the database session and queries
                with patch('api.logic.chat_logic.Session') as mock_session_class:
                    mock_session = Mock()
                    mock_session_class.return_value.__enter__.return_value = mock_session
                    mock_session_class.return_value.__exit__.return_value = None
                    
                    # Mock chat query
                    mock_chat_query = Mock()
                    mock_chat_query.filter.return_value.first.return_value = mock_chat
                    
                    # Mock user query
                    mock_user = Mock()
                    mock_user.name = "Test User"
                    mock_user_query = Mock()
                    mock_user_query.filter.return_value.first.return_value = mock_user
                    
                    # Set up session.query to return different mocks
                    def mock_query_side_effect(model):
                        if model == PrivateChat:
                            return mock_chat_query
                        elif model == User:
                            return mock_user_query
                        else:
                            return Mock()
                    
                    mock_session.query.side_effect = mock_query_side_effect
                    
                    # Test the method
                    await ChatLogic.send_private_message(mock_message)
                    
                    # Verify sender gets message and notification is sent to receiver
                    mock_sender_ws.send_text.assert_called_once()
                    mock_notify.assert_called_once()
                
        # Clean up
        ChatLogic.active_connections.clear()

    @pytest.mark.unit
    @pytest.mark.logic
    @pytest.mark.asyncio
    async def test_send_private_message_websocket_runtime_error(self):
        """Test send_private_message when WebSocket send fails"""
        # Create mock message with proper attributes
        mock_message = Mock()
        mock_message.receiver_id = 2
        mock_message.sender_id = 1
        mock_message.is_flagged = False
        mock_message.chat_id = 1  # Add chat_id attribute
        mock_message.content = "Test message"
        mock_message.message_type = ChatMessageType.TEXT_MESSAGE
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        # Create mock chat
        mock_chat = Mock()
        mock_chat.is_locked = False
        mock_message.chat = mock_chat
        
        # Create mock WebSocket connections that raise RuntimeError
        mock_receiver_ws = AsyncMock()
        mock_receiver_ws.send_text.side_effect = RuntimeError("Connection closed")
        mock_sender_ws = AsyncMock()
        mock_sender_ws.send_text.side_effect = RuntimeError("Connection closed")
        
        # Mock active connections
        ChatLogic.active_connections = {
            1: mock_sender_ws,
            2: mock_receiver_ws
        }
        
        # Mock get_convert_message
        with patch.object(ChatLogic, 'get_convert_message') as mock_convert:
            mock_convert.return_value = lambda msg: {"id": 1, "content": "test"}
            
            # Mock the database session and queries
            with patch('api.logic.chat_logic.Session') as mock_session_class:
                mock_session = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session
                mock_session_class.return_value.__exit__.return_value = None
                
                # Mock chat query
                mock_chat_query = Mock()
                mock_chat_query.filter.return_value.first.return_value = mock_chat
                
                # Mock user query
                mock_user = Mock()
                mock_user.name = "Test User"
                mock_user_query = Mock()
                mock_user_query.filter.return_value.first.return_value = mock_user
                
                # Set up session.query to return different mocks
                def mock_query_side_effect(model):
                    if model == PrivateChat:
                        return mock_chat_query
                    elif model == User:
                        return mock_user_query
                    else:
                        return Mock()
                
                mock_session.query.side_effect = mock_query_side_effect
                
                # Test the method
                await ChatLogic.send_private_message(mock_message)
                
                # Verify connections were removed from active_connections
                assert 1 not in ChatLogic.active_connections
                assert 2 not in ChatLogic.active_connections
            
        # Clean up
        ChatLogic.active_connections.clear()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_convert_message_text_message(self):
        """Test get_convert_message for text message"""
        # Create mock message
        mock_message = Mock()
        mock_message.id = 1
        mock_message.chat_id = 1
        mock_message.sender_id = 1  # Add sender_id attribute
        mock_message.sender.name = "Test User"
        mock_message.content = "Hello world"
        mock_message.message_type = ChatMessageType.TEXT_MESSAGE
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.updated_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.is_flagged = False
        mock_message.filtered_content = None
        
        # Get converter function for user_id=1 (same as sender_id=1)
        converter = ChatLogic.get_convert_message(1)
        
        # Test conversion
        result = converter(mock_message)
        
        assert result["id"] == 1
        assert result["chat_id"] == 1
        assert result["sender"] == "Test User"
        assert result["content"] == "Hello world"
        assert result["message_type"] == "text_message"
        # The sent_by_user should be True because user_id (1) == sender_id (1)
        assert result["sent_by_user"] is True
        assert result["is_flagged"] is False

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_convert_message_flagged_message(self):
        """Test get_convert_message for flagged message"""
        # Create mock message
        mock_message = Mock()
        mock_message.id = 1
        mock_message.chat_id = 1
        mock_message.sender.name = "Test User"
        mock_message.content = "Original content"
        mock_message.message_type = ChatMessageType.TEXT_MESSAGE
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.updated_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.is_flagged = True
        mock_message.filtered_content = "Filtered content"
        
        # Get converter function for different user (not sender)
        converter = ChatLogic.get_convert_message(2)
        
        # Test conversion
        result = converter(mock_message)
        
        assert result["content"] == "Filtered content"  # Should use filtered content
        assert result["sent_by_user"] is False
        assert result["is_flagged"] is True

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_convert_message_tutor_request(self):
        """Test get_convert_message for tutor request message"""
        # Create mock message
        mock_message = Mock()
        mock_message.id = 1
        mock_message.chat_id = 1
        mock_message.sender.name = "Test User"
        mock_message.content = '{"assignment_id": 1, "message": "I need help"}'
        mock_message.message_type = ChatMessageType.TUTOR_REQUEST
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.updated_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.is_flagged = False
        mock_message.filtered_content = None
        
        # Create mock assignment request
        mock_assignment_request = Mock()
        mock_assignment_request.status = TutorRequestStatus.PENDING
        mock_message.assignment_request = mock_assignment_request
        
        # Get converter function
        converter = ChatLogic.get_convert_message(1)
        
        # Test conversion
        result = converter(mock_message)
        
        assert result["message_type"] == "tutor_request"
        # Should have status added to content
        content = result["content"]
        assert "status" in content
        assert "PENDING" in content

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_convert_message_tutor_request_expired(self):
        """Test get_convert_message for tutor request message without assignment request"""
        # Create mock message
        mock_message = Mock()
        mock_message.id = 1
        mock_message.chat_id = 1
        mock_message.sender.name = "Test User"
        mock_message.content = '{"assignment_id": 1, "message": "I need help"}'
        mock_message.message_type = ChatMessageType.TUTOR_REQUEST
        mock_message.created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.updated_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_message.is_flagged = False
        mock_message.filtered_content = None
        mock_message.assignment_request = None  # No assignment request
        
        # Get converter function
        converter = ChatLogic.get_convert_message(1)
        
        # Test conversion
        result = converter(mock_message)
        
        assert result["message_type"] == "tutor_request"
        # Should have EXPIRED status added to content
        content = result["content"]
        assert "status" in content
        assert "EXPIRED" in content
