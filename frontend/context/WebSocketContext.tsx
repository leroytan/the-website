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
  const hasInitializedSocket = useRef(false);

  const clearNotifications = () => {
    setNotifications([]);
  };

  const initWebSocket = async () => {
    try {
      const response = await fetchWithTokenCheck(`/api/ws/jwt`, {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch JWT");
      }
      const data = await response.json();
      const wsURL = BASE_URL.replace(/^http/, "ws").replace(/\/api/, "");
      console.log(`Connecting to WebSocket at ${wsURL}/ws/notifications?access_token=${data.access_token}`);
      const newSocket = new WebSocket(
        `${wsURL}/ws/notifications?access_token=${data.access_token}`
      );
      socketRef.current = newSocket;
      setSocket(newSocket);

      newSocket.onopen = () => console.log("Connected to Notifications WebSocket");

      newSocket.onmessage = (event) => {
        try {
          const notification: Notification = JSON.parse(event.data);
          setNotifications(prev => [...prev, notification]);
        } catch (error) {
          console.error('Failed to parse notification:', event.data);
        }
      };

      newSocket.onclose = () => {
        socketRef.current = null;
        setSocket(null);
        console.log("Notifications WebSocket closed");
      };
    } catch (error) {
      console.error("Failed to initialize WebSocket:", error);
    }
  };

  useEffect(() => {
    // Only attempt WebSocket connection if user is authenticated and not loading
    if (!user || loading) return;

    if (!hasInitializedSocket.current) {
      initWebSocket();
      hasInitializedSocket.current = true;
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