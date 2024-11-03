'use client'

import { useState, useEffect } from 'react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Star, DollarSign, Book, Filter, X, GraduationCap } from 'lucide-react'
import { Header } from '../components/Header'

const inter = Inter({ subsets: ['latin'] })

// Mock data for tutors (expanded with levels)
const mockTutors = [
  {
    id: 1,
    name: 'John Doe',
    subjects: ['Mathematics', 'Physics'],
    levels: ['Primary 5', 'Primary 6', 'Secondary 1'],
    rating: 4.8,
    ratePerHour: 30,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '5 years',
    availability: 'Weekdays, Evenings',
  },
  {
    id: 2,
    name: 'Jane Smith',
    subjects: ['English', 'Literature'],
    levels: ['Primary 3', 'Primary 4', 'Primary 5'],
    rating: 4.9,
    ratePerHour: 35,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '7 years',
    availability: 'Weekends, Mornings',
  },
  {
    id: 3,
    name: 'Mike Johnson',
    subjects: ['Chemistry', 'Biology'],
    levels: ['Secondary 2', 'Secondary 3', 'Secondary 4'],
    rating: 4.7,
    ratePerHour: 28,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '3 years',
    availability: 'Flexible',
  },
  {
    id: 4,
    name: 'Sarah Lee',
    subjects: ['History', 'Geography'],
    levels: ['Primary 4', 'Primary 5', 'Primary 6'],
    rating: 4.6,
    ratePerHour: 25,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '4 years',
    availability: 'Weekdays, Afternoons',
  },
  {
    id: 5,
    name: 'David Chen',
    subjects: ['Computer Science', 'Mathematics'],
    levels: ['Secondary 3', 'Secondary 4', 'Junior College'],
    rating: 4.9,
    ratePerHour: 40,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '8 years',
    availability: 'Evenings, Weekends',
  },
  {
    id: 6,
    name: 'Emily Brown',
    subjects: ['Art', 'Design'],
    levels: ['Primary 1', 'Primary 2', 'Primary 3'],
    rating: 4.8,
    ratePerHour: 32,
    imageUrl: '/placeholder.svg?height=100&width=100',
    experience: '6 years',
    availability: 'Weekends',
  },
]

const TutorCard = ({ tutor }) => (
  <motion.div
    layout="position"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
    transition={{ duration: 0.2, ease: "linear" }}
    className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
  >
    <div className="flex items-center mb-4">
      <Image
        src={tutor.imageUrl}
        alt={tutor.name}
        width={80}
        height={80}
        className="rounded-full mr-4 border-2 border-[#fabb84]"
      />
      <div>
        <h3 className="text-xl font-semibold text-[#4a58b5]">{tutor.name}</h3>
        <div className="flex items-center text-[#fabb84]">
          <Star size={16} className="mr-1" fill="#fabb84" />
          <span className="font-medium">{tutor.rating.toFixed(1)}</span>
        </div>
      </div>
    </div>
    <div className="mb-4 space-y-2">
      <div className="flex items-center text-[#4a58b5]">
        <Book size={16} className="mr-2 text-[#fc6453]" />
        <span>{tutor.subjects.join(', ')}</span>
      </div>
      <div className="flex items-center text-[#4a58b5]">
        <GraduationCap size={16} className="mr-2 text-[#fc6453]" />
        <span>{tutor.levels.join(', ')}</span>
      </div>
      <div className="flex items-center text-[#4a58b5]">
        <DollarSign size={16} className="mr-2 text-[#fc6453]" />
        <span>${tutor.ratePerHour}/hour</span>
      </div>
      <div className="flex items-center text-[#4a58b5]">
        <span className="font-medium mr-2">Experience:</span>
        <span>{tutor.experience}</span>
      </div>
      <div className="flex items-center text-[#4a58b5]">
        <span className="font-medium mr-2">Availability:</span>
        <span>{tutor.availability}</span>
      </div>
    </div>
    <Link href={`/tutors/${tutor.id}`}>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200 font-medium"
      >
        View Profile
      </motion.button>
    </Link>
  </motion.div>
)

