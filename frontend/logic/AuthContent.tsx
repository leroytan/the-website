'use client'
import { redirect } from 'next/navigation'
import React, { createContext, useContext, useEffect, useState } from 'react'

interface AuthContextType {
  isAuthenticated: boolean
  loading: boolean
  error: string | null
  login: (email: string, password: string, userType: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch('/api/protected', { method: 'GET' })
        if (res.status === 200) {
          setIsAuthenticated(true)
          return
        }

        const ref = await fetch('/api/auth/refresh', { method: 'POST' })
        if (ref.status === 200) {
          setIsAuthenticated(true)
          return
        }

        setIsAuthenticated(false)
        setError('You are not logged in or your session has expired.')
      } catch (err) {
        setError('Error checking authentication.')
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])
  const login = async (email: string, password: string, userType: string) => {
    setLoading(true)
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, userType }), // Pass email and password in the request body
      })
  
      if (res.status === 200) {
        setIsAuthenticated(true)
        setError(null)
      } else {
        setIsAuthenticated(false)
        setError('Login failed. Please check your credentials.')
      }
    } catch (err) {
      setError('Error during login. Please try again later.')
    } finally {
      setLoading(false)
      redirect('/')
    }
  }
  const logout = () => {
    setIsAuthenticated(false)
    setError(null)
    fetch('/api/auth/logout', { method: 'POST' }).catch(() => {
      console.error('Error during logout.')
    })
    redirect('/')
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}