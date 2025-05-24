'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, X, User, ChevronDown, ChevronRight, Search, Star } from 'lucide-react'
import { Inter } from 'next/font/google'
import { motion, AnimatePresence } from 'framer-motion'

const inter = Inter({ subsets: ['latin'] })

type Major = {
  name: string
  modules: Module[]
}

type Module = {
  code: string
  name: string
  reviews: Review[]
}

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

const majors: Major[] = [
  {
    name: "Business Administration",
    modules: [
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
          }
        ]
      },
      {
        code: "XXX1702",
        name: "Business Analytics",
        reviews: []
      },
      {
        code: "XXX1703",
        name: "Marketing Management",
        reviews: []
      }
    ]
  },
  {
    name: "Computer Science",
    modules: [
      {
        code: "CS1101S",
        name: "Programming Methodology",
        reviews: []
      }
    ]
  },
  {
    name: "CHS",
    modules: [
      {
        code: "HSI1000",
        name: "How Science Works",
        reviews: []
      }
    ]
  }
]

export default function ModuleReviewPage() {
  const [selectedMajor, setSelectedMajor] = useState<Major | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  const filteredMajors = majors.filter(major => 
    major.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    major.modules.some(module => 
      module.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      module.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  const filteredModules = selectedMajor
    ? selectedMajor.modules.filter(module =>
        module.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        module.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : []

  return (
    <div className={`min-h-screen flex flex-col bg-[#fff2de] ${inter.className}`}>
      <main className="flex-grow pt-24 pb-12">
        <div className="container mx-auto px-4 flex flex-col h-full">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl sm:text-3xl font-bold text-[#4a58b5] mb-6 sm:mb-8"
          >
          </motion.h1>
          
          <div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="Search majors or modules..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 pl-10 pr-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#4a58b5]"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1 bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-[#4a58b5] mb-4">Majors</h2>
              <ul className="space-y-2">
                {filteredMajors.map((major) => (
                  <motion.li
                    key={major.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <button
                      onClick={() => setSelectedMajor(major)}
                      className={`w-full text-left p-2 rounded-lg ${
                        selectedMajor?.name === major.name
                          ? 'bg-[#4a58b5] text-white'
                          : 'text-[#4a58b5] hover:bg-[#fabb84] hover:text-white'
                      }`}
                    >
                      {major.name}
                    </button>
                  </motion.li>
                ))}
              </ul>
            </div>

            <div className="md:col-span-2">
              {selectedMajor && (
                <>
                  <div className="grid gap-4">
                    {filteredModules.map((module) => (
                      <motion.div
                        key={module.code}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Link href={`/module-reviews/${module.code}`} className="block">
                          <div className="bg-white rounded-lg shadow-md p-4 text-left hover:shadow-lg transition-shadow">
                            <h3 className="text-lg font-semibold text-[#4a58b5]">{module.code}</h3>
                            <p className="text-[#4a58b5]">{module.name}</p>
                          </div>
                        </Link>
                      </motion.div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
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

