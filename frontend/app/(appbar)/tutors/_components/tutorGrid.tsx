"use client";
import { Tutor } from "@/components/types";
import { UserImage } from "@/components/userImage";
import { motion } from "framer-motion";
import { Book, GraduationCap, DollarSign, Star } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export function TutorGrid({ tutors }: { tutors: Tutor[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-center">
      {tutors.map((tutor) => (
        <motion.div
          key={tutor.id}
          layout="position"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          exit={{ opacity: 0 }}
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 flex flex-col h-full"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="flex-[30%]">
              <UserImage user={tutor}/>
            </div>
            <div className="flex-[70%]">
              <h3 className="text-xl font-semibold text-[#4a58b5]">
                {tutor.name}
              </h3>
              {/*<div className="flex items-center text-[#fabb84]">
                <Star size={16} className="mr-1" fill="#fabb84" />
                <span className="font-medium">{tutor.rating}</span>
              </div>*/}
            </div>
          </div>
          <div className="mb-4 space-y-2 flex-grow">
            <div className="flex items-center text-[#4a58b5]">
              <Book size={16} className="mr-2 text-[#fc6453]" />
              <span>{tutor.subjects_teachable.length > 0 ? tutor.subjects_teachable.join(", ") : "N/A"}</span>
            </div>
            <div className="flex items-center text-[#4a58b5]">
              <GraduationCap size={16} className="mr-2 text-[#fc6453]" />
              <span>{tutor.levels_teachable.join(", ")}</span>
            </div>
            <div className="flex items-center text-[#4a58b5]">
              <DollarSign size={16} className="mr-2 text-[#fc6453]" />
              <span>
                {tutor.min_rate && tutor.max_rate
                  ? `$${tutor.min_rate} - $${tutor.max_rate} per hour`
                  : "N/A"}
              </span>
            </div>
            <div className="flex items-center text-[#4a58b5]">
              <span className="font-medium mr-2">Experience:</span>
              <span>{tutor.experience} years</span>
            </div>
            <div className="flex items-center text-[#4a58b5]">
              <span className="font-medium mr-2">Availability:</span>
              <span>{tutor.availability}</span>
            </div>
          </div>
          <Link
            href={`/tutors/${tutor.id}`}
            className="mt-auto"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="w-full bg-[#fabb84] text-white py-2 px-4 rounded-md hover:bg-[#fc6453] transition-colors duration-200 font-medium"
            >
              View Profile
            </motion.button>
          </Link>
        </motion.div>
      ))}
    </div>
  );
}