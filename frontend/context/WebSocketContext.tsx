'use client';

import React, { createContext, useContext, useEffect, useState, useRef } from 'react';
import { useAuth } from './authContext';
import { fetchWithTokenCheck } from '@/utils/tokenVersionMismatch';
import { BASE_URL } from '@/utils/constants';

interface Notification {
  type: string;
  message: string;
}

interface WebSocketContextType {
  socket: WebSocket | null;
  notifications: Notification[];
  clearNotifications: () => void;
}

const WebSocketContext = createContext<WebSocketContextType>({
  socket: null,
  notifications: [],
  clearNotifications: () => {}
});

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const { user, loading } = useAuth();
  const socketRef = useRef<WebSocket | null>(null);

  const clearNotifications = () => {
    setNotifications([]);
  };

  const initWebSocket = async () => {
    // Close existing socket if any
    if (socketRef.current) {
      socketRef.current.close();
    }
    return
    
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
        console.log("Connected to Notifications WebSocket");
        socketRef.current = newSocket;
        setSocket(newSocket);
      };

      newSocket.onmessage = (event) => {
        try {
          const notification: Notification = JSON.parse(event.data);
          setNotifications(prev => [...prev, notification]);
        } catch (error) {
          console.error('Failed to parse notification:', event.data);
        }
      };

      newSocket.onclose = (event) => {
        console.log("Notifications WebSocket closed", event.reason);
        socketRef.current = null;
        setSocket(null);
        
        // Reconnection strategy with backoff
        if (user && !loading) {
          setTimeout(initWebSocket, 5000); // Retry after 5 seconds
        }
      };
    } catch (error) {
      console.error("Failed to initialize WebSocket:", error);
    }
  };

  useEffect(() => {
    if (user && !loading) {
      initWebSocket();
    }

    return () => {
      socketRef.current?.close();
    };
  }, [user, loading]);

  return (
    <WebSocketContext.Provider value={{ socket, notifications, clearNotifications }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);