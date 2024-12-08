'use client' 

import { useEffect, useState } from 'react' 
import { useRouter } from 'next/navigation' 
import { checkAuth } from '@/lib/auth' 

export default function ProtectedPage() {
  const router = useRouter() 
  const [isLoading, setIsLoading] = useState(true) 
  const [data, setData] = useState<any>(null) 
  const [error, setError] = useState<string | null>(null) 

  useEffect(() => {
    const verifyAuth = async () => {
      const { authenticated, data: authData, error } = await checkAuth() 
      
      if (!authenticated) {
        router.push('/login') 
        return 
      }

      setData(authData) 
      setIsLoading(false) 
    } 

    verifyAuth() 
  }, [router]) 

  if (isLoading) {
    return <div className="p-4">Loading...</div> 
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div> 
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Protected Page</h1>
      <div>
        <p>Welcome! You are authenticated.</p>
        <pre className="mt-4 p-4 bg-gray-100 rounded">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  ) 
}