from api.router.models import NewChatMessage
from api.storage.models import ChatMessage, ChatRoom
from api.storage.storage_service import StorageService
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


class ChatLogic:

    @staticmethod
    def get_or_create_chatroom(session: Session, user1_id: int, user2_id: int) -> ChatRoom:
        """
        Get an existing chatroom between two users or create a new one if it doesn't exist.
        
        Args:
            session: SQLAlchemy session
            user1_id: ID of the first user
            user2_id: ID of the second user
            
        Returns:
            ChatRoom: The existing or newly created chatroom
        """
        # Check for existing chatroom
        # We need to check both possible user orderings
        existing_chatroom = session.query(ChatRoom).filter(
            or_(
                and_(ChatRoom.user1Id == user1_id, ChatRoom.user2Id == user2_id),
                and_(ChatRoom.user1Id == user2_id, ChatRoom.user2Id == user1_id)
            )
        ).first()
        
        # If a chatroom exists, return it
        if existing_chatroom:
            return existing_chatroom
        
        # Otherwise, create a new chatroom
        new_chatroom = ChatRoom(
            user1Id=user1_id,
            user2Id=user2_id,
            isLocked=False  # Set this according to your requirements
        )

        new_chatroom = StorageService.insert(session, new_chatroom)
        
        return new_chatroom

    @staticmethod
    async def handle_message(active_connections: dict[str|int, WebSocket], new_chat_message: NewChatMessage, from_id: int) -> None:
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
            receiver_id = new_chat_message.receiverId

            # Create a chatroom between the two users if not exists
            chatroom = ChatLogic.get_or_create_chatroom(session, from_id, receiver_id)
            # Check if the chatroom is locked
            if chatroom.isLocked:
                # Do some content filtering
                pass

            # Create a ChatMessage object
            chat_message = ChatMessage(
                content=new_chat_message.content,
                senderId=from_id,
                receiverId=receiver_id,
                chatRoomId=chatroom.id
            )

            # Add the message to the session
            chat_message = StorageService.insert(session, chat_message)

            # Send the message to the receiver via WebSocket
            if receiver_id in active_connections:
                # Send the message to the receiver's WebSocket
                # Ensure that the receiver is connected
                try:
                    await active_connections[receiver_id].send_text(chat_message.content)
                except WebSocketDisconnect:
                    active_connections.pop(receiver_id, None)

    @staticmethod
    def get_chat_history(chat_id: int, user_id: int, last_message_id: int, message_count: int) -> list[ChatMessage]:
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
        with Session(StorageService.engine) as session:
            chatroom = StorageService.find(session, {"id": chat_id}, ChatRoom, find_one=True)
            if chatroom.user1Id != user_id and chatroom.user2Id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to view this chatroom.")
            session.add(chatroom)

            # Get the chat messages
            if last_message_id == -1: last_message_id = float('inf')
            print(f"Getting chat history for user {user_id} with {chatroom.id} up to message ID {last_message_id}")
            chat_messages = session.query(ChatMessage).filter(
                ChatMessage.chatRoomId == chatroom.id,
                ChatMessage.id <= last_message_id
            ).order_by(ChatMessage.timestamp.desc()).limit(message_count).all()
            print(f"Retrieved {len(chat_messages)} messages.")
            return [
                message.to_dict(rules=(
                    "-sender",
                    "-receiver",
                    "-chatRoom",
                )) for message in chat_messages
            ]
        
    @staticmethod
    def unlock_chat(chat_id: int, user_id: int) -> None:
        """
        Unlock chat with a user.

        Args:
            chat_id (int): The ID of the chatroom to unlock.
            user_id (int): The ID of the current user.

        Returns:
            None
        """
        with Session(StorageService.engine) as session:
            chatroom = StorageService.find(session, {"id": chat_id}, ChatRoom, find_one=True)
            if chatroom.user1Id != user_id and chatroom.user2Id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to unlock this chatroom.")
            
            # Unlock the chatroom
            chatroom.isLocked = False
            session.commit()

    @staticmethod
    def mark_messages_as_read(chat_id: int, message_ids: list[int], user_id: int) -> None:
        """
        Mark chat messages as read.

        Args:
            chat_id (int): The ID of the chatroom.
            message_ids (list[int]): List of message IDs to mark as read.
            user_id (int): The ID of the current user.

        Returns:
            None
        """
        with Session(StorageService.engine) as session:
            chatroom = StorageService.find(session, {"id": chat_id}, ChatRoom, find_one=True)
            if chatroom.user1Id != user_id and chatroom.user2Id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to mark messages as read.")
            
            # Mark messages as read in one go
            session.query(ChatMessage).filter(
                ChatMessage.chatRoomId == chatroom.id,
                ChatMessage.id.in_(message_ids)
            ).update({"isRead": True})

            session.commit()
