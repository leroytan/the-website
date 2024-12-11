'use client'

import { motion } from 'framer-motion'
import { Inter } from 'next/font/google'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function ProtectedPage() {
  const router = useRouter()

  // Simulating an authentication check state
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Simulating a function to check if the user is authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Make a request to check the user's authentication status (could be a token validation call)
        const res = await fetch('/api/protected', {
          method: 'GET',
        })
        
        if (res.status === 200) {
          setIsAuthenticated(true)
          return
        }

        const ref = await fetch('/api/auth/refresh', {
          method: 'POST'
        })

        if (ref.status === 200) {
          setIsAuthenticated(true)
          return
        }

        setIsAuthenticated(false)
        setError('You are not logged in or your session has expired.')
        alert('Bye bye')
        
      } catch (err) {
        setError('Error checking authentication.')
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  // If the user is not authenticated, redirect them to the login page
  if (!loading && !isAuthenticated) {
    setTimeout(() => router.push('/login'), 5000)
    return null
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 ${inter.className}`}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <div className="flex justify-center mb-6">
          <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">Protected Page</h2>
        </div>

        {loading ? (
          <p className="text-center text-lg text-[#4a58b5]">Loading...</p>
        ) : error ? (
          <p className="text-center text-lg text-red-500">{error}</p>
        ) : (
          <div>
            <p className="text-center text-lg text-[#4a58b5] mb-6">
              Welcome to the protected page! You are successfully authenticated.
            </p>
            <motion.button
              onClick={() => {
                fetch('/api/auth/logout', {
                  method: 'POST',
                })

                router.push('/login')
              }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
            >
              Log Out
            </motion.button>
          </div>
        )}
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-8 text-center text-xs text-[#4a58b5]"
      >
        &copy; 2024 Teach . Honour . Excel. All rights reserved.
      </motion.p>
    </div>
  )
}
