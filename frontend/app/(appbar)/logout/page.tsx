'use client'
 
import { useAuth } from '@/context/authContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
 
export default function Logout() {

  const router = useRouter()
  const { logout: logoutAuth } = useAuth();
  useEffect(() => {
    logout()
  })

  const logout = async () => {
    
    const response = await fetch(`/api/auth/logout`, { method: 'POST' })
    if (!response.ok) {
    }
    await logoutAuth()
    
    router.push('/')
    router.refresh()
  }
}