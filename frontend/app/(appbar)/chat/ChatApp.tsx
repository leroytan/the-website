"use client";
import { createCheckoutSession } from "@/app/pricing/createCheckoutSession";
import AssignmentCard from "@/components/assignmentCard";
import { BASE_URL } from "@/utils/constants";
import { timeAgo, to12HourTime } from "@/utils/date";
import { ArrowLeftToLine, BookPlusIcon } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import React, { ReactElement, useEffect, useRef, useState } from "react";
import { useError } from "@/context/errorContext";

const ChatApp = () => {

  class ChatThread {
    private id: number;
    private isLocked: boolean; // true if the chat is locked, false if unlocked
    private title: string;
    private messages: Message[];
    private initialPreview: ChatPreview;
    private indexOfLastTutorRequest: number = -1; // Index of the last tutor request message, -1 if none
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
        -1, 
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
      return new ChatThread(dto.chat_id, isLocked, sender, -1, messages);
    }

    constructor(id: number, isLocked: boolean, title: string = "Select a chat", indexOfLastTutorRequest: number = -1, messages: Message[] = [], initialPreview: ChatPreview | null = null) {
      this.id = id;
      this.isLocked = isLocked;
      this.title = title;
      this.indexOfLastTutorRequest = indexOfLastTutorRequest;
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
      if (message.message_type === "tutor_request") {
        const index = this.indexOfLastTutorRequest;
        if (index !== -1) {
          const content = JSON.parse(this.messages[index].content as string);
          content.status = "EXPIRED"; // Update the status of the tutor request to PENDING
          this.messages[index].content = JSON.stringify(content); // Convert back to string
        }
        this.indexOfLastTutorRequest = this.messages.length; // Update the index of the last tutor request
      }
      this.messages.push(...this.convertSortMessages([message]));
    }

    addHistoricalMessages(messages: MessageBackendDTO[]): void {
      const newMessages = this.convertSortMessages(messages);
      this.messages.unshift(...newMessages);
      // find the index of the last tutor request in the new messages
      const lastTutorRequestIndex = this.messages.findLastIndex((msg) => msg.type === "tutorRequest");
      this.indexOfLastTutorRequest = lastTutorRequestIndex;
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
        this.indexOfLastTutorRequest,
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
    assignmentRequestId: number;
    assignmentId: number;
    tutorId: number;
    assignmentTitle?: string;
    status?: "PENDING" | "ACCEPTED" | "EXPIRED"; // Default to PENDING
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

  const searchParams = useSearchParams();
  const router = useRouter();
  const [selectedChat, setSelectedChat] = useState(1);
  const [newMessage, setNewMessage] = useState("");
  const [showChat, setShowChat] = useState(false);
  const [showDropup, setShowDropup] = useState(false);

  const initialChatData: ChatData = {};
  const [chatData, setChatData] = useState<ChatData>(initialChatData);
  const { setError } = useError();

  const chatMessages = chatData[selectedChat]?.getDisplayMessages() || [];
  const chatPreviews: ChatPreview[] = Object.values(chatData).map((chat) => chat.getPreview()).sort((a, b) => a.lastUpdate.getTime() - b.lastUpdate.getTime()).reverse();
  const lockedChats = chatPreviews.filter((chat) => chat.isLocked);
  const unlockedChats = chatPreviews.filter((chat) => !chat.isLocked);
  const chatName = chatData[selectedChat]?.getTitle() || "Select a chat";

  const socketRef = useRef<WebSocket | null>(null);

  const chatJustFetchedRef = useRef(false);
  
  useEffect(() => {
    if (chatJustFetchedRef.current) {
      chatJustFetchedRef.current = false;
      const chatIdFromParams = searchParams.get("chatId");
      if (chatIdFromParams) {
        const chatId = parseInt(chatIdFromParams, 10);
        if (chatData[chatId]) {
          handleChatSelection(chatId);
        } else {
          setError("Chat not found or inaccessible. Please select an existing chat.");
          const currentPath = window.location.href.split("?")[0].slice(window.location.origin.length); // Get the current URL without query params
          router.push(currentPath); // Redirect to base chat URL to clear invalid chatId
        }
      }
    }
  }, [chatData]);

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
      chatJustFetchedRef.current = true;
    } catch (error) {
      setError("Oops! Something went wrong while fetching chats.");
    }
  };

  const fetchHistoricalMessages = async (chatId: number) => {
    const container = scrollRef.current;
    if (!container) {
      setError("Chat display area not found. Please refresh the page.");
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
        const errorData = await response.json();
        setError(errorData.detail || "Failed to fetch chat messages. Please try again.");
        return;
      }

      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        setError("Received invalid response from server. Please try again.");
        return;
      }

      if (!data.messages || typeof data.has_more === "undefined") {
        setError("Unexpected data format from server. Please try again.");
        return;
      }

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
      setError("An unexpected error occurred while fetching chat messages. Please try again.");
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

  // This only runs when the component mounts
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
    const currentUrl = window.location.href.split("?")[0]; // Get the current URL without query params
    router.push(`${currentUrl}?chatId=${chatId}`); // Update URL with chatId
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

  const handleAcceptAssignment = async (assignmentRequestId: number, hourlyRate: number, tutorId: number) => {
    try {
      const session: { id: string; url: string } = await createCheckoutSession({
        mode: "payment",
        success_url: window.location.origin + "/payment-success",
        cancel_url: window.location.origin + "/payment-cancel",
        assignment_request_id: assignmentRequestId,
        tutor_id: tutorId,
        chat_id: selectedChatRef.current
      });

      router.push(session.url);
    } catch (err) {
      console.error("Stripe error:", err);
      alert(err);
    }
  };

  const inputRef = useRef<HTMLInputElement>(null);

  const handleOverlayClick = () => {
    if (inputRef.current) {
      inputRef.current.focus(); // Focus the input when the parent is clicked
    }
  };
  return (
    <div className="flex flex-row bg-customLightYellow h-[calc(100vh-56px)]">
        {/* Sidebar - Shown on mobile */}
        <aside
          className={`w-full md:w-1/4 p-4 border-r border-gray-200 bg-white shadow-sm ${showChat ? "hidden md:block" : "block"
            }`}
        >
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
                {/* <button
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
                </button> */}
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
                            if (tutorRequest.assignmentRequestId === undefined || tutorRequest.tutorId === undefined) {
                              console.error("Invalid tutor request message:", message.content);
                              return <p>Error: Invalid tutor request message.</p>;
                            }
                            return (
                              <div className="max-w-sm mx-auto p-6 bg-white border border-gray-200 rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300">
                                <h2 className="text-xl font-semibold text-gray-800 mb-2">{tutorRequest.assignmentTitle && (
                                  <p className="text-gray-700 mb-2">
                                    <span className="font-medium">📚 </span>{" "}
                                    <Link
                                      href={`/assignments?selected=${tutorRequest.assignmentId}`}
                                      className="text-customDarkBlue hover:underline"
                                    >
                                      {tutorRequest.assignmentTitle}
                                    </Link>
                                  </p>
                                )}</h2>
                                
                                <p className="text-gray-700 mb-1"><span className="font-medium">Rate:</span>  ${tutorRequest.hourlyRate}/hr</p>
                                <p className="text-gray-700 mb-4"><span className="font-medium">Lesson Duration:</span> {tutorRequest.lessonDuration} min</p>
                                {tutorRequest.status === "ACCEPTED" && (
                                  <div className="w-full bg-green-500 text-white font-semibold py-2 px-4 rounded-lg text-center">
                                    Accepted
                                  </div>
                                )}
                                {message.sentByUser && tutorRequest.status === "PENDING" && (
                                  <div className="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg text-center">
                                    Pending
                                  </div>
                                )}
                                {!message.sentByUser && (tutorRequest.status === "PENDING") && (
                                <button
                                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300 hover:bg-customYellow"
                                  onClick={() => handleAcceptAssignment(tutorRequest.assignmentRequestId, tutorRequest.hourlyRate, tutorRequest.tutorId)}
                                >
                                  Accept
                                </button>
                                )}
                                {tutorRequest.status === "EXPIRED" && (
                                  <div className="w-full bg-gray-500 text-white font-semibold py-2 px-4 rounded-lg text-center">
                                    Expired
                                  </div>
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
  );
};

export default ChatApp;
