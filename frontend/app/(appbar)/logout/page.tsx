'use client'
 
import { useAuth } from '@/context/authContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
 
export default function Logout() {
  const router = useRouter()
  const { logout: logoutAuth } = useAuth();

  const logout = async () => {
    await fetch(`/api/auth/logout`, { method: 'POST' });
    logoutAuth();
    router.push('/');
  };

  useEffect(() => {
    logout();
    // Only run once on mount
  }, []);

  return null;
}