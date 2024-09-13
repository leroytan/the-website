'use client'
// app/components/BurgerMenu.tsx

import { useState } from 'react'

export default function BurgerMenu() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <>
      <button
        className="text-blue-500 hover:text-blue-700 focus:outline-none transition-colors duration-200"
        onClick={toggleMenu}
      >
        <svg
          className="h-8 w-8"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      <nav
        className={`fixed top-0 left-0 bottom-0 flex flex-col w-64 bg-white shadow-lg transform ${
          isMenuOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out`}
      >
        <div className="p-4 bg-blue-600">
          <button
            className="text-white hover:text-blue-200 focus:outline-none transition-colors duration-200"
            onClick={toggleMenu}
          >
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <ul className="flex flex-col py-4">
          <li>
            <a href="#" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-100 transition-colors duration-200">
              Home
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-100 transition-colors duration-200">
              About
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-100 transition-colors duration-200">
              Contact
            </a>
          </li>
        </ul>
      </nav>
    </>
  )
}