// app/components/LoginIcon.tsx
'use client'

import { useState } from 'react'

export default function LoginIcon() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  const toggleLogin = () => {
    setIsLoggedIn(!isLoggedIn)
  }

  return (
    <button
      onClick={toggleLogin}
      className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition-colors duration-200"
    >
      {isLoggedIn ? (
        <>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="font-medium">Logged In</span>
        </>
      ) : (
        <>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          <span className="font-medium">Login</span>
        </>
      )}
    </button>
  )
}