const Sidebar = ({ isOpen, onClose }) => {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose()
      }
    }
    window.addEventListener("keydown", handleEscape)
    return () => window.removeEventListener("keydown", handleEscape)
  }, [onClose])

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: "-100%" }}
          animate={{ x: 0 }}
          exit={{ x: "-100%" }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
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
              <li><Link href="/dashboard/tutee" className="text-lg font-semibold hover:underline">Dashboard</Link></li>
              <li><Link href="/courses" className="text-lg font-semibold hover:underline">THE Courses</Link></li>
              <li><Link href="/tutors" className="text-lg font-semibold hover:underline">THE Tutors</Link></li>
              <li><Link href="/schedule" className="text-lg font-semibold hover:underline">My Schedule</Link></li>
              <li><Link href="/messages" className="text-lg font-semibold hover:underline">Messages</Link></li>
            </ul>
          </nav>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default function TutorBrowsePage() {
  const [tutors, setTutors] = useState(mockTutors)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedSubjects, setSelectedSubjects] = useState([])
  const [selectedLevels, setSelectedLevels] = useState([])
  const [showFilters, setShowFilters] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  useEffect(() => {
    setTutors(mockTutors)
  }, [])

  const allSubjects = Array.from(new Set(mockTutors.flatMap(tutor => tutor.subjects)))
  const allLevels = Array.from(new Set(mockTutors.flatMap(tutor => tutor.levels)))

  const filteredTutors = tutors.filter(tutor =>
    (tutor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tutor.subjects.some(subject => subject.toLowerCase().includes(searchTerm.toLowerCase()))) &&
    (selectedSubjects.length === 0 || tutor.subjects.some(subject => selectedSubjects.includes(subject))) &&
    (selectedLevels.length === 0 || tutor.levels.some(level => selectedLevels.includes(level)))
  )

  const toggleSubject = (subject) => {
    setSelectedSubjects(prev =>
      prev.includes(subject)
        ? prev.filter(s => s !== subject)
        : [...prev, subject]
    )
  }

  const toggleLevel = (level) => {
    setSelectedLevels(prev =>
      prev.includes(level)
        ? prev.filter(l => l !== level)
        : [...prev, level]
    )
  }

  const toggleSubpage = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      <Header toggleSubpage={toggleSubpage} />
      
      <main className="pt-16 sm:pt-20 md:pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold text-[#4a58b5] mb-8 text-center">THE Tutors</h1>
          
          <div className="mb-8 flex flex-col sm:flex-row items-center gap-4">
            <div className="relative flex-grow">
              <input
                type="text"
                placeholder="Search tutors by name or subject"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 pl-10 pr-4 text-[#4a58b5] bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center justify-center px-4 py-2 bg-[#4a58b5] text-white rounded-md hover:bg-[#3a4795] transition-colors duration-200"
            >
              <Filter size={20} className="mr-2" />
              Filters
            </motion.button>
          </div>

          <AnimatePresence>
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2, ease: "linear" }}
                className="mb-8 bg-white p-4 rounded-md shadow-md overflow-hidden"
              >
                <h3 className="text-lg font-semibold text-[#4a58b5] mb-4">Filter by Subject:</h3>
                <div className="flex flex-wrap gap-2 mb-4">
                  {allSubjects.map(subject => (
                    <motion.button
                      key={subject}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => toggleSubject(subject)}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        selectedSubjects.includes(subject)
                          ? 'bg-[#fabb84] text-white'
                          : 'bg-gray-200 text-[#4a58b5]'
                      }`}
                    >
                      {subject}
                    </motion.button>
                  ))}
                </div>
                <h3 className="text-lg font-semibold text-[#4a58b5] mb-4">Filter by Level:</h3>
                <div className="flex flex-wrap gap-2">
                  {allLevels.map(level => (
                    <motion.button
                      key={level}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => toggleLevel(level)}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        selectedLevels.includes(level)
                          ? 'bg-[#fabb84] text-white'
                          : 'bg-gray-200 text-[#4a58b5]'
                      }`}
                    >
                      {level}
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <motion.div 
            layout
            transition={{ duration: 0.2, ease: "linear" }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            <AnimatePresence>
              {filteredTutors.map(tutor => (
                <TutorCard key={tutor.id} tutor={tutor} />
              ))}
            </AnimatePresence>
          </motion.div>

          {filteredTutors.length === 0 && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2, ease: "linear" }}
              className="text-center text-[#4a58b5] mt-8 text-lg"
            >
              No tutors found. Try adjusting your search or filters.
            </motion.p>
          )}
        </div>
      </main>

      <footer className="bg-[#4a58b5] text-white py-4 sm:py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-xs sm:text-sm">&copy; 2024 Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}