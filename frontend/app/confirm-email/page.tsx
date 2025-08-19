"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, Loader2 } from "lucide-react";
import Link from "next/link";

function ConfirmEmailContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'already-verified' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const confirmEmail = async () => {
      const token = searchParams.get('token');
      
      if (!token) {
        setStatus('error');
        setMessage('Invalid confirmation link. Please check your email for the correct link.');
        return;
      }

      try {
        const response = await fetch('/api/auth/confirm-email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ confirmation_token: token }),
        });

        const data = await response.json();

        if (response.ok) {
          // Check if email is already verified
          if (data.message && data.message.includes('already verified')) {
            setStatus('already-verified');
            setMessage(data.message);
          } else {
            setStatus('success');
            setMessage(data.message || 'Email confirmed successfully!');
          }
        } else {
          setStatus('error');
          setMessage(data.detail || data.message || 'Failed to confirm email. Please try again.');
        }
      } catch (error) {
        setStatus('error');
        setMessage('An unexpected error occurred. Please try again.');
      }
    };

    confirmEmail();
  }, [searchParams]);

  return (
    <div className="min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full"
      >
        <div className="text-center">
          {status === 'loading' && (
            <>
              <Loader2 className="mx-auto h-12 w-12 text-blue-500 animate-spin mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Confirming Your Email
              </h1>
              <p className="text-gray-600">
                Please wait while we verify your email address...
              </p>
            </>
          )}

          {status === 'success' && (
            <>
              <CheckCircle className="mx-auto h-12 w-12 text-green-500 mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Email Confirmed!
              </h1>
              <p className="text-gray-600 mb-6">
                {message}
              </p>
              <Link
                href="/login"
                className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Continue to Login
              </Link>
            </>
          )}

          {status === 'already-verified' && (
            <>
              <CheckCircle className="mx-auto h-12 w-12 text-blue-500 mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Email Already Verified
              </h1>
              <p className="text-gray-600 mb-6">
                {message}
              </p>
              <Link
                href="/login"
                className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Continue to Login
              </Link>
            </>
          )}

          {status === 'error' && (
            <>
              <XCircle className="mx-auto h-12 w-12 text-red-500 mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Confirmation Failed
              </h1>
              <p className="text-gray-600 mb-6">
                {message}
              </p>
              <div className="space-y-3">
                <Link
                  href="/login"
                  className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Go to Login
                </Link>
                <div className="text-sm text-gray-500">
                  Need a new confirmation link?{' '}
                  <Link href="/login" className="text-blue-600 hover:underline">
                    Contact support
                  </Link>
                </div>
              </div>
            </>
          )}
        </div>
      </motion.div>
    </div>
  );
}

function ConfirmEmailFallback() {
  return (
    <div className="min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <div className="text-center">
          <Loader2 className="mx-auto h-12 w-12 text-blue-500 animate-spin mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Loading...
          </h1>
          <p className="text-gray-600">
            Please wait while we load the confirmation page...
          </p>
        </div>
      </div>
    </div>
  );
}

export default function ConfirmEmailPage() {
  return (
    <Suspense fallback={<ConfirmEmailFallback />}>
      <ConfirmEmailContent />
    </Suspense>
  );
} 