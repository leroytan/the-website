'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ChevronLeft, ChevronRight } from 'lucide-react'
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

export default function ModuleVideoPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [progress, setProgress] = useState(0)
  const [completed, setCompleted] = useState(false)
  const moduleId = parseInt(params.id)
  const currentModule = courseModules.find(m => m.id === moduleId)
  const currentIndex = courseModules.findIndex(m => m.id === moduleId)
  const prevModule = currentIndex > 0 ? courseModules[currentIndex - 1] : null
  const nextModule = currentIndex < courseModules.length - 1 ? courseModules[currentIndex + 1] : null

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer)
          setCompleted(true)
          return 100
        }
        return prev + 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  if (!currentModule) return null

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <Link href="/courses/psle-english/module" className="text-[#4a58b5] hover:underline">
            Back to Modules
          </Link>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => prevModule && router.push(`/courses/psle-english/module/${prevModule.id}`)}
              disabled={!prevModule}
              className={`p-2 rounded-full ${!prevModule ? 'text-gray-400 cursor-not-allowed' : 'text-[#4a58b5] hover:bg-[#fabb84] hover:text-white'}`}
            >
              <ChevronLeft size={20} />
            </button>
            <button
              onClick={() => nextModule && !nextModule.locked && router.push(`/courses/psle-english/module/${nextModule.id}`)}
              disabled={!nextModule || nextModule.locked}
              className={`p-2 rounded-full ${!nextModule || nextModule.locked ? 'text-gray-400 cursor-not-allowed' : 'text-[#4a58b5] hover:bg-[#fabb84] hover:text-white'}`}
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h1 className="text-3xl font-bold text-[#4a58b5] mb-4">{currentModule.title}</h1>
          <video
            src={currentModule.videoUrl}
            controls
            className="w-full aspect-video mb-4"
          />
          <div className="w-full h-2 bg-gray-200 rounded-full mb-2">
            <div
              className="h-full bg-[#fabb84] rounded-full"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="text-sm text-[#4a58b5]">{progress}% completed</p>
        </div>

        {completed && (
          <div className="flex justify-end">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push(`/courses/psle-english/module/${nextModule?.id || moduleId}`)}
              className="bg-[#fabb84] hover:bg-[#fc6453] text-white px-4 py-2 rounded-md"
            >
              {nextModule ? 'Next Module' : 'Complete Course'}
            </motion.button>
          </div>
        )}
      </div>
    </div>
  )
}

