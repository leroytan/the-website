"use client";
import AssignmentCard from "@/components/assignmentCard";
import { geistMono, geistSans } from "@/components/layout";
import UserMenu from "@/components/UserMenu";
import { BASE_URL } from "@/utils/constants";
import { timeAgo, to12HourTime } from "@/utils/date";
import { motion } from "framer-motion";
import { ArrowLeftToLine, BookPlusIcon, PlusCircle } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import React, { ReactElement, useEffect, useRef, useState } from "react";

const ChatApp = () => {

  class ChatThread {
    private id: number;
    private isLocked: boolean; // true if the chat is locked, false if unlocked
    private title: string;
    private messages: Message[];
    private initialPreview: ChatPreview;
    public hasMoreMessages: boolean = true; // true if there are more messages to load, false if no more messages
    public hasUnreadMessages: boolean = false; // true if there are unread messages, false if no unread messages

    static fromPreviewDTO(dto: ChatPreviewBackendDTO): ChatThread {
      const messages: Message[] = []; // Initialize with an empty array
      const preview = dto.has_messages ? {
        id: dto.id,
        name: dto.name,
        lastMessage: dto.last_message,
        displayTime: timeAgo(dto.last_update),
        hasUnread: dto.has_unread,
        isLocked: dto.is_locked,
        hasMessages: dto.has_messages,
        lastUpdate: new Date(dto.last_update),
        lastMessageType: dto.last_message_type === "text_message" ? "textMessage" : "tutorRequest",
      } : null;
      return new ChatThread(
        dto.id,
        dto.is_locked,
        dto.name,
        messages,
        preview,
      );
    }

    static fromMessageDTO(dto: MessageBackendDTO): ChatThread {
      const messages: Message[] = [{
        id: dto.id,
        sender: dto.sender,
        content: dto.content,
        type: dto.message_type === "text_message" ? "textMessage" : "tutorRequest",
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
        sentByUser: dto.sent_by_user,
      }];
      // Ideally, these fields should be emitted by the backend when creating a new chat
      // For now, we assume the chat is locked and the sender is the first message's sender
      const isLocked = true; // new chats are locked by default
      const sender = dto.sender; // the sender of the first message
      return new ChatThread(dto.chat_id, isLocked, sender, messages);
    }

    constructor(id: number, isLocked: boolean, title: string = "Select a chat", messages: Message[] = [], initialPreview: ChatPreview | null = null) {
      this.id = id;
      this.isLocked = isLocked;
      this.title = title;
      this.messages = messages;
      this.initialPreview = initialPreview || {
        id: id,
        name: title,
        lastMessage: "No messages yet",
        displayTime: "",
        hasUnread: false,
        isLocked: isLocked,
        hasMessages: false,
        lastUpdate: new Date(),
        lastMessageType: "text_message", // Default for new chats
      };
      this.hasMoreMessages = this.initialPreview.hasMessages;
      this.hasUnreadMessages = this.initialPreview.hasUnread;
    }

    getDisplayMessages(): MessageDisplay[] {
      return this.messages.map((message) => ({
        sender: message.sender,
        content: message.content,
        type: message.type,
        time: to12HourTime(message.createdAt),
        sentByUser: message.sentByUser,
      }));
    }

    getTitle(): string {
      return this.title;
    }

    getLatestMessage(): Message | null {
      return this.messages.length > 0 ? this.messages[this.messages.length - 1] : null;
    }

    getEarliestMessageCreated(): string | null {
      const earliestMessage = this.messages.length > 0 ? this.messages[0] : null;
      return earliestMessage ? earliestMessage.createdAt : null;
    }

    private convertSortMessages(messages: MessageBackendDTO[]): Message[] {
      return messages.map((msg) => ({
        id: msg.id,
        sender: msg.sender,
        content: msg.content,
        type: msg.message_type === "text_message" ? "textMessage" : "tutorRequest",
        createdAt: msg.created_at,
        updatedAt: msg.updated_at,
        sentByUser: msg.sent_by_user,
      })).sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
    }

    addRecentMessage(message: MessageBackendDTO): void {
      this.messages.push(...this.convertSortMessages([message]));
    }

    addHistoricalMessages(messages: MessageBackendDTO[]): void {
      const newMessages = this.convertSortMessages(messages);
      this.messages.unshift(...newMessages);
    }

    getPreview(): ChatPreview {
      const latestMessage = this.getLatestMessage();
      if (latestMessage === null) {
        if (this.initialPreview.lastMessageType === "tutorRequest") {
          this.initialPreview.lastMessage = (<i>Tutor Request</i>);
        }
        return this.initialPreview;
      }

      let lastMessageContent: string | ReactElement = latestMessage.content;
      if (latestMessage.type === "tutorRequest") {
        lastMessageContent = (<i>Tutor Request</i>);
      }

      return {
        id: this.id,
        name: this.title,
        lastMessage: lastMessageContent,
        displayTime: timeAgo(latestMessage.createdAt),
        hasUnread: this.hasUnreadMessages,
        isLocked: this.isLocked,
        hasMessages: this.messages.length > 0,
        lastUpdate: new Date(latestMessage.createdAt),
        lastMessageType: latestMessage.type,
      };
    }

    clone(): ChatThread {
      const copiedMessages = this.messages.map((msg) => ({
        id: msg.id,
        sender: msg.sender,
        content: msg.content,
        type: msg.type,
        createdAt: msg.createdAt,
        updatedAt: msg.updatedAt,
        sentByUser: msg.sentByUser,
      }));
      const copiedPreview = this.initialPreview
        ? { ...this.initialPreview }
        : null;

      const newThread = new ChatThread(
        this.id,
        this.isLocked,
        this.title,
        copiedMessages,
        copiedPreview
      );

      return newThread;
    }
  }

  interface ChatData {
    [key: number]: ChatThread;
  }

  type ChatPreviewBackendDTO = {
    id: number;                    // Needed for navigation or fetching full chat
    name: string;                  // Display name (user or group)
    last_message: string;          // Plain text version of the latest message
    last_update: string;           // ISO 8601 string for sorting and display
    last_message_type: string;     // "text_message" or "tutor_request"
    has_unread: boolean;          // For notification badge
    is_locked: boolean;           // Optional security/status flag
    has_messages: boolean;         // If chat is empty, hide or style differently
  };

  type ChatPreview = {
    id: number;
    name: string;
    lastMessage: string | ReactElement; // The latest message content, can be a string or React element
    displayTime: string;
    hasUnread: boolean;
    isLocked?: boolean; // true if the chat is locked, false if unlocked
    hasMessages: boolean; // true if the chat has messages, false if no messages
    lastUpdate: Date; // Date object for sorting and display
    lastMessageType: string; // "textMessage" or "tutorRequest"
  };

  type MessageBackendDTO = {
    id: number;
    chat_id: number;
    sender: string;
    content: string;
    message_type: string; // "text_message" or "tutor_request"
    created_at: string; // ISO 8601 format
    updated_at: string; // ISO 8601 format
    sent_by_user: boolean; // true if sent by the user, false if sent by the other party
  }

  type TutorRequest = {
    type: "tutor_request";
    hourlyRate: number;
    lessonDuration: number;
  };

  type Message = {
    id: number;
    sender: string;
    content: string | ReactElement;
    type: string; // "textMessage" or "tutorRequest"
    createdAt: string; // ISO 8601 format
    updatedAt: string; // ISO 8601 format
    sentByUser: boolean; // true if sent by the user, false if sent by the other party
  }

  type MessageDisplay = {
    sender: string;
    content: string | ReactElement;
    type: string; // "textMessage" or "tutorRequest"
    time: string;
    sentByUser: boolean;
  };

  const messageDTOsForAlice: MessageBackendDTO[] = [
    {
      id: 1,
      chat_id: 1,
      sender: "Alice",
      content: "Hey! Are you free later?",
      message_type: "text_message",
      created_at: new Date(Date.now() - 3600000).toISOString(), // 1h ago
      updated_at: new Date(Date.now() - 3600000).toISOString(),
      sent_by_user: false,
    },
    {
      id: 2,
      chat_id: 1,
      sender: "You",
      content: "Yeah, after 5 works!",
      message_type: "text_message",
      created_at: new Date(Date.now() - 3500000).toISOString(),
      updated_at: new Date(Date.now() - 3500000).toISOString(),
      sent_by_user: true,
    },
    {
      id: 3,
      chat_id: 1,
      sender: "Alice",
      content: "Perfect, see you then.",
      message_type: "text_message",
      created_at: new Date(Date.now() - 3400000).toISOString(),
      updated_at: new Date(Date.now() - 3400000).toISOString(),
      sent_by_user: false,
    },
  ];

  const messageDTOsForBob: MessageBackendDTO[] = [
    {
      id: 4,
      chat_id: 2,
      sender: "You",
      content: "Hey Bob, sent the docs over.",
      message_type: "text_message",
      created_at: new Date(Date.now() - 7200000).toISOString(), // 2h ago
      updated_at: new Date(Date.now() - 7200000).toISOString(),
      sent_by_user: true,
    },
    {
      id: 5,
      chat_id: 2,
      sender: "Bob",
      content: "Awesome, reviewing now.",
      message_type: "text_message",
      created_at: new Date(Date.now() - 7100000).toISOString(),
      updated_at: new Date(Date.now() - 7100000).toISOString(),
      sent_by_user: false,
    },
  ];

  const messageDTOsForCharlie: MessageBackendDTO[] = [
    {
      id: 6,
      chat_id: 3,
      sender: "Charlie",
      content: "Lunch today?",
      message_type: "text_message",
      created_at: new Date(Date.now() - 10800000).toISOString(), // 3h ago
      updated_at: new Date(Date.now() - 10800000).toISOString(),
      sent_by_user: false,
    }
  ];

  const initialChatData: ChatData = {
    1: (() => {
      const thread = new ChatThread(1, false, "Alice");
      thread.addHistoricalMessages(messageDTOsForAlice);
      return thread;
    })(),
    2: (() => {
      const thread = new ChatThread(2, false, "Bob");
      thread.addHistoricalMessages(messageDTOsForBob);
      return thread;
    })(),
    3: (() => {
      const thread = new ChatThread(3, true, "Charlie");
      thread.addHistoricalMessages(messageDTOsForCharlie);
      return thread;
    })(),
  };

  const searchParams = useSearchParams();
  const router = useRouter();
  const [selectedChat, setSelectedChat] = useState(1);
  const [newMessage, setNewMessage] = useState("");
  const [showChat, setShowChat] = useState(false);
  const [showDropup, setShowDropup] = useState(false);

  const [chatData, setChatData] = useState<ChatData>(initialChatData);

  const chatMessages = chatData[selectedChat]?.getDisplayMessages() || [];
  const chatPreviews: ChatPreview[] = Object.values(chatData).map((chat) => chat.getPreview()).sort((a, b) => a.lastUpdate.getTime() - b.lastUpdate.getTime()).reverse();
  const lockedChats = chatPreviews.filter((chat) => chat.isLocked);
  const unlockedChats = chatPreviews.filter((chat) => !chat.isLocked);
  const chatName = chatData[selectedChat]?.getTitle() || "Select a chat";

  useEffect(() => {
    // Check if the URL has the `param` query parameter
    const chatId = searchParams.get(`chatId`);
    if (chatId) {
      setSelectedChat(Number(chatId)); // Set the selected chat based on the query param
      setShowChat(true); // Show the chat area if a chat is selected
    }
  }, [searchParams]); // Re-run this effect when the query param changes


  const socketRef = useRef<WebSocket | null>(null);

  const fetchChats = async () => {
    try {
      const response = await fetch(`/api/chats`, {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch chats");
      }
      const data = await response.json();
      const tmpChatData: ChatData = {};
      data.chats.map((chat: ChatPreviewBackendDTO) => {
        const chatThread = ChatThread.fromPreviewDTO(chat);
        tmpChatData[chat.id] = chatThread;
      });
      setChatData(tmpChatData);
    } catch (error) {
      console.error("Error fetching chats:", error);
    }
  };

  const fetchHistoricalMessages = async (chatId: number) => {
    const container = scrollRef.current;
    if (!container) {
      console.error("Scroll container not found");
      return;
    }

    const existingThread = chatData[chatId] || new ChatThread(chatId, false);
    if (!existingThread.hasMoreMessages) {
      return;
    }

    const previousScrollHeight = container.scrollHeight;

    try {
      const createdBefore = existingThread.getEarliestMessageCreated();
      const params = new URLSearchParams({ limit: "10" });
      if (createdBefore) {
        params.append("created_before", createdBefore);
      }

      const response = await fetch(`/api/chat/${chatId}?${params}`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to fetch chat messages");
      }

      const data = await response.json();

      // Apply update inside setChatData
      setChatData((prevChatData) => {
        const updatedThread = prevChatData[chatId]?.clone() || new ChatThread(chatId, false);
        updatedThread.addHistoricalMessages(data.messages);
        updatedThread.hasMoreMessages = data.has_more;

        return {
          ...prevChatData,
          [chatId]: updatedThread,
        };
      });

      // Restore scroll position
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          const newScrollHeight = container.scrollHeight;
          const scrollDifference = newScrollHeight - previousScrollHeight;
          container.scrollTop = scrollDifference;
        });
      });
    } catch (error) {
      console.error("Error fetching chat messages:", error);
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [selectedChat]);

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (scrollRef.current?.scrollTop === 0) {
        fetchHistoricalMessages(selectedChat); // call the async function
      }
    };

    const scrollContainer = scrollRef.current;
    scrollContainer?.addEventListener("scroll", handleScroll);

    return () => {
      scrollContainer?.removeEventListener("scroll", handleScroll);
    };
  }, [fetchHistoricalMessages]);

  const selectedChatRef = useRef(selectedChat);
  useEffect(() => {
    selectedChatRef.current = selectedChat;
  }, [selectedChat]);

  const lastUpdatedChatRef = useRef<number | null>(null);
  useEffect(() => {
    if (lastUpdatedChatRef.current === selectedChat) {
      scrollToBottom();
      lastUpdatedChatRef.current = null; // reset after scrolling
    }
  }, [chatData, selectedChat]);

  const initWebSocket = async () => {
    const response = await fetch(`/api/chat/jwt`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch JWT");
    }
    const data = await response.json();
    const wsURL = BASE_URL.replace(/^http/, "ws").replace(/\/api/, "");
    console.log(`Connecting to WebSocket at ${wsURL}/ws/chat?access_token=${data.access_token}`);
    const socket = new WebSocket(
      `${wsURL}/ws/chat?access_token=${data.access_token}`
    );
    socketRef.current = socket;

    socket.onopen = () => console.log("Connected to WebSocket");

    socket.onmessage = (event) => {
      const parsedData: MessageBackendDTO = JSON.parse(event.data);
      setChatData((prevChatData: ChatData) => {
        const chatId = parsedData.chat_id;
        lastUpdatedChatRef.current = chatId; // Update the last updated chat reference
        const chatThread = prevChatData[chatId]?.clone() || ChatThread.fromMessageDTO(parsedData);
        chatThread.addRecentMessage(parsedData);
        chatThread.hasUnreadMessages = !parsedData.sent_by_user;
        return {
          ...prevChatData,
          [chatId]: chatThread,
        };
      });
    };

    socket.onclose = () => {
      socketRef.current = null;
      console.log("WebSocket closed");
    }
  };

  const hasInitializedSocket = useRef(false);

  // Persistent state
  useEffect(() => {
    if (!hasInitializedSocket.current) {
      fetchChats();
      initWebSocket();
      hasInitializedSocket.current = true;
    }
    return () => socketRef.current?.close();
  }, []);

  const handleChatSelection = async (chatId: number) => {
    setSelectedChat(chatId);
    setShowChat(true);
    setNewMessage("");
    if (chatMessages.length < 10) {
      fetchHistoricalMessages(chatId);
    }
    const response = await fetch(`/api/chat/${chatId}/read`, {
      method: "POST",
      credentials: "include",
    });
    if (!response.ok) {
      console.error("Failed to mark chat as read");
    }
    setChatData((prevChatData) => {
      const updatedThread = prevChatData[chatId]?.clone() || new ChatThread(chatId, false);
      updatedThread.hasUnreadMessages = false; // Mark as read
      return {
        ...prevChatData,
        [chatId]: updatedThread,
      };
    });
  };

  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
      if (
        socketRef.current &&
        socketRef.current.readyState === WebSocket.OPEN
      ) {
        socketRef.current.send(
          JSON.stringify({ chat_id: selectedChat, content: newMessage })
        );
        setNewMessage("");
      }
    }
  };

  const handleSendAssignment = () => {
    const assignment = (
      <AssignmentCard
        title={""}
        location={""}
        estimated_rate_hourly={0}
        weekly_frequency={0}
        available_slots={[]}
        special_requests={""}
        subjects={[]}
        level={""}
      ></AssignmentCard>
    );
    setShowDropup(false);
  };

  const inputRef = useRef<HTMLInputElement>(null);

  const handleOverlayClick = () => {
    if (inputRef.current) {
      inputRef.current.focus(); // Focus the input when the parent is clicked
    }
  };
  return (
    <div className="flex flex-col min-w-[320px] h-screen">
      <div className="flex flex-1 overflow-hidden bg-customLightYellow">
        {/* Sidebar - Shown on mobile */}
        <aside
          className={`w-full md:w-1/4 p-4 border-r border-gray-200 bg-white shadow-sm ${showChat ? "hidden md:block" : "block"
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
                {lockedChats.map((preview, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(preview.id)}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                      <div>
                        <p className="font-medium">{preview.name}</p>
                        <p className="text-sm text-gray-500">{preview.lastMessage}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">{preview.displayTime}</p>
                      {preview.hasUnread && (
                        <span className="text-xs text-white bg-customOrange px-2 py-1 rounded-full">
                          {/* {preview.unreadCount} */}
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
                {unlockedChats.map((preview, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(preview.id)}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                      <div>
                        <p className="font-medium">{preview.name}</p>
                        <p className="text-sm text-gray-500">{preview.lastMessage}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">{preview.displayTime}</p>
                      {preview.hasUnread && (
                        <span className="text-xs text-white bg-customOrange px-2 py-1 rounded-full">
                          {/* {chat.unreadCount} */}
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
          className={`flex-1 p-4 min-w-[320px] ${showChat ? "block" : "hidden md:block"
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
                    if (newMessage.trim() === "" || isNaN(+newMessage)) {
                      console.error("New message has to be a valid user ID");
                      return;
                    }
                    const response = await fetch(`/api/chat/get-or-create`, {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                      },
                      credentials: "include",
                      body: JSON.stringify({
                        other_user_id: newMessage,
                      }),
                    });
                    if (!response.ok) {
                      throw new Error("Failed to create chat");
                    } else {
                      console.log("Chat created successfully");
                      setNewMessage("");
                    }
                    const chatPreview: ChatPreviewBackendDTO = await response.json();
                    setChatData((prevChatData) => {
                      const newChat = ChatThread.fromPreviewDTO(chatPreview);
                      return {
                        ...prevChatData,
                        [chatPreview.id]: newChat,
                      };
                    });
                  }}
                  className="p-2 bg-customDarkBlue text-white rounded-3xl hidden md:block"
                >
                  Create Chat
                </button>
              </div>
            </div>
            <div onClick={handleOverlayClick} className="flex flex-col justify-end flex-1 border rounded-3xl p-4 bg-gray-50">
              <div ref={scrollRef} className="flex flex-col gap-2 mb-4 overflow-y-auto max-h-[60vh]">
                {chatMessages.map((message, index) => (
                  <div
                    key={index}
                    className={message.sentByUser ? "self-end" : "self-start"}
                  >
                    <div
                      className={`p-2 rounded-xl ${message.sentByUser
                        ? "bg-customDarkBlue text-white"
                        : "bg-gray-300"
                        }`}
                    >
                      {message.type === "tutorRequest" ? (
                        (() => {
                          try {
                            const tutorRequest: TutorRequest = JSON.parse(message.content as string);
                            return (
                              <div className="max-w-sm mx-auto p-6 bg-white border border-gray-200 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300">
                                <h2 className="text-xl font-semibold text-gray-800 mb-2">📚 Tutor Request</h2>
                                <p className="text-gray-700 mb-1"><span className="font-medium">Rate:</span>  ${tutorRequest.hourlyRate}/hr</p>
                                <p className="text-gray-700 mb-4"><span className="font-medium">Lesson Duration:</span> {tutorRequest.lessonDuration} min</p>
                                {!message.sentByUser && (
                                <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300 hover:bg-customYellow">
                                  Accept
                                </button>
                                )}
                              </div>
                            );
                          } catch (e) {
                            console.error("Failed to parse tutor request content:", e);
                            return <p>{message.content}</p>; // Fallback to plain text if parsing fails
                          }
                        })()
                      ) : (
                        <p>{message.content}</p>
                      )}
                    </div>
                    <p className="text-xs text-gray-400 mt-1 flex justify-end">
                      {message.time}
                    </p>
                  </div>
                ))}
                <div ref={messagesEndRef} />
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
                  ref={inputRef}
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
