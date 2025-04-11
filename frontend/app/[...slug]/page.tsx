'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import { Home, Search } from 'lucide-react'
import { motion } from 'framer-motion'

const inter = Inter({ subsets: ['latin'] })

export default function NotFound() {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Implement search functionality here
    console.log('Search query:', searchQuery)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] flex flex-col ${inter.className}`}>
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="text-[#4a58b5] hover:text-[#fabb84] transition-colors">
            <Home size={24} />
          </Link>
          <Image
            src="/images/logo.png"
            alt="THE Logo"
            width={100}
            height={50}
            className="w-20 sm:w-24 md:w-28 lg:w-32"
          />
          <div className="w-6"></div>
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center pt-16 pb-12 px-4">
        <div className="max-w-2xl w-full">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h1 className="text-6xl font-bold text-[#4a58b5] mb-4">404</h1>
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-6">Page Not Found</h2>
            <p className="text-[#4a58b5] mb-8">
              Oops! The page you are looking for doesn't exist or has been moved.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <form onSubmit={handleSearch} className="mb-8">
              <div className="flex items-center bg-white rounded-lg shadow-md">
                <input
                  type="text"
                  placeholder="Search our website..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-grow px-4 py-2 rounded-l-lg focus:outline-none text-[#4a58b5]"
                />
                <button
                  type="submit"
                  className="bg-[#fabb84] text-white px-4 py-2 rounded-r-lg hover:bg-[#fc6453] transition-colors duration-200"
                >
                  <Search size={20} />
                </button>
              </div>
            </form>

            <div className="text-center">
              <Link
                href="/"
                className="inline-block bg-[#fabb84] text-white px-6 py-2 rounded-lg font-semibold hover:bg-[#fc6453] transition-colors duration-200"
              >
                Return to Home
              </Link>
            </div>
          </motion.div>
        </div>
      </main>

      <footer className="bg-[#4a58b5] text-white py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">&copy; 2024 Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}