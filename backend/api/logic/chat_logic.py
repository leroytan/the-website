import json
from collections.abc import Callable
from datetime import datetime

from api.logic.logic import Logic
from api.router.models import NewChatMessage
from api.storage.models import ChatMessage, ChatReadStatus, PrivateChat, User
from api.storage.storage_service import StorageService
from fastapi import HTTPException, WebSocket
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


class ChatLogic:

    @staticmethod
    def get_chat_preview(session: Session, user_id: int, chat: PrivateChat) -> dict:
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
        read_status = session.query(ChatReadStatus).filter(
            ChatReadStatus.chat_id == chat_id,
            ChatReadStatus.user_id == user_id,
        ).first()
        has_unread = not read_status.is_read if read_status else False

        # Frontend expects the following format
        return {
            "id": chat_id,
            "name": other_name,
            "last_message": last_message,
            "last_update": last_message_time,
            "has_unread": has_unread,
            "is_locked": chat.is_locked,
            "has_messages": bool(res),
        }

    @staticmethod
    def get_convert_message(user_id: int) -> Callable[[ChatMessage], dict]:
        def convert_message(message: ChatMessage) -> dict:
            """
            Convert a chat message to a dictionary format in the expected format for the frontend.
            """
            sent_by_user = message.sender_id == user_id
            return {
                "id": message.id,
                "chat_id": message.chat_id,
                "sender": message.sender.name,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
                "updated_at": message.updated_at.isoformat(),
                "sent_by_user": sent_by_user,
            }
        return convert_message

    @staticmethod
    def get_or_create_private_chat(current_user_id: int, other_user_id: int) -> dict:
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
    async def handle_private_message(active_connections: dict[str|int, WebSocket], new_chat_message: NewChatMessage, sender_id: int) -> None:
        """
        Handles the incoming chat message, processes it, and returns a ChatMessage object.

        Args:
            new_chat_message (NewChatMessage): The new chat message to be processed.
            user_id (int): The ID of the user sending the message.

        Returns:
            ChatMessage: The processed chat message object.
        """
        # Validate the incoming message
        with Session(StorageService.engine) as session:
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
                chat_id=chat_id
            )

            # Add the message to the session
            session.add(chat_message)
            session.commit()
            session.refresh(chat_message)
            receiver_id = chat_message.receiver_id

            # Update the read status for the receiver
            read_status = session.query(ChatReadStatus).filter_by(chat_id=chat_id, user_id=receiver_id).first()
            if not read_status:
                read_status = ChatReadStatus(chat_id=chat_id, user_id=receiver_id, is_read=False)
                session.add(read_status)
            else:
                read_status.is_read = False
            session.commit()
            
            # Send the message to the receiver via WebSocket
            if receiver_id in active_connections:
                # Send the message to the receiver's WebSocket
                # Ensure that the receiver is connected
                try:
                    to_send = json.dumps(ChatLogic.get_convert_message(-1)(chat_message))
                    await active_connections[receiver_id].send_text(to_send)
                except RuntimeError:
                    active_connections.pop(receiver_id, None)

            if sender_id in active_connections:
                # Send the message to the sender's WebSocket
                try:
                    to_send = json.dumps(ChatLogic.get_convert_message(sender_id)(chat_message))
                    await active_connections[sender_id].send_text(to_send)
                except RuntimeError:
                    active_connections.pop(sender_id, None)

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