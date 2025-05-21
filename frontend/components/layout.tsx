"use client";

import { useState, useEffect, useRef } from "react";
import localFont from "next/font/local";
import "./layout.css"; // Separate CSS file for component-specific styles
import Sidebar from "./sideBar";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  User,
  HomeIcon,
  BriefcaseBusiness,
  MessageCircle,
  UserRoundSearch,
  Bell,
  Plus,
  LayoutDashboard,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "../context/authContext";
import { Button } from "./button";
import { usePathname, useRouter } from "next/navigation";

const BurgerMenu = ({ togglesideBar }: { togglesideBar: () => void }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      onClick={togglesideBar}
      className="text-[#4a58b5]"
    >
      <Menu size={24} />
    </motion.button>
  );
};

const UserMenu = () => {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname()

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);
  const path = [
    {path: "/dashboard", name: "Dashboard", icon: <LayoutDashboard size={24} />},
    {path: "/assignments", name: "Assignments", icon: <BriefcaseBusiness size={24} />},
    {path: "/tutors", name: "Tutors", icon: <UserRoundSearch size={24} />},
    {path: "/chat/tutee", name: "Messages", icon: <MessageCircle size={24} />},
    {path: "/notifications", name: "Notifications", icon: <Bell size={24} />},
  ]
  return (
    <>
      <div className="flex flex-row items-center justify-end gap-6 h-full">
      {path.slice(0,3).map((item) => (
        <Button
          key={item.path}
          onClick={() => router.push(item.path)}
          className={`flex-col items-center text-sm hidden md:flex h-full box-border justify-center ${
            pathname === item.path ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]" : "text-gray-500"
          }`}
        >
          {item.icon}
          <span>{item.name}</span>
        </Button>
      ))}
      <div className="h-auto w-0.5 self-stretch bg-neutral-100" />
      {path.slice(3,5).map((item) => (
        <Button
          key={item.path}
          onClick={() => router.push(item.path)}
          className={`flex-col items-center text-sm hidden md:flex h-full box-border justify-center ${
            pathname === item.path ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]" : "text-gray-500"
          }`}
        >
          {item.icon}
          <span>{item.name}</span>
        </Button>
      ))}
        <div className="relative" ref={dropdownRef}>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(!isOpen)}
            className="text-[#4a58b5]"
          >
            <User size={24} />
          </motion.button>
          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
                className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
              >
                <Link
                  href="/profile/tutee"
                  className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
                  Profile
                </Link>

                <Link
                  href="/logout"
                  className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
                  Log Out
                </Link>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        <Button
          onClick={() => {router.push("/assignments?add=true")}}
          className="flex flex-row items-center bg-customOrange rounded-sm p-2 text-white text-sm"
        >
          <Plus />
          Assignment
        </Button>
      </div>
    </>
  );
};

export const geistSans = localFont({
  src: "../app/fonts/GeistVF.woff", // Adjust the path if necessary
  variable: "--font-geist-sans",
  weight: "100 900",
});
export const geistMono = localFont({
  src: "../app/fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function ComponentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSideBar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
      <header
        id="appbar"
        className="bg-white shadow-md sticky top-0 left-0 right-0 z-10 h-14"
      >
        <div className="flex flex-row items-center justify-between px-4 h-full">
          <div className="md:hidden">
            <BurgerMenu togglesideBar={toggleSideBar} />
          </div>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            
          >
            <Link href="/" passHref className="flex flex-row justify-between items-center">
              <Image
                src="/images/logo.png"
                alt="THE Logo"
                width={3508}
                height={2480}
                className="h-14 w-auto"
              />
              <div className="hidden md:block pl-4 flex-row whitespace-nowrap">
                <span className="text-customDarkBlue font-semibold text-xl">
                  Teach. &nbsp;
                </span>
                <span className="text-customOrange font-semibold text-xl">
                  Honour. &nbsp;
                </span>
                <span className="text-customDarkBlue font-semibold text-xl">
                  Excel.
                </span>
              </div>
            </Link>
          </motion.button>
          {isAuthenticated && <UserMenu />}
          {!isAuthenticated && (
            <Link href="/login">
              <motion.button
                whileHover={{ scale: 1.1 }} // Popup motion effect
                whileTap={{ scale: 0.95 }} // Slight shrink on tap
                className="lock px-4 py-2 text-md text-[#4a58b5] rounded-md transition-transform duration-200"
              >
                Log In
              </motion.button>
            </Link>
          )}
        </div>
      </header>

      {/* Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={toggleSideBar} />

      {/* Main Content */}
      <main
        className={`pt-0 transition-transform ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
      >
        {children}
      </main>
    </div>
  );
}
