'use client'

import { Inter } from 'next/font/google'
import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, Mail, Phone, GraduationCap, BookOpen, DollarSign, Star, Pencil, MapPin, FileText } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

// Mock data for a tutor's profile
const tutorData = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@example.com',
  phoneNumber: '+1234567890',
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

export default function TutorProfilePage() {
  const router = useRouter()

  const handleBackClick = () => {
    router.back()
  }
  
  return (
    <div className={`min-h-screen bg-[#fff2de] p-6 ${inter.className}`}>
      <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-lg p-8">
        <div className="flex justify-between items-center mb-8">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleBackClick}
            className="text-[#4a58b5] hover:text-[#fabb84]"
          >
            <ArrowLeft size={24} />
          </motion.button>
          <Link href="/profile/tutor/edit">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center text-[#fabb84] hover:text-[#fc6453]"
            >
              <Pencil size={20} className="mr-2" />
              <span>Edit Profile</span>
            </motion.div>
          </Link>
        </div>

        <div className="flex items-start gap-6 mb-12">
          <Image
            src={tutorData.imageUrl}
            alt={tutorData.name}
            width={128}
            height={128}
            className="rounded-full border-4 border-[#fabb84]"
          />
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-[#4a58b5] mb-1">{tutorData.name}</h1>
            <p className="text-xl text-[#4a58b5] mb-2">Tutor</p>
            <div className="flex items-center text-[#fabb84] mb-4">
              <Star className="w-5 h-5 mr-1" fill="#fabb84" />
              <span className="font-medium text-lg">{tutorData.rating.toFixed(1)}</span>
            </div>
            <div className="space-y-2">
              <div className="flex items-center text-[#4a58b5]">
                <Mail className="w-5 h-5 mr-2" />
                <span>{tutorData.email}</span>
              </div>
              <div className="flex items-center text-[#4a58b5]">
                <Phone className="w-5 h-5 mr-2" />
                <span>{tutorData.phoneNumber}</span>
              </div>
              <div className="flex items-center text-[#4a58b5]">
                <MapPin className="w-5 h-5 mr-2" />
                <span>{tutorData.roughLocation}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <h2 className="text-2xl font-bold text-[#4a58b5]">Tutor Information</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <GraduationCap className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Highest Qualification</h3>
              </div>
              <p className="text-gray-900">{tutorData.highestQualification}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <BookOpen className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Subjects Teachable</h3>
              </div>
              <p className="text-gray-900">{tutorData.subjectsTeachable}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <GraduationCap className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Levels Teachable</h3>
              </div>
              <p className="text-gray-900">{tutorData.levelsTeachable}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <DollarSign className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Rate</h3>
              </div>
              <p className="text-gray-900">{tutorData.rate}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <Star className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Special Skills</h3>
              </div>
              <p className="text-gray-900">{tutorData.specialSkills}</p>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">About Me</h2>
          <p className="text-gray-900">{tutorData.bio}</p>
        </div>

        <div className="mt-8">
          <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">Resume</h2>
          <Link href={tutorData.resume} target="_blank" rel="noopener noreferrer">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center bg-[#4a58b5] text-white py-2 px-4 rounded-md hover:bg-[#3a4795] transition-colors duration-200"
            >
              <FileText size={20} className="mr-2" />
              View Resume
            </motion.button>
          </Link>
        </div>
      </div>
    </div>
  )
}