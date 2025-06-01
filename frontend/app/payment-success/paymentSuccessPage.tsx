'use client'; // Make sure this is a client-side component

import { motion } from 'framer-motion';
import Image from 'next/image';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Home, Search } from 'react-feather'; // Assuming you're using React Feather icons

const PaymentSuccess = () => {
  const router = useRouter();

  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const tutorId = searchParams.get('tutor_id');
  const chatId = searchParams.get('chat_id');

  const [isLoading, setIsLoading] = useState(true);
  const [paymentStatus, setPaymentStatus] = useState("");

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
      <div className="min-h-screen bg-[#fff2de] flex flex-col items-center justify-center">
        <h2 className="text-3xl font-semibold text-[#4a58b5]">Loading...</h2>
      </div>
    );
  }

  const handleStartChat = async () => {
    if (chatId) {
      router.push(`/chat/tutee?chatId=${chatId}`);
    }
    if (!tutorId) {
      console.error("Tutor ID is required to start a chat.");
      return;
    }
    // Fetching the chat creation or retrieval
    const response = await fetch(`/api/chat/get-or-create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ other_user_id: tutorId }), // Assuming tutor_id is the "other_user_id"
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Failed to create chat: ${error.message}`);
    }

    const chatPreview = await response.json();
    router.push(`/chat/tutee?chatId=${chatPreview.id}`);
  };

  return (
    <div className={`min-h-screen bg-[#fff2de] flex flex-col`}>
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="text-[#4a58b5] hover:text-[#fabb84] transition-colors">
            <Home size={24} />
          </Link>
          <Image
            src="/images/logo.png"
            alt="THE Logo"
            width={100}
            height={50}
            className="w-20 sm:w-24 md:w-28 lg:w-32"
          />
          <div className="w-6"></div>
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center pt-16 pb-12 px-4">
        <div className="max-w-2xl w-full">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h1 className="text-6xl font-bold text-[#4a58b5] mb-4">Payment Successful</h1>
            <h2 className="text-2xl font-semibold text-[#4a58b5] mb-6">{paymentStatus}</h2>
            <p className="text-[#4a58b5] mb-8">
              Your payment was successfully processed. You can now start your conversation with the tutor!
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <div className="text-center">
              <button
                onClick={handleStartChat}
                className="inline-block bg-[#fabb84] text-white px-6 py-2 rounded-lg font-semibold hover:bg-[#fc6453] transition-colors duration-200"
              >
                Start Chat
              </button>
            </div>
          </motion.div>
        </div>
      </main>

      <footer className="bg-[#4a58b5] text-white py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">&copy; 2024 Teach . Honour . Excel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default PaymentSuccess;
