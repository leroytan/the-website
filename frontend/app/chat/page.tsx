"use client";
import { geistMono, geistSans } from "@/components/layout";
import UserMenu from "@/components/UserMenu";
import { motion } from "framer-motion";
import Link from "next/link";
import React from "react";
import Image from "next/image";
import { ArrowLeftToLine } from "lucide-react";
import { useRouter } from 'next/navigation'

const ChatApp = () => {
  const router = useRouter();
  const lockedChats = [
    {
      name: "User 1",
      message: "Hello!",
      time: "Today, 9:52pm",
      notifications: 4,
    },
    {
      name: "User 2",
      message: "That is true...",
      time: "Yesterday, 12:31pm",
      notifications: 0,
    },
    {
      name: "User 3",
      message: "It’s not going to happen",
      time: "Wednesday, 9:12am",
      notifications: 0,
    },
  ];

  const unlockedChats = [
    {
      name: "Anil",
      message: "Yes Sure!",
      time: "Today, 9:52pm",
      notifications: 0,
    },
    {
      name: "Chuutiya",
      message: "See you tomorrow",
      time: "Today, 12:11pm",
      notifications: 1,
    },
    {
      name: "Mary ma’am",
      message: "Thanks!",
      time: "Today, 2:40pm",
      notifications: 1,
    },
    {
      name: "Bill Gates",
      message: "Nevermind bro",
      time: "Yesterday, 12:31pm",
      notifications: 5,
    },
    {
      name: "Victoria H",
      message: "Okay, brother. let’s see...",
      time: "Wednesday, 11:12am",
      notifications: 0,
    },
  ];

  return (
    <div className="flex flex-col min-w-[320px]">
      <div className="flex flex-1 overflow-hidden bg-customLightYellow">
        {/* Sidebar - Hidden on mobile */}
        <aside
          className="hidden md:block w-1/4 p-4 border-r border-gray-200 bg-white shadow-sm shadow-customlightBlue"
          style={{ height: "100vh" }}
        >
          <div
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
          >
            <header id="topbar" className="bg-white">
              <div className="container mx-auto px-4 py-2 sm:py-3 flex items-center justify-between">
                
                <motion.button
                  whileHover={{ scale: 1.1,  }}
                  whileTap={{ scale: 0.95 }}
                  className="text-customDarkBlue hover:text-customYellow"
                  onClick={() => router.back()}
                >
                  <ArrowLeftToLine />
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
          <div className="flex flex-col h-full">
            <div className="w-full flex"></div>
            <div className="mb-4 p-4 ">
              <input
                type="text"
                placeholder="Search"
                className="w-full px-4 py-2 rounded-3xl border border-gray-300 shadow-sm shadow-customlightBlue"
              />
            </div>
            <div className="flex-1 mb-6 overflow-y-auto">
              <div className="bg-white p-2 font-bold sticky top-0 z-10">
                Locked
              </div>
              <div className="space-y-2">
                {lockedChats.map((chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
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

            <div className="flex-1 overflow-y-auto ">
              <div className="bg-white px-2 py-4 font-bold sticky top-0 z-10">
                Unlocked
              </div>
              <div className="space-y-2">
                {unlockedChats.map((chat, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-2 border-b"
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
        <main className="flex-1 p-4 min-w-[320px]">
          <div className="p-4 bg-white rounded-3xl shadow-md h-full flex flex-col">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-gray-300 rounded-full"></div>
              <div className="ml-4">
                <p className="text-lg font-semibold">Anil</p>
                <p className="text-sm text-gray-500">
                  Online - Last seen, 2:02pm
                </p>
              </div>
            </div>
            <div className="flex flex-col justify-end flex-1 border rounded-3xl p-4 bg-gray-50">
              <div className="flex flex-col gap-2 mb-4 overflow-y-auto max-h-[60vh]">
                <div className="self-start">
                  <p className="p-2 bg-gray-300 rounded-3xl">Hey there!</p>
                  <p className="text-xs text-gray-400 mt-1">Today, 9:52pm</p>
                </div>
                <div className="self-start">
                  <p className="p-2 bg-gray-300 rounded-3xl">How are you?</p>
                  <p className="text-xs text-gray-400 mt-1">Today, 9:53pm</p>
                </div>
                <div className="self-end">
                  <p className="p-2 bg-customDarkBlue text-white rounded-3xl">
                    Hello!
                  </p>
                  <p className="text-xs text-gray-400 mt-1 flex justify-end">
                    Today, 9:54pm
                  </p>
                </div>
                <div className="self-end">
                  <p className="p-2 bg-customDarkBlue text-white rounded-3xl">
                    I am fine and how are you?
                  </p>
                  <p className="text-xs text-gray-400 mt-1 flex justify-end">
                    Today, 9:55pm
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 mt-auto">
                <input
                  type="text"
                  placeholder="Type your message here..."
                  className="flex-1 px-4 py-2 rounded-3xl border border-gray-300"
                />
                <button className="p-2 bg-customDarkBlue text-white rounded-3xl hidden md:block">
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
