'use client'
 
import { useRouter } from 'next/navigation'
 
export default function Logout() {

  const router = useRouter()

  const logout = async () => {
    const response = await fetch('/api/auth/logout', { method: 'POST' })
    if (!response.ok) {
      throw new Error('Failed to log out')
    }
    const data = await response.json()
  
    setTimeout(() => {
      console.log(data);
      router.push('/')
    }, 5000)
  }

  logout()
}