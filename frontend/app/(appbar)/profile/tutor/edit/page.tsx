'use client'

import { useState } from 'react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, Star, DollarSign, Book, GraduationCap, Mail, Calendar, Award, Briefcase, FileText, MapPin, Upload, Save } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

// Mock data for a tutor's profile
const initialTutorData = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@example.com',
  subjects: ['Mathematics', 'Physics'],
  levels: ['Secondary 1', 'Secondary 2', 'Secondary 3', 'Secondary 4'],
  rating: 4.8,
  ratePerHour: 30,
  imageUrl: '/placeholder.svg?height=200&width=200',
  highestQualification: "Master's Degree",
  resume: '/path/to/resume.pdf',
  subjectsTeachable: 'Mathematics, Physics, Computer Science',
  levelsTeachable: 'Secondary 1 to Junior College',
  rate: '$30-$50 per hour depending on subject and level',
  specialSkills: 'Problem-solving techniques, Visual learning methods',
  bio: "I'm a passionate educator with a Master's degree in Mathematics and 5 years of tutoring experience. I specialize in breaking down complex concepts into easy-to-understand pieces, making learning enjoyable and effective. My students have consistently improved their grades and developed a love for math and physics.",
  roughLocation: 'Central Singapore',
}

export default function TutorProfileEditPage() {
  const router = useRouter()
  const [tutorData, setTutorData] = useState(initialTutorData)
  const [newImage, setNewImage] = useState<File | null>(null)
  const [newResume, setNewResume] = useState<File | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setTutorData(prev => ({ ...prev, [name]: value }))
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setNewImage(e.target.files[0])
    }
  }

  const handleResumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setNewResume(e.target.files[0])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the updated data to your backend
    console.log('Updated tutor data:', tutorData)
    console.log('New image:', newImage)
    console.log('New resume:', newResume)
    // After successful update, redirect to the profile view page
    router.push('/profile/tutor')
  }

  const handleBack = () => {
    router.back()
  }

  return (
    <div className={`min-h-screen bg-[#fff2de] py-12 px-4 sm:px-6 lg:px-8 ${inter.className}`}>
      <div className="max-w-4xl mx-auto">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleBack}
          className="mb-6 flex items-center text-[#4a58b5] hover:text-[#fabb84]"
        >
          <ArrowLeft size={20} className="mr-2" />
          Back to Profile
        </motion.button>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold text-[#4a58b5] mb-6">Edit Your Profile</h1>

          <div className="mb-6">
            <label htmlFor="imageUpload" className="block text-sm font-medium text-[#4a58b5] mb-2">Profile Picture</label>
            <div className="flex items-center">
              <Image
                src={newImage ? URL.createObjectURL(newImage) : tutorData.imageUrl}
                alt={tutorData.name}
                width={100}
                height={100}
                className="rounded-full mr-4 border-2 border-[#fabb84]"
              />
              <input
                type="file"
                id="imageUpload"
                accept="image/*"
                onChange={handleImageChange}
                className="hidden"
              />
              <label htmlFor="imageUpload" className="cursor-pointer bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200">
                <Upload size={20} className="inline mr-2" />
                Upload New Picture
              </label>
            </div>
          </div>

          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-[#4a58b5] mb-1">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={tutorData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-[#4a58b5] mb-1">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={tutorData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="highestQualification" className="block text-sm font-medium text-[#4a58b5] mb-1">Highest Qualification</label>
            <input
              type="text"
              id="highestQualification"
              name="highestQualification"
              value={tutorData.highestQualification}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="rate" className="block text-sm font-medium text-[#4a58b5] mb-1">Rate</label>
            <input
              type="text"
              id="rate"
              name="rate"
              value={tutorData.rate}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="roughLocation" className="block text-sm font-medium text-[#4a58b5] mb-1">General Location</label>
            <input
              type="text"
              id="roughLocation"
              name="roughLocation"
              value={tutorData.roughLocation}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="bio" className="block text-sm font-medium text-[#4a58b5] mb-1">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={tutorData.bio}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              rows={4}
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="subjectsTeachable" className="block text-sm font-medium text-[#4a58b5] mb-1">Subjects Teachable</label>
            <input
              type="text"
              id="subjectsTeachable"
              name="subjectsTeachable"
              value={tutorData.subjectsTeachable}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="levelsTeachable" className="block text-sm font-medium text-[#4a58b5] mb-1">Levels Teachable</label>
            <input
              type="text"
              id="levelsTeachable"
              name="levelsTeachable"
              value={tutorData.levelsTeachable}
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
              value={tutorData.specialSkills}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="resumeUpload" className="block text-sm font-medium text-[#4a58b5] mb-2">Resume</label>
            <div className="flex items-center">
              <input
                type="file"
                id="resumeUpload"
                accept=".pdf"
                onChange={handleResumeChange}
                className="hidden"
              />
              <label htmlFor="resumeUpload" className="cursor-pointer bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200">
                <Upload size={20} className="inline mr-2" />
                Upload New Resume
              </label>
              {newResume && <span className="ml-2 text-[#4a58b5]">{newResume.name}</span>}
            </div>
          </div>

          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200 flex items-center justify-center"
          >
            <Save size={20} className="mr-2" />
            Save Changes
          </motion.button>
        </form>
      </div>
    </div>
  )
}