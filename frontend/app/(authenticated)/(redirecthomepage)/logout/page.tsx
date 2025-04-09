'use client'
 
import { useAuth } from '@/logic/AuthContent'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
 
export default function Logout() {
  const { logout } = useAuth()
  const router = useRouter()

  useEffect(() => {
    logout()
  })
}