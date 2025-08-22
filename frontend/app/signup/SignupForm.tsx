"use client";
import "@/app/globals.css";
import DropDown from "@/components/dropdown";
import { BASE_URL } from "@/utils/constants";
import { motion } from "framer-motion";
import { Eye, EyeOff, MapPinCheckInside, Square, SquareCheck } from "lucide-react";
import { Inter } from "next/font/google";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { useAuth } from "@/context/authContext";
import ErrorMessage from "@/components/ErrorMessage";

import { FcGoogle } from "react-icons/fc";
import { Check } from "lucide-react";
import TermsDialog from "@/components/TermsDialog/TermsDialog";
import DataProtectionDialog from "@/components/DataProtectionDialog/DataProtectionDialog";
import { Button } from "@/components/button";

const inter = Inter({ subsets: ["latin"] });

const ROLES = ["Tutor", "Tutee/Parent"] as const;
const GENDERS = ["Male", "Female", "Other", "Prefer not to say"] as const;

export default function SignupPage() {
  const router = useRouter();
  const { refetch } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState(""); // New state for password confirmation
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [userType, setUserType] = useState("");
  const [gender, setGender] = useState("");

  const [errorMessage, setErrorMessage] = useState("");
  const [dialogMessage, setDialogMessage] = useState("");
  const [showDialog, setShowDialog] = useState(false);

  // Terms and Conditions dialog state
  const [tncAgreed, setTncAgreed] = useState(false);
  const [tncDialogOpen, setTncDialogOpen] = useState(false);
  // Data Protection Policy dialog state
  const [dpDialogOpen, setDpDialogOpen] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    //check payload
    if (!tncAgreed) {
      setErrorMessage("You must agree to the Terms and Conditions to sign up.");
      return;
    }
    if (!userType) {
      setErrorMessage("Please select a user type.");
      return;
    }
    if (!name || !email || !password || !confirmPassword) {
      setErrorMessage("Please fill in all fields.");
      return;
    }
    if (!gender) {
      setErrorMessage("Please select your gender.");
      return;
    }
    if (password !== confirmPassword) {
      return;
    }
    const res = await fetch(`/api/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email,
        password,
        intends_to_be_tutor: userType === "Tutor",
        gender: gender.toLowerCase().replace(" ", "_"),
      }),
    });

    if (res.status === 400) {
      setErrorMessage("User with the same email already exists.");
      return;
    }
    if (res.ok) {
      const resData = await res.json();
      // Check for different success scenarios
      if (
        resData.status === "waitlisted" ||
        resData.status === "pending_verification"
      ) {
        setDialogMessage(resData.message);
        setShowDialog(true);
      } else {
        // User is verified (example.com), proceed as before
        if (userType === "Tutor") {
          document.cookie = `intends_to_be_tutor=${
            userType === "Tutor"
          }; path=/; SameSite=Lax; Secure`;
          document.cookie = `tutor_profile_complete=${false}; path=/; SameSite=Lax; Secure`;
        }
        await refetch(); // refresh user and tutor data for authcontext
        router.push("/login");
      }
      router.refresh();
    } else {
      const resData = await res.json();
      setErrorMessage(resData.message || "Sign up failed");
    }
  };

  return (
    <div
      className={`min-h-screen bg-[#fff2de] flex flex-col items-center justify-center px-4 py-8 ${inter.className}`}
    >
      {/* Custom Dialog for waitlisted/pending_verification */}
      {showDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-sm w-full flex flex-col items-center">
            <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">
              Notice
            </h3>
            <p className="text-gray-700 mb-4 text-center">{dialogMessage}</p>
            <button
              className="px-4 py-2 bg-[#fabb84] text-white rounded-full hover:bg-[#fc6453] transition-colors duration-200"
              onClick={() => {
                setShowDialog(false);
                router.push("/login");
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-6 sm:p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <div className="flex justify-center mb-6">
          <Image
            src="/images/logo.png"
            alt="T.H.E. Logo"
            width={150}
            height={75}
            className="w-32 sm:w-40"
          />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-[#4a58b5] text-center">
          Sign Up for T.H.E.
        </h2>
        <form onSubmit={handleSubmit}>
          <DropDown
            placeholder="Sign up as a..."
            stringOnDisplay={userType}
            stateController={setUserType}
            iterable={[...ROLES]}
            className="mb-4"
          />
          <div className="mb-4">
            <label
              htmlFor="name"
              className="block text-sm font-medium text-[#4a58b5] mb-1"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
              required
              aria-required="true"
            />
          </div>
          <DropDown
            placeholder="Select your gender..."
            stringOnDisplay={gender}
            stateController={setGender}
            iterable={[...GENDERS]}
            className="mb-4"
          />
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-[#4a58b5] mb-1"
            >
              {userType === "Tutor" ? "University Email" : "Email"}
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
                onChange={(e) => {
                  setPassword(e.target.value);
                }}
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

          <div className="mb-6">
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium text-[#4a58b5] mb-1"
            >
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
                required
                aria-required="true"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                aria-label={
                  showConfirmPassword ? "Hide password" : "Show password"
                }
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-500" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>
            {password !== confirmPassword && confirmPassword && (
              <p className="text-sm text-red-500 mt-2">
                Passwords do not match
              </p>
            )}
          </div>
          {/* Terms and Conditions notice and dialog */}
          <div className="mb-6">
            <div className="flex items-center mt-2">
              <button
                type="button"
                className="flex items-center gap-2 text-sm focus:outline-none"
                onClick={() => setTncDialogOpen(true)}
                tabIndex={0}
              >
                  {tncAgreed ? (
                    <SquareCheck className="text-green-700 w-5 h-5" />
                  ) : (
                    <Square className="text-customYellow w-5 h-5" />
                  )}
                <span className={tncAgreed ? "text-green-700" : "text-[#4a58b5] hover:text-[#fc6453] underline"}>
                  {tncAgreed ? "You have agreed to the Terms and Conditions" : "Agree to the Terms and Conditions"}
                </span>
              </button>
            </div>
            <TermsDialog
              open={tncDialogOpen}
              onClose={() => setTncDialogOpen(false)}
              onAgree={() => setTncAgreed(true)}
              agreed={tncAgreed}
              requireAgree={true}
            />
          </div>
          {errorMessage && <ErrorMessage message={errorMessage} />}

          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200"
          >
            Sign Up
          </motion.button>
        </form>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-2 text-gray-500">
              Or continue with
            </span>
          </div>
        </div>

        <motion.button
          type="button"
          onClick={() => {
            window.location.href = `${BASE_URL}/auth/google/login`;
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-full flex items-center justify-center bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors duration-200 shadow-sm"
        >
          <FcGoogle className="mr-2 h-5 w-5" />
          Sign up with Google
        </motion.button>

        <p className="mt-4 text-center text-sm text-[#4a58b5]">
          Already have an account?{" "}
          <Link href="/login" className="text-[#fc6453] hover:underline">
            Log in
          </Link>
        </p>
      </motion.div>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-8 text-center text-xs text-[#4a58b5]"
      >
        &copy; {new Date().getFullYear()} Teach . Honour . Excel. All rights
        reserved.
      </motion.p>
    </div>
  );
}
