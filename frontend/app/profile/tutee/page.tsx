'use client'

import { Inter } from 'next/font/google'
import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, Mail, Phone, School, GraduationCap, BookOpen, MapPin, Pencil } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

// Mock data for a tutee's profile
const tuteeData = {
  id: 1,
  name: 'Jane Smith',
  email: 'jane.smith@example.com',
  phoneNumber: '+1234567890',
  school: 'Springfield High School',
  level: 'Secondary 3',
  subjects: ['Mathematics', 'Physics', 'Chemistry'],
  imageUrl: '/placeholder.svg?height=200&width=200',
  address: '123 Tutee St, Studyville, SG 12345',
}

export default function TuteeProfilePage() {
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
          <Link href="/profile/tutee/edit">
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
            src={tuteeData.imageUrl}
            alt={tuteeData.name}
            width={128}
            height={128}
            className="rounded-full border-4 border-[#fabb84]"
          />
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-[#4a58b5] mb-1">{tuteeData.name}</h1>
            <p className="text-xl text-[#4a58b5] mb-4">Tutee</p>
            <div className="space-y-2">
              <div className="flex items-center text-[#4a58b5]">
                <Mail className="w-5 h-5 mr-2" />
                <span>{tuteeData.email}</span>
              </div>
              <div className="flex items-center text-[#4a58b5]">
                <Phone className="w-5 h-5 mr-2" />
                <span>{tuteeData.phoneNumber}</span>
              </div>
              <div className="flex items-center text-[#4a58b5]">
                <MapPin className="w-5 h-5 mr-2" />
                <span>{tuteeData.address}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <h2 className="text-2xl font-bold text-[#4a58b5]">Tutee Information</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <School className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">School</h3>
              </div>
              <p className="text-gray-900">{tuteeData.school}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <GraduationCap className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Level</h3>
              </div>
              <p className="text-gray-900">{tuteeData.level}</p>
            </div>
            <div>
              <div className="flex items-center text-[#4a58b5] mb-2">
                <BookOpen className="w-5 h-5 mr-2 text-[#fabb84]" />
                <h3 className="text-lg font-semibold">Subjects</h3>
              </div>
              <p className="text-gray-900">{tuteeData.subjects.join(', ')}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}