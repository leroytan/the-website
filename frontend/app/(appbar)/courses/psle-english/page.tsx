'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ChevronLeft, ChevronRight, CheckCircle, Lock, BookOpen } from 'lucide-react'
import { motion } from 'framer-motion'
import { Inter } from 'next/font/google'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

type courseModule = {
  id: number
  title: string
  completed: boolean
  locked: boolean
  videoUrl: string
}

const courseModules: courseModule[] = [
  { id: 1, title: "Introduction to PSLE English", completed: true, locked: false, videoUrl: "https://example.com/video1.mp4" },
  { id: 2, title: "Grammar Essentials", completed: false, locked: false, videoUrl: "https://example.com/video2.mp4" },
  { id: 3, title: "Vocabulary Building", completed: false, locked: false, videoUrl: "https://example.com/video3.mp4" },
  { id: 4, title: "Comprehension Techniques", completed: false, locked: true, videoUrl: "https://example.com/video4.mp4" },
  { id: 5, title: "Essay Writing Skills", completed: false, locked: true, videoUrl: "https://example.com/video5.mp4" },
  { id: 6, title: "Oral Communication", completed: false, locked: true, videoUrl: "https://example.com/video6.mp4" },
  { id: 7, title: "Listening Comprehension", completed: false, locked: true, videoUrl: "https://example.com/video7.mp4" },
  { id: 8, title: "Exam Strategies and Practice", completed: false, locked: true, videoUrl: "https://example.com/video8.mp4" },
]

export default function ModulePage() {
  const router = useRouter()
  const [completedModules, setCompletedModules] = useState(1)

  const progress = (completedModules / courseModules.length) * 100

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
    <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Link href="/courses" className="text-[#4a58b5] hover:underline flex items-center">
            <ChevronLeft size={20} className="mr-1" />
            Back to Courses
          </Link>
        </div>

        <h1 className="text-3xl font-bold text-[#4a58b5] text-center mb-8">PSLE English Course</h1>

        <div className="grid gap-6 md:grid-cols-2 mb-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex items-center mb-4">
              <BookOpen size={24} className="text-[#4a58b5] mr-2" />
              <h2 className="text-xl font-semibold text-[#4a58b5]">Course Overview</h2>
            </div>
            <p className="text-[#4a58b5] mb-4">
              Master essential English language skills and prepare effectively for your PSLE examination. This comprehensive course covers grammar, vocabulary, comprehension, and more.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-[#4a58b5] mb-4">Course Progress</h2>
            <div className="w-full h-4 bg-gray-200 rounded-full mb-2">
              <div
                className="h-full bg-[#fabb84] rounded-full transition-all duration-500 ease-in-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-[#4a58b5]">{completedModules} of {courseModules.length} modules completed</p>
          </motion.div>
        </div>

        <div className="grid gap-4">
          {courseModules.map((module) => (
            <motion.div
              key={module.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-lg shadow-md p-4 flex items-center justify-between"
            >
              <div className="flex items-center">
                {module.completed ? (
                  <CheckCircle className="text-green-500 mr-2" size={20} />
                ) : module.locked ? (
                  <Lock className="text-gray-400 mr-2" size={20} />
                ) : null}
                <span className={`text-lg ${module.locked ? 'text-gray-400' : 'text-[#4a58b5]'}`}>{module.title}</span>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => router.push(`/courses/psle-english/module/${module.id}`)}
                disabled={module.locked}
                className={`px-4 py-2 rounded-md ${
                  module.locked
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-[#fabb84] text-white hover:bg-[#fc6453]'
                }`}
              >
                {module.completed ? 'Review' : 'Start'}
              </motion.button>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

