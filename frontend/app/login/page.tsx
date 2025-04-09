'use client'

import { motion } from 'framer-motion'
import { Eye, EyeOff } from 'lucide-react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

import { useRouter } from 'next/navigation'

const inter = Inter({ subsets: ['latin'] })

export default function LoginPage() {
  const router = useRouter()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [userType, setUserType] = useState('tutee')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    console.log('Login attempted with:', { email, password, userType })

    console.log('Sending login request...')
    
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, userType })
    })

    console.log('Login response:', res)

    // if status code 401, show error message
    if (res.status === 401) {
      alert('Invalid email or password')
      return
    }

    // if successful, redirect to protected page
    router.push('/protected')
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
          <Image
            src="/images/logo.png"
            alt="THE Logo"
          width={150}
            height={75}
            className="w-32 sm:w-40"
          />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">Login to THE</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-[#4a58b5] mb-2">I am logging in as:</label>
            <div className="flex space-x-4">
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  className="form-radio text-[#fabb84]"
                  name="userType"
                  value="tutee"
                  checked={userType === 'tutee'}
                  onChange={(e) => setUserType(e.target.value)}
                />
                <span className="ml-2 text-[#4a58b5]">Tutee/Parent</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  className="form-radio text-[#fabb84]"
                  name="userType"
                  value="tutor"
                  checked={userType === 'tutor'}
                  onChange={(e) => setUserType(e.target.value)}
                />
                <span className="ml-2 text-[#4a58b5]">Tutor</span>
              </label>
            </div>
          </div>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-[#4a58b5] mb-1">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
              aria-required="true"
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-medium text-[#4a58b5] mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                required
                aria-required="true"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="h-5 w-5 text-gray-500" /> : <Eye className="h-5 w-5 text-gray-500" />}
              </button>
            </div>
          </div>
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
          >
            Log In
          </motion.button>
        </form>
        <p className="mt-4 text-center text-sm text-[#4a58b5]">
          Don't have an account?{' '}
          <Link href="/signup" className="text-[#fc6453] hover:underline">
            Sign up
          </Link>
        </p>
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