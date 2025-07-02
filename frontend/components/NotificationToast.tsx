'use client';

import React, { useEffect, useState } from 'react';
import { useWebSocket } from '@/context/WebSocketContext';
import { X, MessageCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface NotificationToastProps {
  maxNotifications?: number;
  autoHideDuration?: number;
}

const NotificationToast: React.FC<NotificationToastProps> = ({ 
  maxNotifications = 3, 
  autoHideDuration = 5000 
}) => {
  const { notifications, clearNotifications } = useWebSocket();
  const [visibleNotifications, setVisibleNotifications] = useState<typeof notifications>([]);
  const router = useRouter();

  useEffect(() => {
    // Show only the most recent notifications
    const recentNotifications = notifications.slice(-maxNotifications);
    setVisibleNotifications(recentNotifications);

    // Auto-hide notifications after specified duration
    if (recentNotifications.length > 0) {
      const timer = setTimeout(() => {
        clearNotifications();
        setVisibleNotifications([]);
      }, autoHideDuration);

      return () => clearTimeout(timer);
    }
  }, [notifications, maxNotifications, autoHideDuration, clearNotifications]);

  const handleNotificationClick = (notification: any) => {
    if (notification.type === 'new_message' && notification.chat_id) {
      router.push(`/chat?chatId=${notification.chat_id}`);
      clearNotifications();
      setVisibleNotifications([]);
    }
  };

  const handleDismiss = (index: number) => {
    setVisibleNotifications(prev => prev.filter((_, i) => i !== index));
  };

  const handleDismissAll = () => {
    clearNotifications();
    setVisibleNotifications([]);
  };

  if (visibleNotifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {visibleNotifications.map((notification, index) => (
        <div
          key={`${notification.timestamp}-${index}`}
          className="bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-sm cursor-pointer hover:shadow-xl transition-shadow duration-200"
          onClick={() => handleNotificationClick(notification)}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <div className="flex-shrink-0">
                {notification.type === 'new_message' ? (
                  <MessageCircle className="h-6 w-6 text-blue-500" />
                ) : (
                  <div className="h-6 w-6 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-xs font-bold">!</span>
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  {notification.message}
                </p>
                {notification.content_preview && (
                  <p className="text-sm text-gray-500 mt-1 truncate">
                    {notification.content_preview}
                  </p>
                )}
                {notification.timestamp && (
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(notification.timestamp).toLocaleTimeString()}
                  </p>
                )}
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDismiss(index);
              }}
              className="flex-shrink-0 ml-2 text-gray-400 hover:text-gray-600"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      ))}
      
      {visibleNotifications.length > 1 && (
        <div className="flex justify-end">
          <button
            onClick={handleDismissAll}
            className="text-xs text-gray-500 hover:text-gray-700 bg-white border border-gray-200 rounded px-2 py-1"
          >
            Dismiss all
          </button>
        </div>
      )}
    </div>
  );
};

export default NotificationToast;