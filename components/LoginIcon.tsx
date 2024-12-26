'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, LogOut } from 'lucide-react';
import Link from 'next/link';

const LoginIcon = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Simulate checking user's login status (replace with real authentication logic)
    setIsLoggedIn(true);

    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    // Simulate logout process (replace with real logout logic)
    setIsLoggedIn(false);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen((prev) => !prev)}
        className="text-[#4a58b5]"
        aria-label="User menu"
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
            {isLoggedIn ? (
              <>
                <Link
                  href="/profile"
                  className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
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
                <Link
                  href="/login"
                  className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
                  Log In
                </Link>
                <Link
                  href="/signup"
                  className="block px-4 py-2 text-sm text-[#4a58b5] hover:bg-[#fabb84] hover:text-white"
                >
                  Sign Up
                </Link>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LoginIcon;
