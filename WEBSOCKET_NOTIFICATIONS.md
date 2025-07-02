# WebSocket Notifications Infrastructure

This document describes the WebSocket notification system built for handling real-time chat notifications between the frontend and backend.

## Architecture Overview

The system consists of two WebSocket connections:
1. **Root WebSocket** (`/ws/notifications`) - For general notifications across the app
2. **Chat WebSocket** (`/ws/chat`) - For real-time chat messaging

## Backend Components

### 1. WebSocket Manager (`backend/api/router/websocket.py`)
- Manages WebSocket connections for notifications
- Handles user authentication via JWT
- Provides methods for sending personal and broadcast notifications
- Endpoint: `/ws/notifications`

### 2. Chat Logic Integration (`backend/api/logic/chat_logic.py`)
- Enhanced to send notifications via root WebSocket when users aren't actively in chat
- Sends structured notification data including:
  - Message type and content preview
  - Sender information
  - Chat ID for navigation
  - Timestamp

### 3. Chat Router (`backend/api/router/chat.py`)
- Handles real-time chat messaging via `/ws/chat`
- Integrates with chat logic for message processing

## Frontend Components

### 1. WebSocket Context (`frontend/context/WebSocketContext.tsx`)
- Manages root WebSocket connection
- Handles authentication and reconnection
- Provides notification state management
- Supports callback registration for new message handling

### 2. Chat Notifications Hook (`frontend/hooks/useChatNotifications.ts`)
- Custom hook for easy integration of chat notifications
- Filters chat-related notifications
- Provides unread message status

### 3. Notification Toast (`frontend/components/NotificationToast.tsx`)
- Displays real-time notifications as toast messages
- Clickable notifications that navigate to relevant chat
- Auto-dismiss functionality
- Support for multiple notifications

### 4. Navigation Integration
- **Layout Component**: Shows red dot badge on Messages tab when unread messages exist
- **Sidebar Component**: Shows notification badge in mobile navigation
- Real-time updates across the entire application

### 5. Chat App Integration (`frontend/app/(appbar)/chat/ChatApp.tsx`)
- Listens for notifications from root WebSocket
- Updates chat list with unread status
- Creates new chat threads from notifications
- Handles both active chat WebSocket and notification WebSocket

## Notification Flow

### When a message is sent:

1. **Sender** sends message via chat WebSocket (`/ws/chat`)
2. **Backend** processes message in `ChatLogic.handle_private_message()`
3. **Backend** sends message to receiver via chat WebSocket (if connected)
4. **Backend** sends notification via root WebSocket (if receiver not in chat)
5. **Frontend** receives notification and:
   - Shows toast notification
   - Updates navigation badge
   - Updates chat list with unread status

### Notification Structure:
```json
{
  "type": "new_message",
  "message": "New message from John Doe",
  "chat_id": 123,
  "sender_id": 456,
  "sender_name": "John Doe",
  "content_preview": "Hey, are you available for...",
  "message_type": "text_message",
  "timestamp": "2025-02-07T08:55:00Z"
}
```

## Key Features

### ✅ Real-time Notifications
- Instant notifications when messages are received
- Works even when user is not on chat page

### ✅ Smart Notification Logic
- Only sends notifications if user is not actively in the chat
- Prevents duplicate notifications

### ✅ Visual Indicators
- Red dot badges on navigation items
- Toast notifications with click-to-navigate
- Unread message counts in chat list

### ✅ Cross-Platform Support
- Works on both desktop and mobile
- Responsive notification positioning

### ✅ Robust Connection Management
- Automatic reconnection on connection loss
- JWT-based authentication
- Graceful error handling

## Testing

### Test Page
Visit `/test-notifications` to:
- Check WebSocket connection status
- View current notifications
- Clear notifications
- See testing instructions

### Manual Testing Steps
1. Open two browser windows with different user accounts
2. Send a message from User A to User B
3. In User B's window, verify:
   - Toast notification appears
   - Red dot appears on Messages tab
   - Notification shows in test page
4. Click notification to navigate to chat
5. Verify red dot disappears when chat is viewed

## Configuration

### Environment Variables
- WebSocket connections use the same base URL as API calls
- JWT authentication handled automatically via existing auth system

### WebSocket Endpoints
- **Notifications**: `ws://localhost:8000/ws/notifications?access_token=<jwt>`
- **Chat**: `ws://localhost:8000/ws/chat?access_token=<jwt>`

## Usage Examples

### Using the Chat Notifications Hook
```tsx
import { useChatNotifications } from '@/hooks/useChatNotifications';

function MyComponent() {
  const { hasUnreadMessages, notifications, clearNotifications } = useChatNotifications({
    onNewMessage: (notification) => {
      console.log('New message received:', notification);
    }
  });

  return (
    <div>
      {hasUnreadMessages && <span className="notification-badge" />}
      <button onClick={clearNotifications}>Clear All</button>
    </div>
  );
}
```

### Using WebSocket Context Directly
```tsx
import { useWebSocket } from '@/context/WebSocketContext';

function MyComponent() {
  const { socket, notifications, setOnNewMessage } = useWebSocket();

  useEffect(() => {
    setOnNewMessage((notification) => {
      if (notification.type === 'new_message') {
        // Handle new message notification
      }
    });
  }, [setOnNewMessage]);
}
```

## Future Enhancements

- [ ] Push notifications for mobile devices
- [ ] Sound notifications
- [ ] Notification preferences/settings
- [ ] Message read receipts
- [ ] Typing indicators
- [ ] Group chat notifications
- [ ] Notification history/persistence

## Troubleshooting

### Common Issues

1. **WebSocket not connecting**
   - Check if backend server is running
   - Verify JWT token is valid
   - Check browser console for errors

2. **Notifications not appearing**
   - Verify WebSocket connection is established
   - Check if user is authenticated
   - Ensure notification toast component is rendered

3. **Duplicate notifications**
   - Check if multiple WebSocket connections are being created
   - Verify cleanup in useEffect hooks

### Debug Tools
- Use `/test-notifications` page to monitor connection status
- Check browser developer tools WebSocket tab
- Monitor backend logs for WebSocket connection events