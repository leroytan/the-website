'use client'

import { useState } from 'react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import { motion } from 'framer-motion'
import { Upload } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

interface OnboardingPageProps {
  userType: string
  name: string
  email: string
  password: string
}

export default function OnboardingPage({ userType, name: initialName, email, password }: OnboardingPageProps) {
  const [formData, setFormData] = useState({
    name: initialName,
    school: '',
    level: '',
    subjects: '',
    address: '',
    phoneNumber: '',
    highestQualification: '',
    resume: null as File | null,
    subjectsTeachable: '',
    rate: '',
    specialSkills: '',
  })
  const [phoneVerified, setPhoneVerified] = useState(false)
  const [verificationCode, setVerificationCode] = useState('')
  const [showVerificationInput, setShowVerificationInput] = useState(false)

  const qualificationOptions = [
    'High School Diploma',
    'Associate\'s Degree',
    'Bachelor\'s Degree',
    'Master\'s Degree',
    'Ph.D.',
    'Other'
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({ ...formData, resume: e.target.files[0] })
    }
  }

  const handleVerifyPhone = () => {
    // Simulating sending a verification code
    console.log('Sending verification code to', formData.phoneNumber)
    setShowVerificationInput(true)
  }

  const handleVerifyCode = () => {
    // Simulating code verification
    console.log('Verifying code', verificationCode)
    setPhoneVerified(true)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (userType === 'tutor' && !phoneVerified) {
      alert('Please verify your phone number before submitting.')
      return
    }
    console.log('Signup completed with:', { userType, email, password, ...formData })
    // Here you would typically send this data to your backend
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 py-8 ${inter.className}`}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-6 sm:p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <div className="flex justify-center mb-6">
          <Image
            src="/public/images/logo.png"
            alt="THE Logo"
            width={150}
            height={75}
            className="w-32 sm:w-40"
          />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">
          {userType === 'tutee' ? 'Tutee Onboarding' : 'Tutor Onboarding'}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-[#4a58b5] mb-1">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>
          {userType === 'tutee' ? (
            <>
              <div className="mb-4">
                <label htmlFor="school" className="block text-sm font-medium text-[#4a58b5] mb-1">School</label>
                <input
                  type="text"
                  id="school"
                  name="school"
                  value={formData.school}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="level" className="block text-sm font-medium text-[#4a58b5] mb-1">Level</label>
                <input
                  type="text"
                  id="level"
                  name="level"
                  value={formData.level}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="subjects" className="block text-sm font-medium text-[#4a58b5] mb-1">Subject(s)</label>
                <input
                  type="text"
                  id="subjects"
                  name="subjects"
                  value={formData.subjects}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="address" className="block text-sm font-medium text-[#4a58b5] mb-1">Address</label>
                <input
                  type="text"
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
            </>
          ) : (
            <>
              <div className="mb-4">
                <label htmlFor="highestQualification" className="block text-sm font-medium text-[#4a58b5] mb-1">Highest Qualification</label>
                <select
                  id="highestQualification"
                  name="highestQualification"
                  value={formData.highestQualification}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                >
                  <option value="">Select your highest qualification</option>
                  {qualificationOptions.map((option) => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label htmlFor="resume" className="block text-sm font-medium text-[#4a58b5] mb-1">Resume (PDF)</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div className="space-y-1 text-center">
                    <Upload className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="flex text-sm text-gray-600">
                      <label htmlFor="resume" className="relative cursor-pointer bg-white rounded-md font-medium text-[#fabb84] hover:text-[#fc6453] focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-[#fabb84]">
                        <span>Upload a file</span>
                        <input
                          id="resume"
                          name="resume"
                          type="file"
                          accept=".pdf"
                          className="sr-only"
                          onChange={handleFileChange}
                          required
                        />
                      </label>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs text-gray-500">PDF up to 10MB</p>
                  </div>
                </div>
                {formData.resume && (
                  <p className="mt-2 text-sm text-gray-500">
                    File selected: {formData.resume.name}
                  </p>
                )}
              </div>
              <div className="mb-4">
                <label htmlFor="subjectsTeachable" className="block text-sm font-medium text-[#4a58b5] mb-1">Subjects Teachable</label>
                <input
                  type="text"
                  id="subjectsTeachable"
                  name="subjectsTeachable"
                  value={formData.subjectsTeachable}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="rate" className="block text-sm font-medium text-[#4a58b5] mb-1">Rate (for different subjects/levels)</label>
                <input
                  type="text"
                  id="rate"
                  name="rate"
                  value={formData.rate}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
              <div className="mb-4">
                <label htmlFor="specialSkills" className="block text-sm font-medium text-[#4a58b5] mb-1">Special Skills</label>
                <input
                  type="text"
                  id="specialSkills"
                  name="specialSkills"
                  value={formData.specialSkills}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                  required
                />
              </div>
            </>
          )}
          <div className="mb-6">
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-[#4a58b5] mb-1">Phone Number</label>
            <div className="flex">
              <input
                type="tel"
                id="phoneNumber"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleChange}
                className="flex-grow px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                required
              />
              <button
                type="button"
                onClick={handleVerifyPhone}
                className="px-4 py-2 bg-[#fabb84] text-white rounded-r-md hover:bg-[#fc6453] transition-colors duration-200"
                disabled={phoneVerified}
              >
                {phoneVerified ? 'Verified' : 'Verify'}
              </button>
            </div>
            {showVerificationInput && !phoneVerified && (
              <div className="mt-2">
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  placeholder="Enter verification code"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                />
                <button
                  type="button"
                  onClick={handleVerifyCode}
                  className="mt-2 w-full px-4 py-2 bg-[#fabb84] text-white rounded-md hover:bg-[#fc6453] transition-colors duration-200"
                >
                  Verify Code
                </button>
              </div>
            )}
          </div>
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
          >
            Signup
          </motion.button>
        </form>
      </motion.div>
    </div>
  )
}