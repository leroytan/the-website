'use client'

import { useAuth } from "@/context/authContext"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Mail, GraduationCap, School, Pencil } from "lucide-react"
import Link from "next/link"
import { fetchClient } from "@/utils/fetch/fetchClient";
import { UserImage } from "@/components/userImage"

interface UserProfile {
  id: number
  name: string
  email: string
  profile_photo_url: string | undefined
  intends_to_be_tutor: boolean
  created_at: string
  updated_at: string
}

export default function TuteeProfilePage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [profile, setProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push('/login?redirectTo=/profile/tutee')
        return
      }
      
      // Fetch user profile data
      const fetchProfile = async () => {
        try {
          const response = await fetchClient(`/api/me`)
          if (!response.ok) throw new Error('Failed to fetch profile')
          const data = await response.json()
          setProfile(data.user)
        } catch (error) {
          console.error('Error fetching profile:', error)
        }
      }
      
      fetchProfile()
    }
  }, [user, loading, router])

  if (loading || !profile) {
    return <div>Loading...</div>
  }

  return (
    <div className="min-h-screen bg-customLightYellow px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center gap-6 relative">
        <div className="absolute top-4 right-4">
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
        <div className="relative">
          <UserImage user={{ photo_url: profile.profile_photo_url, name: profile.name }} width={140} height={140} />
        
        </div>

        <div className="flex-1">
          <h1 className="text-2xl font-semibold text-customDarkBlue mb-2">{profile.name}</h1>
          <div className="space-y-2 mt-4">
            <div className="flex items-center text-customDarkBlue">
              <Mail className="w-5 h-5 mr-2 text-customOrange" />
              <span>{profile.email}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 bg-white shadow-lg rounded-xl p-6">
          <h3 className="text-customDarkBlue font-semibold text-lg mb-4">About Me</h3>
          <p className="text-gray-600">
            {profile.intends_to_be_tutor ? "I am interested in becoming a tutor." : "I am looking for tutoring services."}
          </p>
        </div>

        <div className="md:col-span-2 bg-white shadow-lg rounded-xl p-6">
          <h3 className="text-customDarkBlue font-semibold text-lg mb-4">Account Information</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center text-customDarkBlue mb-2">
                <School className="w-5 h-5 mr-2 text-customOrange" />
                <h4 className="font-semibold">Member Since</h4>
              </div>
              <p className="text-gray-600">
                {new Date(profile.created_at).toLocaleDateString()}
              </p>
            </div>
            <div>
              <div className="flex items-center text-customDarkBlue mb-2">
                <GraduationCap className="w-5 h-5 mr-2 text-customOrange" />
                <h4 className="font-semibold">Last Updated</h4>
              </div>
              <p className="text-gray-600">
                {new Date(profile.updated_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}