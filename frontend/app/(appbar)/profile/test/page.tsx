"use client";
import { motion } from "framer-motion";
import {
  Award,
  BookOpen,
  DollarSign,
  GraduationCap,
  Pencil,
  Quote,
  School,
  Star,
  Users,
} from "lucide-react";
import { useState } from "react";
import Image from "next/image";
import { useAuth } from "@/context/authContext";
import Link from "next/link";

const tutorProfile = {
  name: "Lexus Tan",
  role: "Tutor",
  subjects: ["Mathematics, English"],
  rating: 4.5,
  reviewsCount: 2,
  studentsCount: 42,
  profileImage: "/placeholder.svg?height=200&width=200",
  email: "lexus.tan@example.com",
  phone: "+1234567890",
  location: "Central Singapore",
  subjectsTeachable: "Mathematics, English",
  highestQualification: "Master's Degree",
  levelsTeachable: "Primary 1 to Primary 6",
  rate: "$25-$45 per hour depending on subject and level",
  specialSkills: "Problem-solving techniques, Visual learning methods",
  about: `
    Hi, I'm Lexus, a dedicated tutor with a passion for helping students excel in Math and English. I specialize in breaking complex concepts into simple, easy-to-understand lessons.
    
    **My Teaching Philosophy**
    I believe every student learns differently, and my approach is tailored to suit individual needs. Whether it's mastering algebra, improving essay writing, or building confidence in problem-solving, I focus on making learning engaging, structured, and results-driven.

    **What You Can Expect**
    - Clear explanations with step-by-step guidance
    - Interactive lessons to keep learning fun and effective
    - Personalized strategies for strengthening weak areas
    - Encouragement and support to build confidence
  `,
};

const reviews = [
  {
    id: 1,
    name: "Amanda Lim",
    rating: 5,
    timeAgo: "2 hours ago",
    text: "Lexus is a fantastic tutor! Always explains with patience and ensures I truly understand the topic. Highly recommend!",
    profileImage: "/placeholder.svg?height=40&width=40",
  },
  {
    id: 2,
    name: "Brandon Chua",
    rating: 4,
    timeAgo: "1 day ago",
    text: "Very structured lessons. Lexus gives clear examples and makes it fun to learn difficult topics.",
    profileImage: "/placeholder.svg?height=40&width=40",
  },
];

