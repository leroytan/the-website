"use client";
import { motion } from "framer-motion";
import {
  Award,
  BookOpen,
  Clock,
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
import { Button } from "@/components/button";
import { Tutor } from "@/components/types";

export default function TutorProfile({ tutor }: { tutor: Tutor }) {
  const { user, tutor: loggedinTutor } = useAuth();
  const isOwnProfile = user && loggedinTutor?.id === tutor.id;
  const [selectedTab, setSelectedTab] = useState("tutor information");
  const [message, setMessage] = useState("");
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Message sent:", message);
    setMessage("");
  };

  return (
    <motion.div className="min-h-screen bg-customLightYellow/50 px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center gap-6 relative">
        <div className="absolute top-4 right-4">
          {isOwnProfile && (
            <Link href={`/tutors/${tutor.id}/edit`}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center text-[#fabb84] hover:text-[#fc6453]"
              >
                <Pencil size={20} className="mr-2" />
                <span>Edit Profile</span>
              </motion.div>
            </Link>
          )}
        </div>
        <div>
          <Image
            src={tutor.photo_url || "/placeholder.svg"}
            alt={tutor.name}
            width={140}
            height={140}
            className="rounded-full border-4 border-[#fabb84]"
          />
        </div>

        <div className="flex flex-col justify-center">
          <h2 className="text-lg sm:text-2xl font-semibold mt-3 text-customDarkBlue flex flex-row items-center break-words">
            <div className="mr-2">{tutor.name}</div>
            <div className="text-orange-500 text-sm px-2 py-1 bg-orange-100 rounded-md flex flex-row justify-center items-center">
              <GraduationCap className="w-5 h-5 mr-1" />
              Tutor
            </div>
          </h2>
          <p className="text-gray-600 text-sm sm:text-base break-words">
            Subjects: {tutor.subjects_teachable?.join(", ") || "N/A"}
          </p>
          <div className="flex flex-wrap items-center space-x-3 mt-2">
            <div className="flex items-center mr-4">
              <Star className="w-5 h-5 mr-1" fill="#fabb84" color="#fabb84" />
              <span className="font-semibold text-customDarkBlue mr-1">
                {tutor.rating?.toFixed(1) || "N/A"}
              </span>
              <span className="text-customDarkBlue">(0 reviews)</span>
            </div>
            <div className="flex items-center mr-4">
              <Users className="w-5 h-5 mr-1" fill="#fabb84" color="#fabb84" />
              <span className="text-customDarkBlue font-semibold mr-1">--</span>
              <span className="text-customDarkBlue">students</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 flex flex-col sm:flex-row gap-6 sm:gap-8">
        <div className="w-full sm:w-1/4 bg-white shadow-lg rounded-xl p-4 sm:p-6">
          <Quote className="w-5 h-5 mr-2 text-[#fabb84]" />
          <h3 className="text-orange-500 font-semibold text-lg">About Me</h3>
          <p className="text-customDarkBlue mt-3 whitespace-pre-line">
            {tutor.about_me || "No description provided."}
          </p>
        </div>

        <div className="w-full sm:w-3/4 bg-white shadow-lg rounded-xl p-4 sm:p-6 max-w-full break-words">
          <div className="flex flex-wrap justify-center sm:justify-start space-x-3 sm:space-x-6 border-b border-gray-200 pb-2 mb-4">
            {["Tutor Information", ...(user ? ["Message"] : [])].map((tab) => (
              <div key={tab} className="flex items-center gap-4">
                <Button
                  className={`pb-2 text-gray-700 ${
                    selectedTab === tab.toLowerCase()
                      ? "border-b-2 border-orange-500 text-orange-500 font-semibold"
                      : ""
                  }`}
                  onClick={() => setSelectedTab(tab.toLowerCase())}
                >
                  {tab}
                </Button>
                {!user && (
                  <Button
                    disabled
                    className={`pb-2 text-gray-700 hover:cursor-not-allowed`}
                    onClick={() => {}}
                  >
                    Message (Log in to message)
                  </Button>
                )}
              </div>
            ))}
          </div>

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
                        Highest Education
                      </h3>
                    </div>
                    <p className="text-gray-900">
                      {tutor.highest_education || "N/A"}
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
                      {tutor.subjects_teachable?.join(", ") || "N/A"}
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
                      {tutor.levels_teachable?.join(", ") || "N/A"}
                    </p>
                  </div>
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <DollarSign className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Rate</h3>
                    </div>
                    <p className="text-gray-900">{tutor.rate || "N/A"}</p>
                  </div>
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <Award className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Special Skills</h3>
                    </div>
                    <p className="text-gray-900">
                      {tutor.special_skills?.join(", ") || "N/A"}
                    </p>
                  </div>
                  {/* New Field: Experience */}
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <Star className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Experience</h3>
                    </div>
                    <p className="text-gray-900">{tutor.experience || "N/A"}</p>
                  </div>
                  {/* New Field: Availability */}
                  <div>
                    <div className="flex items-center text-customDarkBlue mb-2">
                      <Clock className="w-5 h-5 mr-2 text-customOrange" />
                      <h3 className="text-lg font-semibold">Availability</h3>
                    </div>
                    <p className="text-gray-900">
                      {tutor.availability || "N/A"}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}

            {selectedTab === "message" && (
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
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
