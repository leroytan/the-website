'use client'

import { useState, useEffect, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Book, CheckCircle, Award, Linkedin, ArrowRight, Search, X } from 'lucide-react'
import { Inter } from 'next/font/google'
import { Header } from '../components/Header'

const inter = Inter({ subsets: ['latin'] })

// Define a type for courses
type Course = {
  id: number
  title: string
  description: string
  progress: number
  completed: boolean
}

// Mock data for courses
const mockCourses: Course[] = [
  {
    id: 1,
    title: 'Effective Teaching Strategies',
    description: 'Learn modern teaching techniques to engage students effectively.',
    progress: 75,
    completed: false,
  },
  {
    id: 2,
    title: 'Digital Tools for Education',
    description: 'Master the latest digital tools to enhance your teaching methods.',
    progress: 100,
    completed: true,
  },
  {
    id: 3,
    title: 'Student Psychology',
    description: 'Understand student behavior and motivation to improve learning outcomes.',
    progress: 30,
    completed: false,
  },
  {
    id: 4,
    title: 'Curriculum Development',
    description: 'Learn how to design and implement effective educational curricula.',
    progress: 0,
    completed: false,
  },
]

const CourseCard = ({ course, onComplete }: { course: Course; onComplete: (id: number) => void }) => {
  const router = useRouter()

  const handleContinueCourse = () => {
    router.push(`/courses/${course.id}`)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
    >
      <h3 className="text-xl font-bold mb-2 text-[#4a58b5]">{course.title}</h3>
      <p className="text-[#4a58b5] mb-4">{course.description}</p>
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-[#4a58b5]">Progress</span>
          <span className="text-sm font-medium text-[#4a58b5]">{course.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-[#fabb84] h-2.5 rounded-full"
            style={{ width: `${course.progress}%` }}
          ></div>
        </div>
      </div>
      {course.completed ? (
        <div className="flex justify-between items-center">
          <span className="text-green-500 font-medium flex items-center">
            <CheckCircle size={20} className="mr-2" />
            Completed
          </span>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onComplete(course.id)}
            className="bg-[#4a58b5] text-white px-4 py-2 rounded-md hover:bg-[#3a4795] transition-colors duration-200 text-sm font-medium"
          >
            Get Certificate
          </motion.button>
        </div>
      ) : (
        <div className="flex justify-end">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleContinueCourse}
            className="bg-[#fabb84] text-white px-4 py-2 rounded-full hover:bg-[#fc6453] transition-colors duration-200 text-sm font-medium flex items-center"
          >
            Continue
            <ArrowRight size={16} className="ml-2" />
          </motion.button>
        </div>
      )}
    </motion.div>
  )
}

export default function CoursesPage() {
  const [courses] = useState<Course[]>(mockCourses)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCertificate, setShowCertificate] = useState(false)
  const [completedCourseId, setCompletedCourseId] = useState<number | null>(null)

  const filteredCourses = useMemo(
    () =>
      courses.filter((course) =>
        `${course.title} ${course.description}`.toLowerCase().includes(searchTerm.toLowerCase())
      ),
    [searchTerm, courses]
  )

  const handleCompleteCourse = (courseId: number) => {
    setCompletedCourseId(courseId)
    setShowCertificate(true)
  }

  const handleAddToLinkedIn = () => {
    alert('Certificate added to LinkedIn successfully!')
    setShowCertificate(false)
  }

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value)
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <Header toggleSubpage={function (): void {
              throw new Error('Function not implemented.')
          } } />
      <main className="pt-16 sm:pt-20 md:pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8 relative">
            <input
              type="text"
              placeholder="Search courses..."
              value={searchTerm}
              onChange={handleSearch}
              className="w-full px-4 py-2 pl-10 pr-4 text-[#4a58b5] bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84] shadow-sm"
              aria-label="Search courses"
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredCourses.map((course) => (
                <CourseCard key={course.id} course={course} onComplete={handleCompleteCourse} />
              ))}
            </AnimatePresence>
          </div>

          {filteredCourses.length === 0 && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center text-[#4a58b5] mt-8 text-lg"
            >
              No courses found. Try adjusting your search.
            </motion.p>
          )}

          {showCertificate && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4"
            >
              <div className="bg-white rounded-lg p-8 max-w-md w-full">
                <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">Congratulations!</h2>
                <p className="text-[#4a58b5] mb-6">
                  You have completed the course: {courses.find((c) => c.id === completedCourseId)?.title}
                </p>
                <div className="flex justify-between">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleAddToLinkedIn}
                    className="bg-[#0077b5] text-white px-4 py-2 rounded-md hover:bg-[#006097] transition-colors duration-200 flex items-center"
                  >
                    <Linkedin size={20} className="mr-2" />
                    Add to LinkedIn
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowCertificate(false)}
                    className="bg-gray-300 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors duration-200"
                  >
                    Close
                  </motion.button>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}