export default function TutorProfile() {
  const { isAuthenticated } = useAuth();
  const [selectedTab, setSelectedTab] = useState("tutor information");
  const [message, setMessage] = useState("");
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the message to your backend
    console.log("Message sent:", message);
    setMessage("");
  };

  return (
    <motion.div className="min-h-screen bg-customLightYellow px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      {/* Profile Section */}
      <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center gap-6 relative">
        <div className="absolute top-4 right-4">
          <Link href="/profile/test/edit">
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="flex items-center text-[#fabb84] hover:text-[#fc6453]"
      >
        <Pencil size={20} className="mr-2" />
        <span>Edit Profile</span>
      </motion.div>
    </Link>
        </div>
        <div>
          <Image
            src={tutorProfile.profileImage}
            alt={tutorProfile.name}
            width={140}
            height={140}
            className="rounded-full border-4 border-[#fabb84]"
          />
        </div>

        <div className="flex flex-col justify-center">
          <h2 className="text-lg sm:text-2xl font-semibold mt-3 text-customDarkBlue flex flex-row items-center break-words">
            <div className="mr-2">{tutorProfile.name} </div>
            <div className="text-orange-500 text-sm px-2 py-1 bg-orange-100 rounded-md flex flex-row justify-center items-center">
              <GraduationCap className="w-5 h-5 mr-1" />
              {tutorProfile.role}
            </div>
          </h2>
          <p className="text-gray-600 text-sm sm:text-base break-words">
            Subjects: {tutorProfile.subjects.join(", ")}
          </p>
          <div className="flex flex-wrap items-center space-x-3 mt-2">
            <div className="flex items-center mr-4">
              <Star className="w-5 h-5 mr-1" fill="#fabb84" color="#fabb84" />
              <span className="font-semibold text-customDarkBlue mr-1">
                {tutorProfile.rating.toFixed(1)}
              </span>
              <span className="text-customDarkBlue">
                ({tutorProfile.reviewsCount} reviews)
              </span>
            </div>
            <div className="flex items-center mr-4">
              <Users className="w-5 h-5 mr-1" fill="#fabb84" color="#fabb84" />
              <span className="text-customDarkBlue font-semibold mr-1">
                {tutorProfile.studentsCount}
              </span>
              <span className="text-customDarkBlue">students</span>
            </div>
          </div>
        </div>
      </div>

      {/* About and Navigation Section */}
      <div className="mt-6 flex flex-col sm:flex-row gap-6 sm:gap-8">
        <div className="w-full sm:w-1/4 bg-white shadow-lg rounded-xl p-4 sm:p-6">
          <Quote className="w-5 h-5 mr-2 text-[#fabb84]" />
          <h3 className="text-orange-500 font-semibold text-lg">About Me</h3>
          <p className="text-customDarkBlue mt-3 whitespace-pre-line">
            {tutorProfile.about}
          </p>
        </div>

        <div className="w-full sm:w-3/4 bg-white shadow-lg rounded-xl p-4 sm:p-6 max-w-full break-words">
          {/* Navigation Tabs */}
          <div className="flex flex-wrap justify-center sm:justify-start space-x-3 sm:space-x-6 border-b border-gray-200 pb-2 mb-4">
            {["Tutor Information", "Reviews", ...(isAuthenticated ? ["Message"] : [])].map((tab) => (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                key={tab}
                className={`pb-2 text-gray-700 ${
                  selectedTab === tab.toLowerCase()
                    ? "border-b-2 border-orange-500 text-orange-500 font-semibold"
                    : ""
                }`}
                onClick={() => setSelectedTab(tab.toLowerCase())}
              >
                {tab}
              </motion.button>
            ))}
          </div>

          {/* Dynamic Content Section */}
          <div className="bg-white rounded-xl p-4 sm:p-6 max-w-full break-words">
            {selectedTab === "tutor information" && (
              <motion.div
                className="space-y-8"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <div className="grid md:grid-cols-2 gap-8">
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <GraduationCap className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">
                        Highest Qualification
                      </h3>
                    </div>
                    <p className="text-gray-900">
                      {tutorProfile.highestQualification}
                    </p>
                  </div>
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <BookOpen className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">
                        Subjects Teachable
                      </h3>
                    </div>
                    <p className="text-gray-900">
                      {tutorProfile.subjectsTeachable}
                    </p>
                  </div>
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <School className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">
                        Levels Teachable
                      </h3>
                    </div>
                    <p className="text-gray-900">
                      {tutorProfile.levelsTeachable}
                    </p>
                  </div>
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <DollarSign className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Rate</h3>
                    </div>
                    <p className="text-gray-900">{tutorProfile.rate}</p>
                  </div>
                  <div>
                    <div className="flex items-center text-[#4a58b5] mb-2">
                      <Award className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Special Skills</h3>
                    </div>
                    <p className="text-gray-900">
                      {tutorProfile.specialSkills}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
            {selectedTab === "reviews" && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                {reviews.map((review) => (
                  <div key={review.id} className="flex gap-4 border-b py-3">
                    <Image
                      src={review.profileImage}
                      alt={review.name}
                      className="w-10 h-10 rounded-full"
                      width={40}
                      height={40}
                    />
                    <div>
                      <h4 className="text-gray-800 font-semibold">
                        {review.name}
                      </h4>
                      <p className="text-sm text-gray-500">{review.timeAgo}</p>
                      <p className="text-customYellow flex flex-row items-center">
                        {Array.from({ length: review.rating }, (_, i) => (
                          <Star
                            key={i}
                            className="w-4 h-4 mr-1"
                            fill="#fabb84"
                          />
                        ))}
                      </p>
                      <p className="text-customDarkBlue mt-1">{review.text}</p>
                    </div>
                  </div>
                ))}
              </motion.div>
            )}
            {selectedTab === "message" && (
              <div>
                <motion.form
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  onSubmit={handleSendMessage}
                  className="space-y-4"
                >
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message here..."
                    className="w-full p-2 border border-gray-300 rounded-md text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-[#fabb84] break-words"
                    rows={4}
                  />
                  <div className="flex justify-end space-x-2">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      type="button"
                      className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
                    >
                      Cancel
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      type="submit"
                      className="px-4 py-2 bg-[#fabb84] text-white rounded-md hover:bg-[#fc6453] transition-colors duration-200"
                    >
                      Send Message
                    </motion.button>
                  </div>
                </motion.form>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
