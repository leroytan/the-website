'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, X, User, ChevronLeft, ChevronRight, LogOut } from 'lucide-react'
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

const LoginIcon = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false) // New state to track login status
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // In a real app, you'd check the user's login status here
    // For now, we'll just simulate a logged-in user
    setIsLoggedIn(true)

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

  const handleLogout = () => {
    // In a real app, you'd handle the logout process here
    setIsLoggedIn(false)
    setIsOpen(false)
  }

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
            className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
          >
            {isLoggedIn ? (
              <>
                <Link href="/profile" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
                  <LogOut size={18} className="inline mr-2" />
                  Log Out
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
                  Log In
                </Link>
                <Link href="/signup" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
                  Sign Up
                </Link>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
const ReviewCarousel = () => {
  const [currentReview, setCurrentReview] = useState(0)
  const reviews = [
    { id: 1, text: "Great experience with THE! The tutors are knowledgeable and patient.", author: "John Doe" },
    { id: 2, text: "Excellent tutors and programmes! My grades have improved significantly.", author: "Jane Smith" },
    { id: 3, text: "Highly recommend their services! The flexible scheduling is perfect for busy students.", author: "Mike Johnson" },
  ]

  const nextReview = () => {
    setCurrentReview((prev) => (prev + 1) % reviews.length)
  }

  const prevReview = () => {
    setCurrentReview((prev) => (prev - 1 + reviews.length) % reviews.length)
  }

  return (
    <div className="relative flex items-center justify-center">
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={prevReview}
        className="mr-4 bg-[#4a58b5] text-white p-2 rounded-full z-10"
      >
        <ChevronLeft size={24} />
      </motion.button>
      <div className="relative overflow-hidden w-[80%] h-[200px]">
        <AnimatePresence initial={false} custom={currentReview}>
          <motion.div
            key={currentReview}
            custom={currentReview}
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -300 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="bg-white p-6 rounded-lg shadow-lg absolute w-full"
          >
            <p className="text-[#4a58b5] mb-4 text-base sm:text-lg">{reviews[currentReview].text}</p>
            <p className="font-bold text-[#fc6453] text-sm sm:text-base">- {reviews[currentReview].author}</p>
          </motion.div>
        </AnimatePresence>
      </div>
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={nextReview}
        className="ml-4 bg-[#4a58b5] text-white p-2 rounded-full z-10"
      >
        <ChevronRight size={24} />
      </motion.button>
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
              <li><a href="/" className="text-lg font-semibold hover:underline">Home</a></li>
              <li><a href="#" className="text-lg font-semibold hover:underline">THE Team</a></li>
              <li><a href="#" className="text-lg font-semibold hover:underline">Courses</a></li>
              <li><a href="/tutors" className="text-lg font-semibold hover:underline">THE Tutors</a></li>
            </ul>
          </nav>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export function AppPage() {
  const [isSubpageOpen, setIsSubpageOpen] = useState(false)

  const toggleSubpage = () => {
    setIsSubpageOpen(!isSubpageOpen)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <Subpage isOpen={isSubpageOpen} onClose={() => setIsSubpageOpen(false)} />

      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <BurgerMenu toggleSubpage={toggleSubpage} />
          <Image src="/images/logo.png"
            alt="THE Logo"
            width={100}
            height={75} className="w-20 sm:w-24 md:w-28 lg:w-32" />
          <LoginIcon />
        </div>
      </header>

      <main className="pt-16">
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
          style={{backgroundImage: "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Background%20Programmes%20(1)-uqKeIKQelD3tB85FeakeXgL048p4db.png')"}}
        >
          <div className="container mx-auto px-4 text-center">
            <motion.h2
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-3xl sm:text-4xl font-extrabold mb-4 sm:mb-6 text-[#4a58b5]"
            >
              Welcome to THE
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="mb-6 sm:mb-8 text-base sm:text-lg leading-relaxed text-[#4a58b5] font-medium"
            >
              <span className="font-bold">Teach . Honour . Excel</span> - Your path to educational excellence!
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-[#fabb84] text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-bold hover:bg-[#fc6453] transition-colors duration-200"
              >
                Request a tutor
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-[#fabb84] text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-bold hover:bg-[#fc6453] transition-colors duration-200"
              >
                Join Us
              </motion.button>
            </motion.div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-[#fff2de]" // Update 1
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">Our Features</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Personalized Learning", "Expert Tutors", "Flexible Scheduling", "Interactive Sessions"].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  whileHover={{ scale: 1.03 }} // Update 3
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300" // Update 2
                >
                  <h3 className="text-lg sm:text-xl font-bold mb-3 text-[#4a58b5]">{feature}</h3>
                  <p className="text-[#4a58b5] text-sm sm:text-base">We offer tailored educational experiences to help you excel in your studies.</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">Why Join Us</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Flexible Hours", "Competitive Pay", "Professional Development"].map((reason, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
                >
                  <h3 className="text-lg sm:text-xl font-bold mb-3 text-[#4a58b5]">{reason}</h3>
                  <p className="text-[#4a58b5] text-sm sm:text-base">Join our team of dedicated educators and make a difference in students' lives.</p>
                </motion.div>
              ))}
            </div>
          </div>
        
        </motion.section>

        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">Meet the Team</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
              {["John Doe", "Jane Smith", "Mike Johnson", "Emily Brown"].map((member, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-[#fabb84] rounded-lg shadow-md p-6 text-center"
                >
                  <div className="w-16 h-16 sm:w-24 sm:h-24 bg-[#fc6453] rounded-full mx-auto mb-4"></div>
                  <h3 className="text-lg sm:text-xl font-bold mb-2 text-white">{member}</h3>
                  <p className="text-white text-sm sm:text-base font-medium">Expert Tutor</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">Our Programmes</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Math Tutoring", "Science Courses", "Language Classes", "Test Preparation", "Coding Bootcamps", "Art Workshops"].map((programme, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
                >
                  <h3 className="text-lg sm:text-xl font-bold mb-3 text-[#4a58b5]">{programme}</h3>
                  <p className="text-[#4a58b5] text-sm sm:text-base">Comprehensive courses designed to help you succeed in your academic journey.</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">Student Reviews</h2>
            <ReviewCarousel />
          </div>
        </motion.section>
      </main>

      <footer className="bg-[#4a58b5] text-white py-6 sm:py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm sm:text-base font-medium">&copy; 2024 Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}