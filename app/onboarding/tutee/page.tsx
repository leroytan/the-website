'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

const inter = Inter({ subsets: ['latin'] })

export default function TuteeOnboarding() {
  const router = useRouter() 
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    {
      title: "Welcome to Your Learning Journey!",
      content: (
        <div>
          <p>We’re excited to have you here. Let’s set you up for success!</p>
        </div>
      ),
    },
    {
      title: "Choose Your Subjects",
      content: (
        <div>
          <p>Select the subjects you want to focus on:</p>
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
      title: "Set Your Availability",
      content: (
        <div>
          <p>Let us know when you’re available for tutoring sessions.</p>
          {/* Include a simple scheduling interface or form */}
        </div>
      ),
    },
    {
      title: "Get Matched with Tutors",
      content: (
        <div>
          <p>We will match you with the best tutors based on your preferences.</p>
          <Link href="/dashboard/tutee" className="btn">Go to Dashboard</Link>
        </div>
      ),
    },
  ]

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      router.push('/dashboard/tutee')
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
