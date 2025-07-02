import asyncio
import json
from collections.abc import Callable
from datetime import datetime

from api.router.models import ChatPreview, NewChatMessage
from api.storage.models import ChatMessage, ChatReadStatus, PrivateChat, User, ChatMessageType, TutorRequestStatus
from api.storage.storage_service import StorageService
from fastapi import HTTPException, WebSocket
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


class ChatLogic:
    active_connections: dict[str|int, WebSocket] = {}
    mutex = asyncio.Lock()

    @staticmethod
    def get_chat_preview(session: Session, user_id: int, chat: PrivateChat) -> ChatPreview:
        """
        Get a preview of the chat.
        """
        chat_id = chat.id
        if chat.is_locked:  # TODO: Implement alias names for locked chats
            other_name = "Anonymous User"
        else:
            other_id = chat.user1_id if chat.user1_id != user_id else chat.user2_id
            other_name = session.query(User).filter(User.id == other_id).first().name
        # Get the last message in the chat
        res = session.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at.desc()).first()
        # Get message content and created_at
        last_message = res.content if res else ""
        last_message_time = res.created_at.isoformat() if res else ""
        last_message_type = res.message_type if res else "text_message"
        read_status = session.query(ChatReadStatus).filter(
            ChatReadStatus.chat_id == chat_id,
            ChatReadStatus.user_id == user_id,
        ).first()
        has_unread = not read_status.is_read if read_status else False

        # Frontend expects the following format
        return ChatPreview(
            id=chat_id,
            name=other_name,
            last_message=last_message,
            last_update=last_message_time,
            last_message_type=last_message_type,
            has_unread=has_unread,
            is_locked=chat.is_locked,
            has_messages=bool(res),
        )

    @staticmethod
    def get_convert_message(user_id: int) -> Callable[[ChatMessage], dict]:
        def convert_message(message: ChatMessage) -> dict:
            """
            Convert a chat message to a dictionary format in the expected format for the frontend.
            """
            sent_by_user = message.sender_id == user_id
            message_dict = {
                "id": message.id,
                "chat_id": message.chat_id,
                "sender": message.sender.name,
                "content": message.content,
                "message_type": message.message_type.value,
                "created_at": message.created_at.isoformat(),
                "updated_at": message.updated_at.isoformat(),
                "sent_by_user": sent_by_user,
            }
            if message.message_type == ChatMessageType.TUTOR_REQUEST:
                content = json.loads(message_dict.get("content"))  # Ensure content is valid JSON
                if message.assignment_request:
                    content["status"] = message.assignment_request.status.value
                else:
                    content["status"] = TutorRequestStatus.EXPIRED.value
                message_dict["content"] = json.dumps(content)
            return message_dict
        return convert_message

    @staticmethod
    def get_or_create_private_chat(current_user_id: int, other_user_id: int) -> ChatPreview:
        """
        Get or create a chatroom between two users.

        Args:
            session (Session): The SQLAlchemy session.
            user1_id (int): The ID of the first user.
            user2_id (int): The ID of the second user.

        Returns:
            Chat: The chatroom object.
        """
        with Session(StorageService.engine) as session:
            # Ensure that user1_id is less than user2_id to maintain consistency
            user1_id = min(current_user_id, other_user_id)
            user2_id = max(current_user_id, other_user_id)
            # Check if the chatroom already exists
            chat = session.query(PrivateChat).filter(
                    and_(PrivateChat.user1_id == user1_id, PrivateChat.user2_id == user2_id)
            ).first()

            if not chat:
                try:
                    # If it doesn't exist, create it
                    chat = PrivateChat(user1_id=user1_id, user2_id=user2_id)
                    session.add(chat)
                    session.flush()
                    session.commit()
                except IntegrityError as e:
                    if isinstance(e.orig, ForeignKeyViolation):
                        raise HTTPException(status_code=400, detail="One or both users do not exist.")
                    else:
                        raise HTTPException(status_code=500, detail="An error occurred while creating the chatroom.")
            return ChatLogic.get_chat_preview(session, current_user_id, chat)
        
    @staticmethod
    def store_private_message(session: Session, new_chat_message: NewChatMessage, sender_id: int) -> ChatMessage:
        """
        Stores a new chat message in the database and returns the stored ChatMessage object.

        Args:
            new_chat_message (NewChatMessage): The new chat message to be stored.
            sender_id (int): The ID of the user sending the message.

        Returns:
            ChatMessage: The stored chat message object.
        """
        # Validate the incoming message
        chat_id = new_chat_message.chat_id

        chat = session.query(PrivateChat).filter(PrivateChat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chatroom not found.")
        elif chat.user1_id != sender_id and chat.user2_id != sender_id:
            raise HTTPException(status_code=403, detail="You are not authorized to send messages in this chatroom.")

        # Check if the chatroom is locked
        if chat.is_locked:
            # Do some content filtering
            pass

        # Create a ChatMessage object
        chat_message = ChatMessage(
            content=new_chat_message.content,
            sender_id=sender_id,
            chat_id=chat_id,
            message_type=new_chat_message.message_type
        )

        # Add the message to the session
        session.add(chat_message)
        receiver_id = chat_message.receiver_id_from_chat(chat)

        # Update the read status for the receiver
        read_status = session.query(ChatReadStatus).filter_by(chat_id=chat_id, user_id=receiver_id).first()
        if not read_status:
            read_status = ChatReadStatus(chat_id=chat_id, user_id=receiver_id, is_read=False)
            session.add(read_status)
        else:
            read_status.is_read = False
        session.commit()
        
        # Refresh the chat message and load the chat relationship
        session.refresh(chat_message, ['chat', 'sender', 'assignment_request'])

        return chat_message
    
    @staticmethod
    async def send_notification_to_user(user_id: int, notification_data: dict) -> None:
        """
        Send a notification to a user via the root WebSocket connection.
        This is imported here to avoid circular imports.
        """
        try:
            from api.router.websocket import WebSocketManager
            notification_json = json.dumps(notification_data)
            await WebSocketManager.send_personal_notification(user_id, notification_json)
        except ImportError:
            print("WebSocketManager not available for notifications")
        except Exception as e:
            print(f"Failed to send notification to user {user_id}: {e}")
    
    @staticmethod
    async def send_private_message(chat_message: ChatMessage) -> None:
        """
        Sends a private chat message to the appropriate WebSocket connections.
        Args:
            chat_message (ChatMessage): The chat message to be sent.
        """
        receiver_id = chat_message.receiver_id
        sender_id = chat_message.sender_id

        # Send the message to the receiver via WebSocket
        if receiver_id in ChatLogic.active_connections:
            # Send the message to the receiver's WebSocket
            # Ensure that the receiver is connected
            try:
                to_send = json.dumps(ChatLogic.get_convert_message(-1)(chat_message))
                print(f"Sending message to receiver {receiver_id}: {to_send}")
                await ChatLogic.active_connections[receiver_id].send_text(to_send)
            except RuntimeError:
                async with ChatLogic.mutex:
                    ChatLogic.active_connections.pop(receiver_id, None)

        if sender_id in ChatLogic.active_connections:
            # Send the message to the sender's WebSocket
            try:
                to_send = json.dumps(ChatLogic.get_convert_message(sender_id)(chat_message))
                print(f"Sending message to sender {sender_id}: {to_send}")
                await ChatLogic.active_connections[sender_id].send_text(to_send)
            except RuntimeError:
                async with ChatLogic.mutex:
                    ChatLogic.active_connections.pop(sender_id, None)

        # Send notification to receiver via root WebSocket if they're not connected to chat
        if receiver_id not in ChatLogic.active_connections:
            with Session(StorageService.engine) as session:
                sender = session.query(User).filter(User.id == sender_id).first()
                sender_name = sender.name if sender else "Unknown User"
                
                notification_data = {
                    "type": "new_message",
                    "message": f"New message from {sender_name}",
                    "chat_id": chat_message.chat_id,
                    "sender_id": sender_id,
                    "sender_name": sender_name,
                    "content_preview": chat_message.content[:50] + "..." if len(chat_message.content) > 50 else chat_message.content,
                    "message_type": chat_message.message_type.value,
                    "timestamp": chat_message.created_at.isoformat()
                }
                await ChatLogic.send_notification_to_user(receiver_id, notification_data)

    @staticmethod
    async def handle_private_message(new_chat_message: NewChatMessage, sender_id: int) -> None:
        """
        Handles the incoming chat message, processes it, and returns a ChatMessage object.

        Args:
            new_chat_message (NewChatMessage): The new chat message to be processed.
            user_id (int): The ID of the user sending the message.

        Returns:
            ChatMessage: The processed chat message object.
        """
        with Session(StorageService.engine, expire_on_commit=False) as session:
            chat_message = ChatLogic.store_private_message(session, new_chat_message, sender_id)
            await ChatLogic.send_private_message(chat_message)

    @staticmethod
    def get_private_chat_history(chat_id: int, user_id: int, created_before: str, limit: int) -> dict:
        convert_message = ChatLogic.get_convert_message(user_id)

        with Session(StorageService.engine) as session:
            chatroom = StorageService.find(session, {"id": chat_id}, PrivateChat, find_one=True)
            if not chatroom:
                raise HTTPException(status_code=404, detail="Chatroom not found.")
            elif chatroom.user1_id != user_id and chatroom.user2_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to view this chatroom.")

            query = session.query(ChatMessage).filter(
                ChatMessage.chat_id == chat_id,
            )

            if created_before:
                created_before_dt = datetime.fromisoformat(created_before)
                query = query.filter(ChatMessage.created_at < created_before_dt)
           
            chat_messages = query.order_by(ChatMessage.created_at.desc()).limit(limit + 1).all()
            has_more = len(chat_messages) > limit

            print(f"Chat messages fetched: {len(chat_messages)} (limit: {limit}, has_more: {has_more})")
            return {
                "messages": [
                    convert_message(message) for message in chat_messages[:limit]
                ][::-1],  # Reverse the order to show the oldest messages first
                "message_count": len(chat_messages),
                "has_more": has_more,
            }
   
    @staticmethod
    def unlock_chat(chat_id: int, user_id: int) -> None:
        """
        Unlock a chatroom.

        Args:
            chat_id (int): The ID of the chatroom to unlock.
        """
        with Session(StorageService.engine) as session:
            chat = session.query(PrivateChat).filter(PrivateChat.id == chat_id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chatroom not found.")
            elif chat.user1_id != user_id and chat.user2_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to unlock this chatroom.")
            chat.is_locked = False
            session.commit()
            
    @staticmethod
    def get_private_chats(user_id: int) -> dict:
        """
        Get all private chats for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[PrivateChat]: List of private chatrooms.
        """     
    
        with Session(StorageService.engine) as session:
            chats = session.query(PrivateChat).filter(
                (PrivateChat.user1_id == user_id) | (PrivateChat.user2_id == user_id),
            ).options(
                joinedload(PrivateChat.user1),
                joinedload(PrivateChat.user2)
            ).all()
            
            return {
                "chats": [
                    ChatLogic.get_chat_preview(session, user_id, chat) for chat in chats
                ]
            }
        
    @staticmethod
    def mark_chat_as_read(chat_id: int, user_id: int) -> None:
        """
        Mark a chat as read for the current user.

        Args:
            chat_id (int): The ID of the chat to mark as read.
            user_id (int): The ID of the user marking the chat as read.
        """
        with Session(StorageService.engine) as session:
            chat = session.query(PrivateChat).filter(PrivateChat.id == chat_id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chatroom not found.")
            if chat.user1_id != user_id and chat.user2_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to mark this chat as read.")
            session.add(chat)
            
            status = session.query(ChatReadStatus).filter_by(chat_id=chat_id, user_id=user_id).first()
            if not status:
                status = ChatReadStatus(chat_id=chat_id, user_id=user_id, is_read=True)
                session.add(status)
            else:
                status.is_read = True

            session.commit()