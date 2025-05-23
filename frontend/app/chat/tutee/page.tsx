"use client";
import AssignmentCard from "@/components/assignmentCard";
import { geistMono, geistSans } from "@/components/layout";
import UserMenu from "@/components/UserMenu";
import { BASE_URL } from "@/utils/constants";
import { motion } from "framer-motion";
import { ArrowLeftToLine, BookPlusIcon, PlusCircle } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { ReactElement, useEffect, useRef, useState } from "react";

const ChatApp = () => {
  type ChatPreview = {
    id: number;
    name: string;
    message: string;
    time: string;
    notifications: number;
  };

  type Number2String = {
    [key: number]: string;
  };

  type Message = {
    id?: number;
    sender: string;
    message: string | ReactElement;
    time: string;
    sentByUser: boolean;
  }

  type ChatHistory = {
    [key: number]: Message[];
  }

  interface ChatData {
    lockedChats: ChatPreview[];
    unlockedChats: ChatPreview[];
    displayNames: Number2String;
    chatHistory: ChatHistory;
  }
  
  const chatData: ChatData = {
    lockedChats: [
      {
        id: 1,
        name: "User 1",
        message: "Hello!",
        time: "Today, 9:52pm",
        notifications: 4,
      },
      {
        id: -1,
        name: "User 2",
        message: "That is true...",
        time: "Yesterday, 12:31pm",
        notifications: 0,
      },
      {
        id: -1,
        name: "User 3",
        message: "It’s not going to happen",
        time: "Wednesday, 9:12am",
        notifications: 0,
      },
    ],
    unlockedChats: [
      {
        id: 2,
        name: "Anil",
        message: "Yes Sure!",
        time: "Today, 9:52pm",
        notifications: 0,
      },
      {
        id: 3,
        name: "Chuutiya",
        message: "That would be great. Thank you!",
        time: "Today, 12:11pm",
        notifications: 1,
      },
      {
        id: -1,
        name: "Mary ma’am",
        message: "Thanks!",
        time: "Today, 2:40pm",
        notifications: 1,
      },
      {
        id: -1,
        name: "Bill Gates",
        message: "Nevermind bro",
        time: "Yesterday, 12:31pm",
        notifications: 5,
      },
      {
        id: -1,
        name: "Victoria H",
        message: "Okay, brother. let’s see...",
        time: "Wednesday, 11:12am",
        notifications: 0,
      },
      {
        id: -1,
        name: "Victoria H",
        message: "Okay, brother. let’s see...",
        time: "Wednesday, 11:12am",
        notifications: 0,
      },
      {
        id: -1,
        name: "Victoria H",
        message: "Okay, brother. let’s see...",
        time: "Wednesday, 11:12am",
        notifications: 0,
      },
    ],
    displayNames: {
      1: "User",
      2: "Anil",
      3: "Parent",
    },
    chatHistory: {
      1: [
        {
          sender: "User",
          message: "Hello!",
          time: "Today, 9:52pm",
          sentByUser: true,
        },
      ],
      2: [
        {
          sender: "Anil",
          message: "Hey there!",
          time: "Today, 9:52pm",
          sentByUser: false,
        },
        {
          sender: "Anil",
          message: "How are you?",
          time: "Today, 9:53pm",
          sentByUser: false,
        },
        {
          sender: "User",
          message: "Hello!",
          time: "Today, 9:54pm",
          sentByUser: true,
        },
        {
          sender: "User",
          message: "I am fine and how are you?",
          time: "Today, 9:55pm",
          sentByUser: true,
        },
      ],
      3: [
        {
          sender: "Parent",
          message: "Hello, I wanted to discuss my child's progress.",
          time: "Today, 10:00am",
          sentByUser: false,
        },
        {
          sender: "Tutor",
          message:
            "Sure! Your child is doing well in mathematics but needs some improvement in writing skills.",
          time: "Today, 10:05am",
          sentByUser: true,
        },
        {
          sender: "Parent",
          message: "That sounds good. What do you suggest for improvement?",
          time: "Today, 10:10am",
          sentByUser: false,
        },
        {
          sender: "Tutor",
          message:
            "Regular practice and reading more structured material can help. I can also provide extra worksheets.",
          time: "Today, 10:15am",
          sentByUser: true,
        },
        {
          sender: "Parent",
          message: "That would be great. Thank you!",
          time: "Today, 10:20am",
          sentByUser: false,
        },
      ],
      0: []
    },
  };
  const router = useRouter();
  const [selectedChat, setSelectedChat] = useState(0);
  type ChatHistoryKeys = keyof typeof chatData.chatHistory;
  const [chatMessages, setChatMessages] = useState<Message[]>(chatData.chatHistory[selectedChat as ChatHistoryKeys]);
  const [newMessage, setNewMessage] = useState("");
  const [showChat, setShowChat] = useState(false);
  const [showDropup, setShowDropup] = useState(false);
  const [lockedChats, setLockedChats] = useState<ChatPreview[]>(chatData.lockedChats);
  const [unlockedChats, setUnlockedChats] = useState<ChatPreview[]>(chatData.unlockedChats);
  const [displayNames, setDisplayNames] = useState<Number2String>(chatData.displayNames);
  const [chatHistory, setChatHistory] = useState<React.SetStateAction<ChatHistory>>(chatData.chatHistory);
  const [chatName, setChatName] = useState<string>("");
  const socketRef = useRef<WebSocket | null>(null);

  // Changing state
  const selectedChatRef = useRef(selectedChat);
  useEffect(() => {
    selectedChatRef.current = selectedChat;
  }, [selectedChat]);

  const chatMessagesRef = useRef(chatMessages);
  useEffect(() => {
    chatMessagesRef.current = chatMessages;
  }, [chatMessages]);

  const chatHistoryRef = useRef(chatHistory);
  useEffect(() => {
    chatHistoryRef.current = chatHistory;
  }, [chatHistory]);

  const fetchChats = async () => {
    try {
      const response = await fetch(`/api/chats`, {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch chats");
      }
      const data = await response.json();
      setLockedChats(data.locked_chats);
      setUnlockedChats(data.unlocked_chats);
      const tmpNames: Number2String = {};
      const setNames = (chats: ChatPreview[]) => chats.forEach((chat: ChatPreview) => {
        tmpNames[chat.id] = chat.name;
      });
      setNames(data.locked_chats);
      setNames(data.unlocked_chats);
      setDisplayNames(tmpNames);
    } catch (error) {
      console.error("Error fetching chats:", error);
    }
  }

  const initWebSocket = async () => {
    const response = await fetch(`/api/chat/jwt`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch JWT");
    }
    const data = await response.json();
    const wsURL = BASE_URL.replace(/^http/, "ws").replace(/\/api/, "");
    const socket = new WebSocket(`${wsURL}/ws/chat?access_token=${data.access_token}`);
    socketRef.current = socket;

    socket.onopen = () => console.log('Connected to WebSocket');

    socket.onmessage = (event) => {
      const text = event.data;
      const parsedData = JSON.parse(text);
      setChatHistory((prevChatHistory: ChatHistory) => {
        const selectedChat = selectedChatRef.current;
        const updatedChatHistory = { ...prevChatHistory };
        const updatedChatMessages = [...updatedChatHistory[selectedChat], ];
        updatedChatMessages.push({
          ...parsedData,
          time: to12HourTime(parsedData.time),
        });
        updatedChatHistory[selectedChat] = updatedChatMessages;
        // Update the Screen
        setChatMessages(updatedChatMessages);
        // Store in javascript browser memory
        return updatedChatHistory;
      });
    };

    socket.onclose = () => console.log('WebSocket closed');
  }

  // Persistent state
  useEffect(() => {
    fetchChats();
    initWebSocket();
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  function to12HourTime(input: string): string {
    // Parse the input date string into a Date object
    const date = new Date(input.replace(/\.(\d{3})\d+$/, '.$1'));
    if (isNaN(date.getTime())) throw new Error("Invalid date");
  
    // Get the timezone offset (in minutes) and adjust the UTC time
    const localOffset = date.getTimezoneOffset(); // Local timezone offset in minutes
    const localDate = new Date(date.getTime() - localOffset * 60000); // Adjust UTC by local timezone offset
  
    // Extract hours, minutes, seconds
    const [h, m, s] = [localDate.getHours(), localDate.getMinutes(), localDate.getSeconds()];
    const hour12 = h % 12 || 12;
    const ampm = h < 12 ? 'AM' : 'PM';
  
    // Return the formatted time
    return `${hour12}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')} ${ampm}`;
  }

  const handleChatSelection = async (chatId: number) => {
    setSelectedChat(chatId);
    setChatName(displayNames[chatId]);
    setShowChat(true);
    setNewMessage("");
    const response = await fetch(`/api/chat/${chatId}`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch chat messages");
    }
    const data = await response.json();

    setChatHistory((prevChatHistory: ChatHistory) => {
      const updatedChatHistory = { ...prevChatHistory };
      const messages = data.messages.map((message: Message) => ({
        ...message,
        time: to12HourTime(message.time),
      }));
      updatedChatHistory[chatId] = messages;
      setChatMessages(messages);
      return updatedChatHistory;
    });
  };

  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
    
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({chat_id: selectedChat, content: newMessage}));
        setChatHistory((prevChatHistory: ChatHistory) => {
          const updatedChatHistory = { ...prevChatHistory };
          const updatedChatMessages = [
            ...updatedChatHistory[selectedChat],
            {
              sender: "User",
              message: newMessage,
              time: new Date().toLocaleTimeString(),
              sentByUser: true,
            },
          ];
          updatedChatHistory[selectedChat] = updatedChatMessages;
          setChatMessages(updatedChatMessages);
          return updatedChatHistory;
        });
        setNewMessage("");
      }
      
    }
  };
  const handleSendAssignment = () => {
    const assignment = (
      <AssignmentCard
        id={4}
        time={"FRI 07:00 PM"}
        title={"P5 Math"}
        location={"662C Jurong West Street 64 643662"}
        duration={"1.5h"}
        price={"$35-45/h"}
        averagePrice={35}
        status={"disabled"}
        level={"Secondary"}
        subject={"Mathematics"}
      ></AssignmentCard>
    );

    setChatMessages([
      ...chatMessages,
      { sender: "User", message: assignment, time: "Now", sentByUser: true },
    ]);
    setShowDropup(false);
  };
  return (
    <div className="flex flex-col min-w-[320px] h-screen">
      <div className="flex flex-1 overflow-hidden bg-customLightYellow">
        {/* Sidebar - Shown on mobile */}
        <aside
          className={`w-full md:w-1/4 p-4 border-r border-gray-200 bg-white shadow-sm ${
            showChat ? "hidden md:block" : "block"
          }`}
        >
          <div
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
          >
            <header id="topbar" className="bg-white">
              <div className="container mx-auto px-4 py-2 sm:py-3 flex items-center justify-between">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className="text-customDarkBlue hover:text-customYellow"
                >
                  <ArrowLeftToLine onClick={() => router.back()} />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link href="/" passHref>
                    <Image
                      src="/images/logo.png"
                      alt="THE Logo"
                      width={60}
                      height={30}
                    />
                  </Link>
                </motion.button>

                <UserMenu />
              </div>
            </header>

            {/* Main Content */}
          </div>
          <div className="flex flex-col flex-grow h-full ">
            <div className="w-full flex"></div>
            <div className="mb-4 p-4 ">
              <input
                type="text"
                placeholder="Search"
                className="w-full px-4 py-2 rounded-3xl border shadow-sm border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              />
            </div>
            <div className="flex-1 mb-6 overflow-y-auto pb-20">
              <div className="bg-white p-2 font-bold sticky top-0 z-10">
                Locked
              </div>
              <div className="space-y-2">
                {lockedChats.map((chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(chat.id)}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                      <div>
                        <p className="font-medium">{chat.name}</p>
                        <p className="text-sm text-gray-500">{chat.message}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">{chat.time}</p>
                      {chat.notifications > 0 && (
                        <span className="text-xs text-white bg-customOrange px-2 py-1 rounded-full">
                          {chat.notifications}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto pb-20">
              <div className="bg-white px-2 py-4 font-bold sticky top-0 z-10">
                Unlocked
              </div>
              <div className="space-y-2">
                {unlockedChats.map((chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(chat.id)}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                      <div>
                        <p className="font-medium">{chat.name}</p>
                        <p className="text-sm text-gray-500">{chat.message}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">{chat.time}</p>
                      {chat.notifications > 0 && (
                        <span className="text-xs text-white bg-customOrange px-2 py-1 rounded-full">
                          {chat.notifications}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Chat Area */}
        <main
          className={`flex-1 p-4 min-w-[320px] ${
            showChat ? "block" : "hidden md:block"
          }`}
        >
          <button
            className="mb-4 p-2 text-sm bg-gray-200 rounded-md md:hidden"
            onClick={() => setShowChat(false)}
          >
            <ArrowLeftToLine size={24} />
          </button>
          <div className="p-4 bg-white rounded-3xl shadow-md h-full flex flex-col">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-gray-300 rounded-full"></div>
              <div className="ml-4">
                <p className="text-lg font-semibold">{chatName}</p>
                {/* <p className="text-sm text-gray-500">Online</p> */}
                <button
                  onClick={async () => {
                    const response = await fetch(`/api/chat/new`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json'
                      },
                      credentials: "include",
                      body: JSON.stringify({
                        other_id: 10
                      })
                    });
                    if (!response.ok) {
                      throw new Error("Failed to create chat");
                    } else {
                      console.log("Chat created successfully");
                    }
                  }}
                  className="p-2 bg-customDarkBlue text-white rounded-3xl hidden md:block"
                >
                  Create Chat
                </button>
              </div>
            </div>
            <div className="flex flex-col justify-end flex-1 border rounded-3xl p-4 bg-gray-50">
              <div className="flex flex-col gap-2 mb-4 overflow-y-auto max-h-[60vh]">
                {chatMessages.map((chat, index) => (
                  <div
                    key={index}
                    className={chat.sentByUser ? "self-end" : "self-start"}
                  >
                    <div
                      className={`p-2 rounded-xl ${
                        chat.sentByUser
                          ? "bg-customDarkBlue text-white"
                          : "bg-gray-300"
                      }`}
                    >
                      {chat.message}
                    </div>
                    <p className="text-xs text-gray-400 mt-1 flex justify-end">
                      {chat.time}
                    </p>
                  </div>
                ))}
              </div>

              <div className="flex items-center gap-2 mt-auto">
                <button
                  className="p-2 bg-gray-300 rounded-full"
                  onClick={() => setShowDropup(!showDropup)}
                >
                  <BookPlusIcon size={24} />
                </button>
                {showDropup && (
                  <div className="absolute mb-28 bg-white shadow-md rounded-lg p-2 w-48">
                    <button
                      className="w-full text-left p-2 hover:bg-gray-100"
                      onClick={handleSendAssignment}
                    >
                      P5 Math
                    </button>
                  </div>
                )}
                <input
                  type="text"
                  placeholder="Type your message here..."
                  className="flex-1 px-4 py-2 rounded-3xl border border-gray-300"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleSendMessage();
                    }
                  }}
                />
                <button
                  onClick={handleSendMessage}
                  className="p-2 bg-customDarkBlue text-white rounded-3xl hidden md:block"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ChatApp;
