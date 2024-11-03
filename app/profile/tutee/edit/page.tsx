'use client'

import { useState } from 'react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, School, GraduationCap, Book, Mail, Phone, MapPin, Upload, Save } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

// Mock data for a tutee's profile
const initialTuteeData = {
  id: 1,
  name: 'Jane Smith',
  email: 'jane.smith@example.com',
  phoneNumber: '+1234567890',
  school: 'Springfield High School',
  level: 'Secondary 3',
  subjects: 'Mathematics, Physics, Chemistry',
  imageUrl: '/placeholder.svg?height=200&width=200',
  address: '123 Tutee St, Studyville, SG 12345',
}

export default function TuteeProfileEditPage() {
  const router = useRouter()
  const [tuteeData, setTuteeData] = useState(initialTuteeData)
  const [newImage, setNewImage] = useState<File | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setTuteeData(prev => ({ ...prev, [name]: value }))
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setNewImage(e.target.files[0])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the updated data to your backend
    console.log('Updated tutee data:', tuteeData)
    console.log('New image:', newImage)
    // After successful update, redirect to the profile view page
    router.push('/profile/tutee')
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

          <div className="mb-6">
            <label htmlFor="imageUpload" className="block text-sm font-medium text-[#4a58b5] mb-2">Profile Picture</label>
            <div className="flex items-center">
              <Image
                src={newImage ? URL.createObjectURL(newImage) : tuteeData.imageUrl}
                alt={tuteeData.name}
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
              value={tuteeData.name}
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
              value={tuteeData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-[#4a58b5] mb-1">Phone Number</label>
            <input
              type="tel"
              id="phoneNumber"
              name="phoneNumber"
              value={tuteeData.phoneNumber}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="school" className="block text-sm font-medium text-[#4a58b5] mb-1">School</label>
            <input
              type="text"
              id="school"
              name="school"
              value={tuteeData.school}
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
              value={tuteeData.level}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="subjects" className="block text-sm font-medium text-[#4a58b5] mb-1">Subjects</label>
            <input
              type="text"
              id="subjects"
              name="subjects"
              value={tuteeData.subjects}
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
              value={tuteeData.address}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
            />
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