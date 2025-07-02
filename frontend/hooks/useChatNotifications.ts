'use client';

import { useEffect } from 'react';
import { useWebSocket } from '@/context/WebSocketContext';

interface ChatNotification {
  type: string;
  message: string;
  chat_id?: number;
  sender_id?: number;
  sender_name?: string;
  content_preview?: string;
  message_type?: string;
  timestamp?: string;
}

interface UseChatNotificationsOptions {
  onNewMessage?: (notification: ChatNotification) => void;
  onNotification?: (notification: ChatNotification) => void;
}

export const useChatNotifications = (options: UseChatNotificationsOptions = {}) => {
  const { notifications, clearNotifications, setOnNewMessage } = useWebSocket();
  const { onNewMessage, onNotification } = options;

  useEffect(() => {
    if (onNewMessage) {
      const handleNewMessage = (notification: ChatNotification) => {
        if (notification.type === 'new_message') {
          onNewMessage(notification);
        }
        if (onNotification) {
          onNotification(notification);
        }
      };
      
      setOnNewMessage(handleNewMessage);
      
      return () => {
        setOnNewMessage(() => {});
      };
    }
  }, [onNewMessage, onNotification, setOnNewMessage]);

  // Filter chat-related notifications
  const chatNotifications = notifications.filter(
    notification => notification.type === 'new_message'
  );

  return {
    notifications: chatNotifications,
    allNotifications: notifications,
    clearNotifications,
    hasUnreadMessages: chatNotifications.length > 0,
  };
};