'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, X, User, Book, Calendar, MessageSquare } from 'lucide-react'
import { Inter } from 'next/font/google'
import { motion, AnimatePresence } from 'framer-motion'

const inter = Inter({ subsets: ['latin'] })

const BurgerMenu = ({ toggleSubpage }: { toggleSubpage: () => void }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      onClick={toggleSubpage}
      className="text-[#4a58b5]"
    >
      <Menu size={24} />
    </motion.button>
  )
}

const UserMenu = () => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

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
            <Link href="/profile" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Profile
            </Link>
            <Link href="/settings" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Settings
            </Link>
            <Link href="/logout" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Log Out
            </Link>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

const Subpage = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose()
      }
    }
    window.addEventListener("keydown", handleEscape)
    return () => window.removeEventListener("keydown", handleEscape)
  }, [onClose])

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: "-100%" }}
          animate={{ x: 0 }}
          exit={{ x: "-100%" }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className="fixed top-0 left-0 w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-1/4 h-full bg-white shadow-lg z-50"
        >
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onClose}
            className="absolute top-4 right-4 text-[#4a58b5]"
          >
            <X size={24} />
          </motion.button>
          <nav className="p-6 text-[#4a58b5]">
            <ul className="space-y-4">
              <li><Link href="/dashboard/tutee" className="text-lg font-semibold hover:underline">Dashboard</Link></li>
              <li><Link href="/courses" className="text-lg font-semibold hover:underline">My Courses</Link></li>
              <li><Link href="/schedule" className="text-lg font-semibold hover:underline">Schedule</Link></li>
              <li><Link href="/messages" className="text-lg font-semibold hover:underline">Messages</Link></li>
              <li><Link href="/progress" className="text-lg font-semibold hover:underline">My Progress</Link></li>
            </ul>
          </nav>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default function TuteeDashboard() {
  const [isSubpageOpen, setIsSubpageOpen] = useState(false)

  const toggleSubpage = () => {
    setIsSubpageOpen(!isSubpageOpen)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <Subpage isOpen={isSubpageOpen} onClose={() => setIsSubpageOpen(false)} />
      
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-2 sm:py-4 flex items-center justify-between">
          <BurgerMenu toggleSubpage={toggleSubpage} />
          <Image src="" alt="THE Logo" width={100} height={50} className="w-16 sm:w-20 md:w-24 lg:w-28" />
          <UserMenu />
        </div>
      </header>

      <main className="pt-16 sm:pt-20 md:pt-24 pb-12">
        <div className="container mx-auto px-4">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl sm:text-3xl font-bold text-[#4a58b5] mb-6 sm:mb-8"
          >
            Welcome back, [Tutee Name]!
          </motion.h1>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-white rounded-lg shadow-md p-4 sm:p-6"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-[#4a58b5] mb-3 sm:mb-4">Upcoming Sessions</h2>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <Calendar className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">Math Tutoring - Today, 4:00 PM</span>
                </li>
                <li className="flex items-center">
                  <Calendar className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">Science Study - Tomorrow, 2:00 PM</span>
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-white rounded-lg shadow-md p-4 sm:p-6"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-[#4a58b5] mb-3 sm:mb-4">Current Courses</h2>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <Book className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">Advanced Mathematics</span>
                </li>
                <li className="flex items-center">
                  <Book className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">Physics 101</span>
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="bg-white rounded-lg shadow-md p-4 sm:p-6"
            >
              <h2 className="text-lg sm:text-xl font-semibold text-[#4a58b5] mb-3 sm:mb-4">Recent Messages</h2>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <MessageSquare className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">New message from Math Tutor</span>
                </li>
                <li className="flex items-center">
                  <MessageSquare className="mr-2 text-[#fabb84]" size={18} />
                  <span className="text-sm sm:text-base">Reminder: Homework due tomorrow</span>
                </li>
              </ul>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-8 sm:mt-12"
          >
            <h2 className="text-xl sm:text-2xl font-bold text-[#4a58b5] mb-4 sm:mb-6">Your Progress</h2>
            <div className="bg-white rounded-lg shadow-md p-4 sm:p-6">
              <div className="h-40 sm:h-60 bg-gray-100 rounded-md flex items-center justify-center">
                <p className="text-[#4a58b5] text-sm sm:text-base">Your progress visualization will be displayed here.</p>
              </div>
            </div>
          </motion.div>
        </div>
      </main>

      <footer className="bg-[#4a58b5] text-white py-4 sm:py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-xs sm:text-sm">&copy; 2024 Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}