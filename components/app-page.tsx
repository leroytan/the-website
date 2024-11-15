'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, X, User, ChevronLeft, ChevronRight } from 'lucide-react'
import { Inter } from 'next/font/google'
import { motion, AnimatePresence } from 'framer-motion'
import ReviewCarousel from './reviewCarousel'
import Subpage from './subpage'

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
            className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
          >
            <Link href="/login" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Log In
            </Link>
            <Link href="/signup" className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white">
              Sign Up
            </Link>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
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
          <Image src="" alt="THE Logo" width={100} height={50} className="w-20 sm:w-24 md:w-28 lg:w-32" />
          <LoginIcon />
        </div>
      </header>

      <main className="pt-16">
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
          style={{backgroundImage: "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Background-a09Or0u1zoDzwvwghU8CFesgQh4yOS.png')"}}
        >
          <div className="container mx-auto px-4 text-center">
            <motion.h2
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-3xl sm:text-4xl font-extrabold mb-4 sm:mb-6 text-orange-600"
            >
              Welcome to T.H.E.
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="mb-6 sm:mb-8 text-base sm:text-lg leading-relaxed text-white font-medium text-orange-600"
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
          className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
          style={{backgroundImage: "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Background%20Programmes-UN9YJk8RghvKNa65AnUQKDWDOmxMJC.png')"}}
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-white text-center">Our Features</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Personalized Learning", "Expert Tutors", "Flexible Scheduling", "Interactive Sessions"].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-white bg-opacity-90 rounded-lg shadow-md p-6"
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
          className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
          style={{backgroundImage: "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Why%20Join%20Us-AF4xs9i4oRDtWzeHkkRzt6udY0tm2Q.png')"}}
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-white text-center">Why Join Us</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Flexible Hours", "Competitive Pay", "Professional Development"].map((reason, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-white bg-opacity-90 rounded-lg shadow-md p-6"
                
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
          className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
          style={{backgroundImage: "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Background%20Description-ujr6myuKnkLaN7LPC4udhicvSYuKVD.png')"}}
        >
          <div className="container mx-auto px-4">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-white text-center">Our Programmes</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
              {["Math Tutoring", "Science Courses", "Language Classes", "Test Preparation", "Coding Bootcamps", "Art Workshops"].map((programme, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="bg-white bg-opacity-90 rounded-lg shadow-md p-6"
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
          className="bg-[#fabb84]"
        >
          <div className="container mx-auto px-4 py-8 sm:py-12 md:py-16">
            <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-white text-center">Student Reviews</h2>
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