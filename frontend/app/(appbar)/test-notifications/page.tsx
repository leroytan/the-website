'use client';

import React, { useState } from 'react';
import { useChatNotifications } from '@/hooks/useChatNotifications';
import { useWebSocket } from '@/context/WebSocketContext';

const TestNotificationsPage = () => {
  const { notifications, hasUnreadMessages, clearNotifications } = useChatNotifications();
  const { socket } = useWebSocket();
  const [testMessage, setTestMessage] = useState('');

  const sendTestNotification = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      const testNotification = {
        type: 'new_message',
        message: testMessage || 'Test notification',
        chat_id: 1,
        sender_id: 999,
        sender_name: 'Test User',
        content_preview: testMessage || 'This is a test message',
        message_type: 'text_message',
        timestamp: new Date().toISOString()
      };
      
      // Note: This won't actually work since the WebSocket is for receiving only
      // This is just for demonstration of the notification structure
      console.log('Would send:', testNotification);
      alert('This is a test page. In real usage, notifications come from the backend when messages are sent.');
    } else {
      alert('WebSocket not connected');
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">WebSocket Notification Test</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Connection Status */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Connection Status</h2>
          <div className="space-y-2">
            <p>
              <span className="font-medium">WebSocket Status:</span>{' '}
              <span className={`px-2 py-1 rounded text-sm ${
                socket?.readyState === WebSocket.OPEN 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {socket?.readyState === WebSocket.OPEN ? 'Connected' : 'Disconnected'}
              </span>
            </p>
            <p>
              <span className="font-medium">Has Unread Messages:</span>{' '}
              <span className={`px-2 py-1 rounded text-sm ${
                hasUnreadMessages 
                  ? 'bg-orange-100 text-orange-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {hasUnreadMessages ? 'Yes' : 'No'}
              </span>
            </p>
          </div>
        </div>

        {/* Test Controls */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Test Controls</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Test Message</label>
              <input
                type="text"
                value={testMessage}
                onChange={(e) => setTestMessage(e.target.value)}
                placeholder="Enter test message"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={sendTestNotification}
              className="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
            >
              Test Notification (Demo Only)
            </button>
            <button
              onClick={clearNotifications}
              className="w-full bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 transition-colors"
            >
              Clear Notifications
            </button>
          </div>
        </div>
      </div>

      {/* Current Notifications */}
      <div className="mt-6 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Current Notifications ({notifications.length})</h2>
        {notifications.length === 0 ? (
          <p className="text-gray-500">No notifications</p>
        ) : (
          <div className="space-y-3">
            {notifications.map((notification, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-medium text-blue-600">{notification.type}</span>
                  <span className="text-xs text-gray-500">
                    {notification.timestamp ? new Date(notification.timestamp).toLocaleTimeString() : 'No timestamp'}
                  </span>
                </div>
                <p className="text-gray-800 mb-1">{notification.message}</p>
                {notification.content_preview && (
                  <p className="text-sm text-gray-600 italic">"{notification.content_preview}"</p>
                )}
                <div className="mt-2 text-xs text-gray-500">
                  Chat ID: {notification.chat_id} | Sender: {notification.sender_name}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 bg-blue-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">How to Test</h2>
        <ol className="list-decimal list-inside space-y-2 text-sm">
          <li>Open two browser windows/tabs with different user accounts</li>
          <li>In one window, go to the chat page and send a message to the other user</li>
          <li>In the other window (where the message recipient is), you should see:
            <ul className="list-disc list-inside ml-4 mt-1">
              <li>A notification toast appear in the top-right corner</li>
              <li>A red dot appear on the Messages tab in the navigation</li>
              <li>The notification appear in this test page</li>
            </ul>
          </li>
          <li>Click on the notification toast to navigate to the chat</li>
          <li>The red dot should disappear when you view the chat</li>
        </ol>
      </div>
    </div>
  );
};

export default TestNotificationsPage;