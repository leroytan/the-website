'use client'

import { useEffect, useRef } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
import FocusTrap from 'focus-trap-react'

interface SubpageProps {
  isOpen: boolean
  onClose: () => void
}

const menuItems = [
  { href: "/", label: "Home" },
  { href: "#features", label: "Features" },
  { href: "#why-join-us", label: "Why Join Us" },
  { href: "#team", label: "Team" },
  { href: "#programmes", label: "Programmes" },
  { href: "#reviews", label: "Reviews" },
]

export default function Subpage({ isOpen, onClose }: SubpageProps) {
  const firstItemRef = useRef<HTMLAnchorElement>(null)

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose()
      }
    }
    window.addEventListener("keydown", handleEscape)
    return () => window.removeEventListener("keydown", handleEscape)
  }, [onClose])

  useEffect(() => {
    if (isOpen) {
      firstItemRef.current?.focus()
    }
  }, [isOpen])

  return (
    <AnimatePresence>
      {isOpen && (
        <FocusTrap>
          <div>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.5 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="fixed inset-0 bg-black z-40"
              onClick={onClose}
              aria-hidden="true"
            />
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="fixed top-0 left-0 w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-1/4 h-full bg-white shadow-lg z-50 overflow-y-auto"
            >
              <div className="p-6">
                <div className="flex justify-between items-center mb-8">
                  <h2 className="text-2xl font-bold text-[#4a58b5]">Menu</h2>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={onClose}
                    className="text-[#4a58b5] focus:outline-none focus:ring-2 focus:ring-[#fabb84] rounded-full p-1"
                    aria-label="Close menu"
                  >
                    <X size={24} />
                  </motion.button>
                </div>
                <nav aria-label="Main navigation">
                  <ul className="space-y-4">
                    {menuItems.map((item, index) => (
                      <motion.li
                        key={item.href}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Link
                          href={item.href}
                          className="text-lg font-semibold text-[#4a58b5] hover:text-[#fabb84] transition-colors duration-200 block py-2 focus:outline-none focus:ring-2 focus:ring-[#fabb84] rounded"
                          onClick={onClose}
                          ref={index === 0 ? firstItemRef : null}
                        >
                          {item.label}
                        </Link>
                      </motion.li>
                    ))}
                  </ul>
                </nav>
              </div>
            </motion.div>
          </div>
        </FocusTrap>
      )}
    </AnimatePresence>
  )
}