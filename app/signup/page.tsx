'use client'

import React, { useState } from 'react'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import Image from 'next/image'
import { motion } from 'framer-motion'
import { Eye, EyeOff } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { select } from 'framer-motion/client'

const inter = Inter({ subsets: ['latin'] })

const ROLES = ['Tutor', 'Tutee'] as const

export default function SignupPage() {
  const router = useRouter()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [selectedRole, setSelectedRole] = useState('Select Role');

  const [errorMessage, setErrorMessage] = useState('')
  const [token, setToken] = useState('') // dummy function for token

  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => setIsOpen((prev) => !prev);

  const handleSelect = (role: string) => {
    setSelectedRole(role);
    setIsOpen(false);
  };
  

  const submitSignup = async (e: React.FormEvent) => {

    if (selectedRole === 'Select Role') {
      setErrorMessage('Invalid role')
      return;
    }

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, userType: selectedRole.toLowerCase() }),
    }

    const response = await fetch('/api/auth/signup', requestOptions)
    const data = await response.json()

    if (!response.ok) {
      setErrorMessage(data.detail)
      console.error(data.detail)  // TODO: show the error message to the user
      return;
    }

    setToken(data.token)
    if (selectedRole === 'Tutor') {
      router.push('/onboarding/tutor')
    } else {
      router.push('/onboarding/tutee')
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Signup attempted with:', name, email, password, selectedRole)
    submitSignup(e)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 py-8 ${inter.className}`}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-6 sm:p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <div className="flex justify-center mb-6">
          <Image
            src=""
            alt="T.H.E. Logo"
            width={150}
            height={75}
            className="w-32 sm:w-40"
          />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">Sign Up for T.H.E.</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-[#4a58b5] mb-1">Name</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
              aria-required="true"
            />
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
          I am a...
          <div className="relative w-100">
            {/* Dr`opdown Button */}
            <button
              onClick={toggleDropdown}
              className="w-full px-4 py-2 bg-gray-200 rounded-lg text-left font-medium 
                        hover:bg-gray-300 focus:outline-none transition-colors"
            >
              {selectedRole}
            </button>

            {/* Dropdown List */}
            {isOpen && (
              <ul
                className="absolute w-full mt-2 bg-white shadow-md rounded-lg border border-gray-300 z-10"
              >
                {ROLES.map((role) => (
                  <li
                    key={role}
                    onClick={() => handleSelect(role)}
                    className="px-4 py-2 hover:bg-blue-500 hover:text-white cursor-pointer transition-colors"
                  >
                    {role}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <br></br>
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
          >
            Sign Up
          </motion.button>
        </form>
        <p className="mt-4 text-center text-sm text-[#4a58b5]">
          Already have an account?{' '}
          <Link href="/login" className="text-[#fc6453] hover:underline">
            Log in
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