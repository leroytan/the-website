'use client'

import { useState } from 'react'
import { Inter } from 'next/font/google'
import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, Star, DollarSign, Book, GraduationCap, Mail, Calendar, Award, Briefcase, FileText, MapPin } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

// Mock data for a tutor, including information from onboarding
const mockTutor = {
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

export default function TutorProfilePage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [showMessageForm, setShowMessageForm] = useState(false)
  const [message, setMessage] = useState('')

  // In a real app, you'd fetch the tutor data based on the ID
  const tutor = mockTutor

  const handleBack = () => {
    router.back()
  }

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the message to your backend
    console.log('Message sent:', message)
    setMessage('')
    setShowMessageForm(false)
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
          Back to Tutors
        </motion.button>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col md:flex-row items-center md:items-start mb-6">
            <Image
              src={tutor.imageUrl}
              alt={tutor.name}
              width={200}
              height={200}
              className="rounded-full mb-4 md:mb-0 md:mr-6 border-4 border-[#fabb84]"
            />
            <div>
              <h1 className="text-3xl font-bold text-[#4a58b5] mb-2">{tutor.name}</h1>
              <div className="flex items-center text-[#fabb84] mb-2">
                <Star size={20} className="mr-1" fill="#fabb84" />
                <span className="font-medium text-lg">{tutor.rating.toFixed(1)}</span>
              </div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <Mail size={20} className="mr-2 text-[#fc6453]" />
                <span>{tutor.email}</span>
              </div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <GraduationCap size={20} className="mr-2 text-[#fc6453]" />
                <span>{tutor.highestQualification}</span>
              </div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <DollarSign size={20} className="mr-2 text-[#fc6453]" />
                <span>{tutor.rate}</span>
              </div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <MapPin size={20} className="mr-2 text-[#fc6453]" />
                <span>{tutor.roughLocation}</span>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-2">About Me</h2>
            <p className="text-[#4a58b5]">{tutor.bio}</p>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-2">Subjects Teachable</h2>
            <div className="flex items-center text-[#4a58b5]">
              <Book size={20} className="mr-2 text-[#fc6453]" />
              <span>{tutor.subjectsTeachable}</span>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-2">Levels Teachable</h2>
            <div className="flex items-center text-[#4a58b5]">
              <GraduationCap size={20} className="mr-2 text-[#fc6453]" />
              <span>{tutor.levelsTeachable}</span>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-2">Special Skills</h2>
            <div className="flex items-center text-[#4a58b5]">
              <Award size={20} className="mr-2 text-[#fc6453]" />
              <span>{tutor.specialSkills}</span>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-2">Resume</h2>
            <Link href={tutor.resume} target="_blank" rel="noopener noreferrer">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center px-4 py-2 bg-[#4a58b5] text-white rounded-md hover:bg-[#3a4795] transition-colors duration-200"
              >
                <FileText size={20} className="mr-2" />
                View Resume
              </motion.button>
            </Link>
          </div>

          {!showMessageForm ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowMessageForm(true)}
              className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200 font-medium"
            >
              Message Tutor
            </motion.button>
          ) : (
            <motion.form
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              onSubmit={handleSendMessage}
              className="space-y-4"
            >
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message here..."
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                rows={4}
              />
              <div className="flex justify-end space-x-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  type="button"
                  onClick={() => setShowMessageForm(false)}
                  className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
                >
                  Cancel
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  type="submit"
                  className="px-4 py-2 bg-[#fabb84] text-white rounded-md hover:bg-[#fc6453] transition-colors duration-200"
                >
                  Send Message
                </motion.button>
              </div>
            </motion.form>
          )}
        </div>
      </div>
    </div>
  )
}