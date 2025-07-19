'use client';

import { CheckCircle2 } from 'lucide-react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Button } from '@/components/button';
import { fetchClient } from '@/utils/fetch/fetchClient';

const PaymentSuccess = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const tutorId = searchParams.get('tutor_id');
  const chatId = searchParams.get('chat_id');

  const [isLoading, setIsLoading] = useState(true);
  const [paymentStatus, setPaymentStatus] = useState('');

  useEffect(() => {
    if (sessionId) {
      // Simulate fetching the payment status
      setIsLoading(false);
      setPaymentStatus('Payment was successful!');
      // In a real-world scenario, you would verify the session_id with your backend here.
    }
  }, [sessionId]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#fff2de] via-[#fabb84]/30 to-[#4a58b5]/10 flex flex-col items-center justify-center">
        <h2 className="text-3xl font-semibold text-[#4a58b5] animate-pulse">Loading...</h2>
      </div>
    );
  }

  const handleStartChat = async () => {
    if (chatId) {
      router.push(`/chat?chatId=${chatId}`);
      return;
    }
    if (!tutorId) {
      console.error('Tutor ID is required to start a chat.');
      return;
    }
    // Fetching the chat creation or retrieval
    const response = await fetchClient(`/api/chat/get-or-create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ other_user_id: tutorId }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Failed to create chat: ${error.message}`);
    }

    const chatPreview = await response.json();
    router.push(`/chat?chatId=${chatPreview.id}`);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#fff2de] via-[#fabb84]/30 to-[#4a58b5]/10">
      <div className="bg-white/90 rounded-3xl shadow-2xl px-8 py-12 flex flex-col items-center max-w-md w-full">
        <div className="mb-6">
          <CheckCircle2 size={72} className="text-[#4a58b5] drop-shadow-lg" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#4a58b5] mb-2 text-center">Payment Successful!</h1>
        <h2 className="text-lg sm:text-xl font-medium text-[#4a58b5] mb-4 text-center">{paymentStatus}</h2>
        <p className="text-[#4a58b5] mb-8 text-base sm:text-lg text-center">
          Your payment was successfully processed.<br />Your conversation with the tutor is now fully unlocked!
        </p>
        <div className="flex gap-3 w-full justify-center">
          <Button
            onClick={handleStartChat}
            className="px-4 py-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 w-36"
          >
            Open Chat
          </Button>
          <Link href="/" className="w-36">
            <Button className="px-4 py-2 flex items-center bg-white text-customDarkBlue border border-customDarkBlue rounded-full hover:bg-orange-50 transition-colors duration-200 shadow-sm">
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PaymentSuccess;
