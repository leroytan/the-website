"use client";

import { useState, useEffect, useRef } from "react";
import localFont from "next/font/local";
import "./layout.css"; // Separate CSS file for component-specific styles
import Sidebar from "./sideBar";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, User, Book, Calendar, MessageSquare } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "./AuthContent";

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
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

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

  return (
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
        className="bg-white shadow-md sticky top-0 left-0 right-0 z-10"
      >
        <div className="container mx-auto px-4 py-2 sm:py-3 flex items-center justify-between">
          <BurgerMenu togglesideBar={toggleSideBar} />
          <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
            <Link href="/" passHref>
              <Image
                src="/images/logo.png"
                alt="THE Logo"
                width={100}
                height={50}
                className="w-16 sm:w-20 md:w-24 lg:w-28"
              />
            </Link>
          </motion.button>
          {isAuthenticated && <UserMenu />}
          {!isAuthenticated && (
            <Link
              href="/login"
            >
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
