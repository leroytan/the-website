"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import TutorProfileForm from "./tutorProfileForm"; // Import the TutorProfileForm component
import { Button } from "@/components/button";

export default function TutorOnboarding() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      document.cookie =
        "tutor_profile_complete=false; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax; Secure";
      document.cookie =
        "intends_to_be_tutor=false; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax; Secure";
      router.push("/dashboard");
      router.refresh();
    }
  };
  const steps = [
    {
      content: (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl shadow-md p-6 w-[900px]"
        >
          <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">
            Welcome to Your Tutoring Journey!
          </h2>
          <p>
            We’re thrilled to have you join our team of tutors! <br />
            Before that, we need you to fill up some basic info about yourself.{" "}
            <br />
            This will take just 5 minutes.
          </p>
          <Button
            onClick={nextStep}
            className="mt-4 px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200 flex items-center"
          >
            Next
          </Button>
        </motion.div>
      ),
    },
    {
      content: <TutorProfileForm nextStep={nextStep} />,
    },
    {
      content: (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl shadow-md p-6 w-[900px]"
        >
          <h2 className="text-2xl font-bold text-[#4a58b5] mb-4">
            Get Ready to Teach!
          </h2>
          <p>You're all set! Start connecting with your students.</p>
            <Button
              className="mt-4 px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200 flex items-center"
              onClick={nextStep}
            >
              Go to Dashboard
            </Button>
        </motion.div>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-customLightYellow flex justify-center items-center">
      {steps[currentStep].content}
    </div>
  );
}
