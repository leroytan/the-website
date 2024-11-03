'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { User, LogOut } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export const UserMenu = () => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const router = useRouter()

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

  const handleToggle = () => {
    setIsOpen(!isOpen)
  }

  const handleProfileClick = () => {
    setIsOpen(false)
    router.push('/profile/tutee')
  }

  const handleLogoutClick = () => {
    setIsOpen(false)
    // Implement logout logic here
    console.log('Logging out...')
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={handleToggle}
        className="text-[#4a58b5] focus:outline-none"
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
            <button 
              onClick={handleProfileClick}
              className="flex items-center w-full px-4 py-2 text-sm text-left text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
            >
              <User size={16} className="mr-2" />
              Profile
            </button>
            <button 
              onClick={handleLogoutClick}
              className="flex items-center w-full px-4 py-2 text-sm text-left text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
            >
              <LogOut size={16} className="mr-2" />
              Log Out
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}