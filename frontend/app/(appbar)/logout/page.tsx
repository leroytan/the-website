'use client'
 
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
 
export default function Logout() {

  const router = useRouter()

  useEffect(() => {
    logout()
  })

  const logout = async () => {
    const response = await fetch('/api/auth/logout', { method: 'POST' })
    if (!response.ok) {
    }
    const data = await response.json()
    console.log(data)
    router.push('/')
    router.refresh()
  }
}