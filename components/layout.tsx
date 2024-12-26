'use client';

import { useState } from "react";
import localFont from "next/font/local";
import "./layout.css"; // Separate CSS file for component-specific styles
import Sidebar from "./sideBar";

const geistSans = localFont({
  src: "../app/fonts/GeistVF.woff", // Adjust the path if necessary
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "../app/fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function ComponentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div
      className={`${geistSans.variable} ${geistMono.variable} antialiased`}
    >
      {/* Header */}
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          {/* Sidebar Toggle Button */}
          <button
            onClick={toggleSidebar}
            className="text-[#4a58b5] font-bold"
          >
            ☰ Menu
          </button>
          <div>Logo or Other Content</div>
        </div>
      </header>

      {/* Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={toggleSidebar} />

      {/* Main Content */}
      <main
        className={`pt-16 transition-transform ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
      >
        {children}
      </main>
    </div>
  );
}
