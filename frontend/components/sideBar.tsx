'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '../context/authContext';

type SidebarProps = {
  isOpen: boolean;
  onClose: () => void;
};

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { isAuthenticated } = useAuth();
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: '-100%' }}
          animate={{ x: 0 }}
          exit={{ x: '-100%' }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
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
              
              <li>
              <Link href="/" className="text-lg font-semibold hover:underline" onClick={onClose}>
              Home
              </Link>
              </li>
              <li>
                <Link href="/tutors" className="text-lg font-semibold hover:underline" onClick={onClose}>
                  THE Tutors
                </Link>
              </li>
              <li>
                <Link href="/assignments" className="text-lg font-semibold hover:underline" onClick={onClose}>
                  THE Assignments
                </Link>
              </li>
              {isAuthenticated && (
              <li>
                <Link href="/chat/tutee" className="text-lg font-semibold hover:underline " onClick={onClose}>
                  Chat
                </Link>
              </li>
              )}
            </ul>
          </nav>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Sidebar;
