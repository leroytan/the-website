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
  Plus,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "../context/authContext";
import { Button } from "./button";
import { usePathname, useRouter } from "next/navigation";
import AddAssignmentButton from "../app/(appbar)/assignments/_components/addAssignmentButton";
import { useError } from "@/context/errorContext";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";

const BurgerMenu = ({ togglesideBar }: { togglesideBar: () => void }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      onClick={togglesideBar}
      className="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
    >
      <Menu size={24} className="text-[#4a58b5]" />
    </motion.button>
  );
};

const UserMenu = () => {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const { user, tutor, loading } = useAuth();
  const { error, setError } = useError();

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
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
      >
        <div className="w-8 h-8 md:w-10 md:h-10 rounded-full overflow-hidden">
          <Image
            src={user?.profile_photo_url || "/images/THE-guyprofilephoto.png"}
            alt="Profile"
            width={40}
            height={40}
            className="object-cover w-full h-full"
          />
        </div>
        <span className="hidden md:block text-sm font-medium text-gray-700">
          {user?.name}
        </span>
        <ChevronDown
          size={20}
          className={`text-gray-500 transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg py-2 z-50">
          <div className="px-4 py-2 border-b border-gray-100">
            <p className="text-sm font-medium text-gray-900">{user?.name}</p>
            <p className="text-xs text-gray-500">{user?.email}</p>
          </div>
          <div className="py-1">
            <button
              onClick={() => {
                router.push("/profile");
                setIsOpen(false);
              }}
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Profile
            </button>
            {user && !tutor && (
              <button
                onClick={async () => {
                  try {
                    const response = await fetchWithTokenCheck(`/api/me`, {
                      method: "PUT",
                      headers: {
                        "Content-Type": "application/json",
                      },
                      body: JSON.stringify({ intends_to_be_tutor: true }),
                    });

                    if (response.ok) {
                      document.cookie = `intends_to_be_tutor=${true}; path=/; SameSite=Lax; Secure`;
                      document.cookie = `tutor_profile_complete=${false}; path=/; SameSite=Lax; Secure`;
                      router.push("/onboarding/tutor");
                    } else {
                      setError("An error occurred while updating your status.");
                      // Optionally, display an error message to the user
                    }
                  } catch (error) {
                    setError("An error occurred while updating your status.");
                    // Optionally, display an error message to the user
                  }
                }}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Become a Tutor
              </button>
            )}
            <button
              onClick={() => {
                router.push("/logout");
                setIsOpen(false);
              }}
              className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </div>
      )}
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
  const { user, loading, tutor } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  const toggleSideBar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

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
      path: "/chat",
      name: "Messages",
      icon: <MessageCircle size={24} />,
    },
    { path: "/notifications", name: "Notifications", icon: <Bell size={24} /> },
  ];

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
            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <BurgerMenu togglesideBar={toggleSideBar} />
            </div>

            {/* Logo and Brand */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="flex-shrink-0"
            >
              <Link href="/" passHref className="flex flex-row items-center">
                <Image
                  src="/images/logo.png"
                  alt="THE Logo"
                  width={3508}
                  height={2480}
                  className="h-10 md:h-14 w-auto"
                />
                <div className="hidden md:block pl-4">
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

            {/* Desktop Navigation */}
            {user && (
              <div className="hidden md:flex items-center h-full ml-auto">
                <nav className="flex items-center h-full">
                  {path.slice(0, 3).map((item) => (
                    <Button
                      key={item.path}
                      onClick={() => router.push(item.path)}
                      className={`flex flex-col items-center justify-center h-full px-4 gap-0.5 ${
                        pathname === item.path
                          ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]"
                          : "text-gray-500 hover:text-[#4a58b5]"
                      }`}
                    >
                      <div className="flex items-center justify-center">
                        {item.icon}
                      </div>
                      <span className="text-sm">{item.name}</span>
                    </Button>
                  ))}
                  <div className="h-auto w-0.5 self-stretch bg-neutral-100 mx-2" />
                  {path.slice(3, 5).map((item) => (
                    <Button
                      key={item.path}
                      onClick={() => router.push(item.path)}
                      className={`flex flex-col items-center justify-center h-full px-4 gap-0.5 ${
                        pathname === item.path
                          ? "border-b-2 border-b-[#4a58b5] text-[#4a58b5]"
                          : "text-gray-500 hover:text-[#4a58b5]"
                      }`}
                    >
                      <div className="flex items-center justify-center">
                        {item.icon}
                      </div>
                      <span className="text-sm">{item.name}</span>
                    </Button>
                  ))}
                </nav>
              </div>
            )}

            {/* Mobile Navigation Icons */}
            {user && (
              <div className="flex md:hidden items-center gap-4 ml-auto">
                {!tutor && (
                  <Button
                    onClick={() => {
                      const params = new URLSearchParams(
                        window.location.search
                      );
                      params.set("add", "true");
                      router.push(`/assignments?${params.toString()}`);
                    }}
                    className="p-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200"
                  >
                    <Plus size={24} />
                  </Button>
                )}
                <Button
                  onClick={() => router.push("/chat")}
                  className={`p-2 ${
                    pathname === "/chat" ? "text-[#4a58b5]" : "text-gray-500"
                  }`}
                >
                  <MessageCircle size={24} />
                </Button>
                <Button
                  onClick={() => router.push("/notifications")}
                  className={`p-2 ${
                    pathname === "/notifications"
                      ? "text-[#4a58b5]"
                      : "text-gray-500"
                  }`}
                >
                  <Bell size={24} />
                </Button>
              </div>
            )}

            {/* Right-aligned items */}
            <div className="flex items-center gap-3 ml-4">
              {user && !tutor && (
                <div className="hidden md:flex items-center">
                  <AddAssignmentButton />
                </div>
              )}
              {/* User Menu */}
              {user && <UserMenu />}
              {!user && (
                <Link href="/login">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-4 py-2 text-md text-[#4a58b5] rounded-md transition-transform duration-200"
                  >
                    Log In
                  </motion.button>
                </Link>
              )}
            </div>
          </div>
        )}
      </header>

      {/* Mobile Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={toggleSideBar} />

      {/* Main Content */}
      <main className="min-h-[calc(100vh-3.5rem)]">{children}</main>
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="flex flex-row items-center justify-between px-4 h-full">
      <div className="md:hidden">
        <BurgerMenu togglesideBar={() => {}} />
      </div>

      <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
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
  );
}
