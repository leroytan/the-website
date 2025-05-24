"use client";
import { geistMono, geistSans } from "@/components/layout";
import UserMenu from "@/components/UserMenu";
import { motion } from "framer-motion";
import Link from "next/link";
import React, { ReactElement, useState } from "react";
import Image from "next/image";
import { ArrowLeftToLine } from "lucide-react";
import { useRouter } from "next/navigation";
import AssignmentCard from "@/components/assignmentCard";
type Chat = {
  name: string;
  message: string;
  time: string;
  notifications: number;
};
const ChatApp = () => {
  const chatData = {
    lockedChats: [
      {
        name: "User 1",
        message: "Assignment Card",
        time: "Today, 9:52pm",
        notifications: 1,
      },
    ],
    unlockedChats: [],
    chatHistory: {
      "User 1": [
        {
          sender: "User",
          message: (
            <AssignmentCard
              title={""}
              location={""}
              estimated_rate={""}
              weekly_frequency={0}
              available_slots={[]}
              special_requests={""}
              subjects={[]}
              level={""}
            ></AssignmentCard>
          ),
          time: "Today, 9:52pm",
          sentByUser: false,
        },
      ],
      Anil: [
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
    },
  };
  const router = useRouter();
  const [selectedChat, setSelectedChat] = useState("User 1");
  type ChatHistoryKeys = keyof typeof chatData.chatHistory;
  const [chatMessages, setChatMessages] = useState<
    {
      sender: string;
      message: string | ReactElement;
      time: string;
      sentByUser: boolean;
    }[]
  >(chatData.chatHistory[selectedChat as ChatHistoryKeys]);
  const [newMessage, setNewMessage] = useState("");
  const [showChat, setShowChat] = useState(false);

  const handleChatSelection = (chatName: React.SetStateAction<string>) => {
    setSelectedChat(chatName);
    setChatMessages(chatData.chatHistory[chatName as ChatHistoryKeys]);
    setShowChat(true);
    setNewMessage("");
  };
  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
      setChatMessages([
        ...chatMessages,
        { sender: "User", message: newMessage, time: "Now", sentByUser: true },
      ]);
      setNewMessage("");
    }
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
                {chatData.lockedChats.map((chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(chat.name)}
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
                {chatData.unlockedChats.map((chat: Chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
                    onClick={() => handleChatSelection(chat.name)}
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
                <p className="text-lg font-semibold">{selectedChat}</p>
                <p className="text-sm text-gray-500">Online</p>
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
                <input
                  type="text"
                  placeholder="Type your message here..."
                  className="flex-1 px-4 py-2 rounded-3xl border border-gray-300"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
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
