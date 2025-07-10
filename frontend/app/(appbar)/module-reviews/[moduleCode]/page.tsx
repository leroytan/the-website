'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { motion } from 'framer-motion'
import { ChevronLeft, Star } from 'lucide-react'
import { Inter } from 'next/font/google'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

type Review = {
  yearSem: string
  workload: number
  difficulty: number
  overview: string
  otherPoints: string[]
  reviewer: {
    year: number
    course: string
    specialization: string
  }
}

type Module = {
  code: string
  name: string
  reviews: Review[]
}

// This would typically come from an API or database
const getModuleData = (moduleCode: string): Module | null => {
  const allModules = [
    {
      code: "XXX1701",
      name: "Introduction to Business",
      reviews: [
        {
          yearSem: "AY23/24 Sem 1",
          workload: 4,
          difficulty: 3,
          overview: "A comprehensive introduction to business concepts and practices.",
          otherPoints: [
            "Weekly tutorials are helpful",
            "Group project is manageable"
          ],
          reviewer: {
            year: 2,
            course: "Business",
            specialization: "BID"
          }
        },
        {
          yearSem: "AY22/23 Sem 2",
          workload: 3,
          difficulty: 2,
          overview: "Good foundation for business studies. Covers a wide range of topics.",
          otherPoints: [
            "Lectures are engaging",
            "Exams are fair"
          ],
          reviewer: {
            year: 3,
            course: "Business",
            specialization: "Finance"
          }
        }
      ]
    },
    // Add more modules here...
  ]

  return allModules.find(module => module.code === moduleCode) || null
}

export default function ModuleReviewsPage() {
  const params = useParams()
  const moduleCode = params.moduleCode as string
  const [moduleData, setModuleData] = useState<Module | null>(null)

  useEffect(() => {
    const data = getModuleData(moduleCode)
    setModuleData(data)
  }, [moduleCode])

  if (!moduleData) {
    return <div>Loading...</div>
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <main className="pt-24 pb-12">
        <div className="container mx-auto px-4">
          <Link href="/module-reviews" className="inline-flex items-center text-[#4a58b5] hover:text-[#fabb84] mb-4">
            <ChevronLeft size={20} />
            <span>Back to all modules</span>
          </Link>
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl sm:text-3xl font-bold text-[#4a58b5] mb-2"
          >
            {moduleData.code}: {moduleData.name}
          </motion.h1>
          <p className="text-[#4a58b5] mb-6">Module Reviews</p>

          {/*<div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="Search reviews..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 pl-10 pr-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#4a58b5]"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            </div>
          </div>*/}

          <div className="space-y-6">
            {moduleData.reviews.map((review, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="bg-white rounded-lg shadow-md p-6"
              >
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Year/Sem taken</h3>
                  <p className="text-[#4a58b5]">{review.yearSem}</p>
                </div>

                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Workload</h3>
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        size={24}
                        className={star <= review.workload ? "fill-[#fabb84] text-[#fabb84]" : "text-gray-300"}
                      />
                    ))}
                  </div>
                </div>

                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Difficulty</h3>
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        size={24}
                        className={star <= review.difficulty ? "fill-[#fabb84] text-[#fabb84]" : "text-gray-300"}
                      />
                    ))}
                  </div>
                </div>

                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">General Overview of Course</h3>
                  <p className="text-[#4a58b5]">{review.overview}</p>
                </div>

                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Other Points</h3>
                  <ul className="list-disc pl-5 text-[#4a58b5]">
                    {review.otherPoints.map((point, index) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>

                <div className="flex items-center pt-4 border-t">
                  <div className="w-12 h-12 rounded-full bg-[#4a58b5] text-white flex items-center justify-center mr-4">
                    👤
                  </div>
                  <div>
                    <p className="font-semibold text-[#4a58b5]">
                      Year {review.reviewer.year} {review.reviewer.course} Student NUS
                    </p>
                    <p className="text-[#4a58b5]">{review.reviewer.specialization}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </main>

      <footer className="bg-[#4a58b5] text-white py-4 sm:py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-xs sm:text-sm">&copy; {new Date().getFullYear()} Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}


