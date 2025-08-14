"use client";
import "@/app/globals.css";
import { motion } from "framer-motion";
import { Eye, EyeOff } from "lucide-react";
import { Inter } from "next/font/google";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

import { useRouter } from "next/navigation";
import { BASE_URL } from "@/utils/constants";
import { useAuth } from "@/context/authContext";
import { User, Tutor } from "@/components/types";
import ErrorMessage from "@/components/ErrorMessage";
import logger from "@/utils/logger";

import { FcGoogle } from "react-icons/fc";

const inter = Inter({ subsets: ["latin"] });

export default function LoginForm({ redirectTo }: { redirectTo: string }) {
  const router = useRouter();
  const { refetch } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [errorMessage, setErrorMessage] = useState("");
  const [needsEmailVerification, setNeedsEmailVerification] = useState(false);

  // Helper function to ensure error message is always a string
  const setErrorMessageSafe = (message: any) => {
    if (typeof message === 'string') {
      setErrorMessage(message);
    } else if (message && typeof message === 'object' && message.message) {
      setErrorMessage(message.message);
    } else {
      setErrorMessage('An unexpected error occurred');
    }
  };

  const handleResendConfirmation = async () => {
    try {
      const res = await fetch(`/api/auth/resend-confirmation-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (res.ok) {
        setErrorMessageSafe("Confirmation email sent! Please check your inbox.");
        setNeedsEmailVerification(false);
      } else {
        setErrorMessageSafe("Failed to send confirmation email. Please try again.");
      }
    } catch (error) {
      setErrorMessageSafe("An error occurred. Please try again.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch(`/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (res.ok) {
      const { user, tutor }: { user: User | null; tutor: Tutor | null } = await refetch(); // refresh user and tutor data for authcontext

      logger.debug("Manual login refetch completed:", {
        user: user ? { id: user.id, name: user.name, email: user.email } : null,
        tutor: tutor ? { id: tutor.id } : null
      });

      // Set helper cookies for middleware
      if (user?.intends_to_be_tutor && !tutor) {
      document.cookie = `intends_to_be_tutor=${!!user.intends_to_be_tutor}; path=/; SameSite=Lax; Secure`;
      document.cookie = `tutor_profile_complete=${!!tutor}; path=/; SameSite=Lax; Secure`;
      }
      
      router.replace(redirectTo);
      // router.refresh();
    } else {
      const errorData = await res.json();
      
      // Handle email verification error specifically
      if (res.status === 403 && errorData.detail?.code === "EMAIL_NOT_VERIFIED") {
        setErrorMessageSafe(errorData.detail.message || "Please verify your email address before logging in.");
        setNeedsEmailVerification(true);
        return;
      }
      
      // Reset email verification state for other errors
      setNeedsEmailVerification(false);
      
      // Ensure we always set a string message
      setErrorMessageSafe(errorData.message || errorData.detail?.message || "Login failed");
    }
  };

  return (
    <div
      className={`min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 ${inter.className}`}
    >
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <div className="flex justify-center mb-6">
          <Image
            src="/images/logo.png"
            alt="THE Logo"
            width={150}
            height={75}
            className="w-32 sm:w-40"
          />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">
          Login to THE
        </h2>
        <form onSubmit={handleSubmit}>
          
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-[#4a58b5] mb-1"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
              aria-required="true"
            />
          </div>
          <div className="mb-6">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-[#4a58b5] mb-1"
            >
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                required
                aria-required="true"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-500" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>
          </div>
          {errorMessage && typeof errorMessage === 'string' && (
            <div className="mb-4">
              <ErrorMessage message={errorMessage} />
              {needsEmailVerification && (
                <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-800 mb-2">
                    Need a new confirmation link?
                  </p>
                  <button
                    type="button"
                    onClick={handleResendConfirmation}
                    className="text-sm text-blue-600 hover:underline"
                  >
                    Resend confirmation email
                  </button>
                </div>
              )}
            </div>
          )}
          <div className="flex justify-between items-center mb-4">
            <Link
              href="/login/forgot-password"
              className="text-sm text-[#4a58b5] hover:underline"
            >
              Forgot Password?
            </Link>
          </div>
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
          >
            Log In
          </motion.button>
        </form>

        <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
                <span className="bg-white px-2 text-gray-500">Or continue with</span>
            </div>
        </div>

        <motion.button
            type="button"
            onClick={() => { window.location.href = `${BASE_URL}/auth/google/login`; }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full flex items-center justify-center bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors duration-200 shadow-sm"
        >
            <FcGoogle className="mr-2 h-5 w-5" />
            Sign in with Google
        </motion.button>

        <p className="mt-4 text-center text-sm text-[#4a58b5]">
          Don't have an account?{" "}
          <Link href="/signup" className="text-[#fc6453] hover:underline">
            Sign up
          </Link>
        </p>
      </motion.div>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-8 text-center text-xs text-[#4a58b5]"
      >
        &copy; {new Date().getFullYear()} Teach . Honour . Excel. All rights reserved.
      </motion.p>
    </div>
  );
}
