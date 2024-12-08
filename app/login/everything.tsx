// lib/auth.ts
export const checkAuth = async () => {
  try {
    const response = await fetch('/api/protected', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // In Next.js, we use this instead of credentials: 'include'
      credentials: 'same-origin'
    });

    if (!response.ok) {
      throw new Error('Unauthorized');
    }

    const data = await response.json();
    return { authenticated: true, data };
  } catch (error) {
    return { authenticated: false, error };
  }
};

// components/LoginForm.tsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { Alert, AlertDescription } from '@/components/ui/alert';

const LoginForm = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Invalid username or password');
        }
        throw new Error('Login failed');
      }

      const data = await response.json();
      
      // Store user type in localStorage
      localStorage.setItem('userType', data.userType);
      
      // Note: We don't need to store the token as it's in an HTTP-only cookie
      router.push('/protected');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  // ... rest of the form component remains the same ...
};

// pages/protected.tsx
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { checkAuth } from '@/lib/auth';

export default function ProtectedPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const verifyAuth = async () => {
      const { authenticated, data: authData, error } = await checkAuth();
      
      if (!authenticated) {
        router.push('/login');
        return;
      }

      setData(authData);
      setIsLoading(false);
    };

    verifyAuth();
  }, [router]);

  if (isLoading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div>;
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
  );
}

// pages/api/protected.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { verify } from 'jsonwebtoken';

const SECRET_KEY = process.env.JWT_SECRET!;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Get the token from the cookie
    const token = req.cookies.auth_token;

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    // Verify the token
    const decoded = verify(token, SECRET_KEY);

    // Return protected data
    return res.status(200).json({
      message: 'You have access to protected data',
      user: decoded
    });
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// middleware.ts (Next.js middleware for protecting routes)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Get the token from the cookies
  const token = request.cookies.get('auth_token');

  // If there's no token and the user is trying to access protected routes
  if (!token && request.nextUrl.pathname.startsWith('/protected')) {
    // Redirect to the login page
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

// Configure which routes to protect
export const config = {
  matcher: ['/protected/:path*']
};