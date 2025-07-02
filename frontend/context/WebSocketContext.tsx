'use client';

import React, { createContext, useContext, useEffect, useState, useRef } from 'react';
import { useAuth } from './authContext';
import { fetchWithTokenCheck } from '@/utils/tokenVersionMismatch';
import { BASE_URL } from '@/utils/constants';
import logger from '@/utils/logger';

interface Notification {
  type: string;
  message: string;
  chat_id?: number;
  sender_id?: number;
  sender_name?: string;
  content_preview?: string;
  message_type?: string;
  timestamp?: string;
}

interface WebSocketContextType {
  socket: WebSocket | null;
  notifications: Notification[];
  clearNotifications: () => void;
  onNewMessage?: (notification: Notification) => void;
  setOnNewMessage: (callback?: (notification: Notification) => void) => void;
}

const WebSocketContext = createContext<WebSocketContextType>({
  socket: null,
  notifications: [],
  clearNotifications: () => {},
  setOnNewMessage: () => {}
});

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [onNewMessage, setOnNewMessage] = useState<((notification: Notification) => void) | undefined>();
  const { user, loading } = useAuth();
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const isIntentionallyClosedRef = useRef(false);

  const clearNotifications = () => {
    setNotifications([]);
  };

  const handleSetOnNewMessage = (callback?: (notification: Notification) => void) => {
    setOnNewMessage(callback);
  };

  const initWebSocket = async () => {
    
    // Clear any pending reconnection timeout
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    // Close existing socket if any
    if (socketRef.current) {
      isIntentionallyClosedRef.current = true;
      socketRef.current.close();
    }
    
    try {
      const response = await fetchWithTokenCheck(`/api/ws/jwt`, {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch JWT");
      }
      const data = await response.json();
      const wsURL = BASE_URL.replace(/^http/, "ws").replace(/\/api/, "");
      
      const newSocket = new WebSocket(
        `${wsURL}/ws/notifications?access_token=${data.access_token}`
      );
      
      newSocket.onopen = () => {
        socketRef.current = newSocket;
        setSocket(newSocket);
        isIntentionallyClosedRef.current = false;
      };

      newSocket.onmessage = (event) => {
        try {
          const notification: Notification = JSON.parse(event.data);
          setNotifications(prev => [...prev, notification]);
          
          // Handle new message notifications
          if (notification.type === 'new_message' && onNewMessage) {
            onNewMessage(notification);
          }
        } catch (error) {
          logger.error('WebSocketContext: Failed to parse notification:', event.data);
        }
      };

      newSocket.onclose = (event) => {
        
        // Only clear socket state if this is the current socket
        if (socketRef.current === newSocket) {
          socketRef.current = null;
          setSocket(null);
        }
        
        // Only reconnect if:
        // 1. User is authenticated and not loading
        // 2. Connection was not intentionally closed
        // 3. No reconnection timeout is already scheduled
        if (user && !loading && !isIntentionallyClosedRef.current && !reconnectTimeoutRef.current) {
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectTimeoutRef.current = null;
            if (user && !loading && !socketRef.current) {
              initWebSocket();
            }
          }, 5000);
        }
      };

      newSocket.onerror = (error) => {
        logger.error("WebSocketContext: WebSocket error occurred", error);
      };
    } catch (error) {
      logger.error("WebSocketContext: Failed to initialize WebSocket:", error);
    }
  };

  useEffect(() => {
    
    if (user && !loading) {
      initWebSocket();
    }

    return () => {
      if (socketRef.current) {
        isIntentionallyClosedRef.current = true;
        socketRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
        reconnectTimeoutRef.current = null;
      }
    };
  }, [user, loading]);

  return (
    <WebSocketContext.Provider value={{
      socket,
      notifications,
      clearNotifications,
      onNewMessage,
      setOnNewMessage: handleSetOnNewMessage
    }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);