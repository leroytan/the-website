'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

const inter = Inter({ subsets: ['latin'] })

export default function TutorOnboarding() {
  const router = useRouter()

  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    {
      title: "Welcome to Your Tutoring Journey!",
      content: (
        <div>
          <p>We’re thrilled to have you join our team of tutors!</p>
        </div>
      ),
    },
    {
      title: "Define Your Expertise",
      content: (
        <div>
          <p>Select the subjects you’re comfortable teaching:</p>
          <ul>
            <li>Math</li>
            <li>Science</li>
            <li>Languages</li>
            <li>More...</li>
          </ul>
        </div>
      ),
    },
    {
      title: "Set Your Schedule",
      content: (
        <div>
          <p>Let us know your available times for tutoring sessions.</p>
          {/* Include a simple scheduling interface or form */}
        </div>
      ),
    },
    {
      title: "Get Ready to Teach!",
      content: (
        <div>
          <p>You're all set! Start connecting with your students.</p>
          <Link href="/dashboard/tutor" className="btn">Go to Dashboard</Link>
        </div>
      ),
    },
  ]

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      router.push('/dashboard/tutor')
    }
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className} flex flex-col justify-center items-center`}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white rounded-lg shadow-md p-6 w-full max-w-md"
      >
        <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">{steps[currentStep].title}</h2>
        <div className="mb-4">{steps[currentStep].content}</div>
        <button onClick={nextStep} className="bg-[#4a58b5] text-white px-4 py-2 rounded">
          {currentStep < steps.length - 1 ? "Next" : "Finish"}
        </button>
      </motion.div>
    </div>
  )
}
