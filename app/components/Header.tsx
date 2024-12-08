'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, User } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

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
            <Link href="/profile/tutee" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Profile
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

export const Header = ({ toggleSubpage }: { toggleSubpage: () => void }) => {
  return (
    <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
      <div className="container mx-auto px-4 py-2 sm:py-4 flex items-center justify-between">
        <BurgerMenu toggleSubpage={toggleSubpage} />
        <Image src="/images/logo.png" alt="THE Logo" width={100} height={50} className="w-16 sm:w-20 md:w-24 lg:w-28" />
        <UserMenu />
      </div>
    </header>
  )
}