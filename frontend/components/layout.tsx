"use client";

import { useState, useEffect, useRef } from "react";
import localFont from "next/font/local";
import "./layout.css"; // Separate CSS file for component-specific styles
import Sidebar from "./sideBar";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  User,
  BriefcaseBusiness,
  MessageCircle,
  UserRoundSearch,
  Bell,
  LayoutDashboard,
  ChevronDown,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "../context/authContext";
import { Button } from "./button";
import { usePathname, useRouter } from "next/navigation";
import AddAssignmentButton from "../app/(appbar)/assignments/_components/addAssignmentButton";

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
  const pathname = usePathname();
  const { user, tutor, loading } = useAuth();

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
    {
      path: "/dashboard",
      name: "Dashboard",
      icon: <LayoutDashboard size={24} />,
    },
    {
      path: "/assignments",
      name: "Assignments",
      icon: <BriefcaseBusiness size={24} />,
    },
    { path: "/tutors", name: "Tutors", icon: <UserRoundSearch size={24} /> },
    {
      path: "/chat/tutee",
      name: "Messages",
      icon: <MessageCircle size={24} />,
    },
    { path: "/notifications", name: "Notifications", icon: <Bell size={24} /> },
  ];
  return (
    <>
      <div className="flex flex-row items-center justify-end gap-6 h-full z-20">
        {path.slice(0, 3).map((item) => (
          <Button
            key={item.path}
            onClick={() => router.push(item.path)}
            className={`flex-col items-center text-sm hidden md:flex h-full box-border justify-center ${
              pathname === item.path
                ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]"
                : "text-gray-500"
            }`}
          >
            {item.icon}
            <span>{item.name}</span>
          </Button>
        ))}
        <div className="h-auto w-0.5 self-stretch bg-neutral-100" />
        {path.slice(3, 5).map((item) => (
          <Button
            key={item.path}
            onClick={() => router.push(item.path)}
            className={`flex-col items-center text-sm hidden md:flex h-full box-border justify-center ${
              pathname === item.path
                ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]"
                : "text-gray-500"
            }`}
          >
            {item.icon}
            <span>{item.name}</span>
          </Button>
        ))}
        <div className="relative" ref={dropdownRef}>
          {!tutor && (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setIsOpen(!isOpen)}
              className="text-customDarkBlue relative flex-col items-center text-sm hidden md:flex h-full box-border justify-center px-4"
              style={{ minWidth: 100 }}
            >
              <div className="flex flex-col items-center">
                <User size={24} />
                <span>{user?.name}</span>
              </div>
              <ChevronDown
                size={18}
                className="absolute right-2 top-1/2 -translate-y-1/2"
              />
            </motion.button>
          )}
          {tutor && (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setIsOpen(!isOpen)}
              className="text-customDarkBlue flex-col items-center text-sm hidden md:flex h-full box-border justify-center"
              style={{ minWidth: 80 }} // optional: ensures enough width for chevron
            >
              <div className="flex flex-col items-center">
                <Image
                  src={
                    user?.profile_photo_url ||
                    "/images/THE-girlprofilephoto.png"
                  }
                  alt="Profile"
                  width={30}
                  height={30}
                  className="rounded-full"
                />
                <span>{user?.name}</span>
              </div>
              <ChevronDown
                size={18}
                className="absolute right-0 top-1/2 -translate-y-1/2"
              />
            </motion.button>
          )}
          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
                className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50"
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
        {!tutor && <AddAssignmentButton />}
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
type UserWithRole =
  | {
      id: number;
      name: string;
      email: string;
      role: "tutor";
      tutorProfile: object; // refine this based on your schema
    }
  | {
      id: number;
      name: string;
      email: string;
      role: "client";
      tutorProfile: null;
    }
  | null;
export default function ComponentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSideBar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
      <header
        id="appbar"
        className="bg-white shadow-sm sticky top-0 left-0 right-0 z-20 h-14"
      >
        {loading ? (
          <LoadingSkeleton />
        ) : (
          <div className="flex flex-row items-center justify-between px-4 h-full">
            <div className="md:hidden">
              <BurgerMenu togglesideBar={toggleSideBar} />
            </div>

            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                href="/"
                passHref
                className="flex flex-row justify-between items-center"
              >
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
            {user && <UserMenu />}
            {!user && (
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
        )}
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
function LoadingSkeleton() {
  return <div className="flex flex-row items-center justify-between px-4 h-full">
            <div className="md:hidden">
              <BurgerMenu togglesideBar={()=>{}} />
            </div>

            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                href="/"
                passHref
                className="flex flex-row justify-between items-center"
              >
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
            
          </div>
}
