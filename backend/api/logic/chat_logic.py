import json

from api.router.models import NewChatMessage
from api.storage.models import ChatMessage, PrivateChat, User
from api.storage.storage_service import StorageService
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload


class ChatLogic:

    @staticmethod
    def get_or_create_private_chat(user1_id: int, user2_id: int) -> PrivateChat:
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
            if user1_id > user2_id:
                user1_id, user2_id = user2_id, user1_id
            # Check if the chatroom already exists
            chat = session.query(PrivateChat).filter(
                    and_(PrivateChat.user1_id == user2_id, PrivateChat.user2_id == user1_id)
            ).first()

            # If it doesn't exist, create it
            if not chat:
                chat = PrivateChat(user1_id=user1_id, user2_id=user2_id)
                session.add(chat)
                session.commit()

            return {
                "chat_id": chat.id,
                "is_locked": chat.is_locked,
            }

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
            if chat.user1_id != sender_id and chat.user2_id != sender_id:
                raise HTTPException(status_code=403, detail="You are not authorized to send messages in this chatroom.")
            session.add(chat)

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
            to_send = json.dumps(chat_message.to_dict(rules=(
                            "-sender",
                            "-chat",
                        )))
            
            receiver_id = chat_message.receiver_id
            
            # Send the message to the receiver via WebSocket
            if receiver_id in active_connections:
                # Send the message to the receiver's WebSocket
                # Ensure that the receiver is connected
                try:
                    await active_connections[receiver_id].send_text(to_send)
                except WebSocketDisconnect:
                    active_connections.pop(receiver_id, None)

    @staticmethod
    async def get_private_chat_history(chat_id: int, user_id: int, last_message_id: int, message_count: int) -> list[dict]:
        """
        Get chat history between two users.

        Args:
            chat_id (int): The ID of the user to get chat history with.
            user_id (int): The ID of the current user.
            last_message_id (int): The ID of the last message received.
            message_count (int): The number of messages to retrieve prior to (and including) the last message.

        Returns:
            list[ChatMessage]: List of chat messages.
        """
        async def convert_message(message: ChatMessage) -> dict:
            """
            Convert a chat message to a dictionary format in the expected format for the frontend.
            """
            sent_by_user = message.sender_id == user_id
            return {
                "id": message.id,
                "sender": message.sender.name,
                "message": message.content,
                "time": message.created_at.isoformat(),
                "sentByUser": sent_by_user,
            }

        with Session(StorageService.engine) as session:
            chatroom = StorageService.find(session, {"id": chat_id}, PrivateChat, find_one=True)
            if chatroom.user1_id != user_id and chatroom.user2_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to view this chatroom.")
            session.add(chatroom)

            # Get the chat messages
            if last_message_id == -1: last_message_id = float('inf')
            chat_messages = session.query(ChatMessage).filter(
                ChatMessage.chat_id == chat_id,
                ChatMessage.id <= last_message_id
            ).order_by(ChatMessage.created_at.desc()).limit(message_count).all()
            return [
                await convert_message(message) for message in chat_messages
            ][::-1]  # Reverse the order to show the oldest messages first
        
   
    @staticmethod
    async def unlock_chat(chat_id: int) -> None:
        """
        Unlock a chatroom.

        Args:
            chat_id (int): The ID of the chatroom to unlock.
        """
        with Session(StorageService.engine) as session:
            chat = session.query(PrivateChat).filter(PrivateChat.id == chat_id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chatroom not found.")
            session.add(chat)
            chat.is_locked = False
            session.commit()
            session.refresh(chat)
            
    @staticmethod
    async def get_private_chats(user_id: int) -> dict:
        """
        Get all private chats for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[PrivateChat]: List of private chatrooms.
        """     
    
        with Session(StorageService.engine) as session:
            async def get_chat_preview(chat: PrivateChat, locked: bool = True) -> dict:
                """
                Get a preview of the chat.
                """
                chat_id = chat.id
                if locked:  # TODO: Implement alias names for locked chats
                    other_name = "Anonymous User"
                else:
                    other_id = chat.user1_id if chat.user1_id != user_id else chat.user2_id
                    other_name = session.query(User).filter(User.id == other_id).first().name
                messages = await ChatLogic.get_private_chat_history(chat_id, user_id, -1, 1)
                last_message = messages[0]["message"] if messages else ""
                last_message_time = messages[0]["time"] if messages else None
                unread_count = 5  # Placeholder for unread messages count

                # Frontend expects the following format
                return {
                    "id": chat_id,
                    "name": other_name,
                    "message": last_message,
                    "time": last_message_time,
                    "notifications": unread_count,
                }

            locked_chats = session.query(PrivateChat).filter(
                (PrivateChat.user1_id == user_id) | (PrivateChat.user2_id == user_id),
                PrivateChat.is_locked == True
            ).options(
                joinedload(PrivateChat.user1),
                joinedload(PrivateChat.user2)
            ).all()

            unlocked_chats = session.query(PrivateChat).filter(
                (PrivateChat.user1_id == user_id) | (PrivateChat.user2_id == user_id),
                PrivateChat.is_locked == False
            ).options(
                joinedload(PrivateChat.user1),
                joinedload(PrivateChat.user2)
            ).all()
            
            return {
                "locked_chats": [
                    await get_chat_preview(chat, True) for chat in locked_chats
                ],
                "unlocked_chats": [
                    await get_chat_preview(chat, False) for chat in unlocked_chats
                ]
            }
        
        