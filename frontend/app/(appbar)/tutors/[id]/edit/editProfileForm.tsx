"use client";
import ProfilePictureUploader from "../../../../../components/ProfilePictureUploader";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { motion } from "framer-motion";
import {
  Award,
  BookOpen,
  Clock,
  DollarSign,
  GraduationCap,
  Pencil,
  Quote,
  Save,
  School,
  Star,
} from "lucide-react";
import { Button } from "@/components/button";
import Input from "@/components/input";
import DropDown from "@/components/dropdown";
import MultiSelectButton from "@/components/multiSelectButton";
import { Tutor } from "@/components/types";
import TagInput from "@/components/tagInput";
import { fetchClient } from "@/utils/fetch/fetchClient";
import MultiRangeSlider from "@/components/RangeSlider/multiRangeSlider";
import { useAuth } from "@/context/authContext";
import { ErrorProvider } from "@/context/errorContext";

export default function EditTutorProfile({ tutor }: { tutor: Tutor }) {
  const router = useRouter();
  const { refetch } = useAuth();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    highest_education: tutor.highest_education || "",
    availability: tutor.availability || "",
    resume_url: tutor.resume_url || "",
    min_rate: tutor.min_rate ?? 0,
    max_rate: tutor.max_rate ?? 100,
    location: tutor.location || "",
    rating: tutor.rating || "",
    about_me: tutor.about_me || "",
    experience: tutor.experience || "",
    subjects_teachable: tutor.subjects_teachable || [],
    levels_teachable: tutor.levels_teachable || [],
    special_skills: tutor.special_skills || [],
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Extract only the required fields
    const payload = {
      highest_education: formData.highest_education,
      availability: formData.availability,
      resume_url: formData.resume_url,
      min_rate: formData.min_rate,
      max_rate: formData.max_rate,
      location: formData.location,
      rating: formData.rating,
      about_me: formData.about_me,
      experience: formData.experience,
      subjects_teachable: formData.subjects_teachable,
      levels_teachable: formData.levels_teachable,
      special_skills: formData.special_skills,
    };


    const res = await fetchClient(`/api/tutors/${tutor.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      refetch(); // Refresh user and tutor data in auth context
      router.push(`/tutors/${tutor.id}`);
    } else {
      alert("Failed to update profile");
    }
    setLoading(false);
  };

  return (
    <motion.div className="min-h-screen bg-customLightYellow/50 px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Top Profile Info */}
        <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center items-center gap-6 relative">
          <div className="absolute top-4 right-4">
            <div className="flex items-center text-customOrange border-2 rounded-lg p-2 border-customOrange">
              <span>Edit view</span>
            </div>
          </div>
          <ProfilePictureUploader photoUrl={tutor.photo_url} />
          <div className="flex flex-col justify-center text-center">
            <h2 className="text-lg sm:text-2xl font-semibold mt-3 text-customDarkBlue">
              {tutor.name}
            </h2>
          </div>
        </div>

        {/* Bottom Split: Left - About Me, Right - Tutor Info */}
        <div className="flex flex-col sm:flex-row gap-6 sm:gap-8">
          <div className="w-full sm:w-1/4 bg-white shadow-lg rounded-xl p-4 sm:p-6 relative">
            <Quote className="w-5 h-5 mb-2 text-customYellow rotate-180" />
            <h3 className="text-orange-500 font-semibold text-lg">About Me</h3>
            <textarea
              name="about_me"
              placeholder="Tell clients more about yourself"
              className="border rounded-md p-4 w-full h-32 text-gray-700 px-3 py-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-customYellow"
              value={formData.about_me}
              onChange={handleChange}
            />
            <Quote className="w-5 h-5 text-customYellow absolute bottom-4 right-4" />
          </div>

          <div className="w-full sm:w-3/4 bg-white shadow-lg rounded-xl p-4 sm:p-6">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <GraduationCap className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">
                    Highest Qualification
                  </h3>
                </div>
                <DropDown
                  placeholder="- Select One -"
                  stringOnDisplay={formData.highest_education}
                  stateController={(value) =>
                    setFormData((prev) => ({
                      ...prev,
                      highest_education: value,
                    }))
                  }
                  iterable={["Secondary", "Polytechnic", "JC", "University"]}
                />
              </div>
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <BookOpen className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">Subjects Teachable</h3>
                </div>
                <MultiSelectButton
                  options={[
                    "English",
                    "Math",
                    "Science",
                    "Chinese",
                    "Malay",
                    "Tamil",
                  ]}
                  selected={formData.subjects_teachable}
                  onChange={(selected) =>
                    setFormData((prev) => ({
                      ...prev,
                      subjects_teachable: selected,
                    }))
                  }
                />
              </div>
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <School className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">Levels Teachable</h3>
                </div>
                <MultiSelectButton
                  options={[
                    "Primary 1",
                    "Primary 2",
                    "Primary 3",
                    "Primary 4",
                    "Primary 5",
                    "Primary 6",
                  ]}
                  selected={formData.levels_teachable}
                  onChange={(selected) =>
                    setFormData((prev) => ({
                      ...prev,
                      levels_teachable: selected,
                    }))
                  }
                />
              </div>
              <div className="flex flex-col relative width-full height-full">
                <div className="flex items-center text-customDarkBlue mb-2">
                  <DollarSign className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">Hourly Rate</h3>
                </div>
                <div className="flex items-center justify-between pt-2 pb-4">
                  <MultiRangeSlider
                    min={0}
                    max={100}
                    from={formData.min_rate}
                    to={formData.max_rate}
                    onChange={({ min, max }) => {
                      setFormData((prev) => ({
                        ...prev,
                        min_rate: min,
                        max_rate: max,
                      }));
                    }}
                    formatter={(x) => `$${x}/hr`}
                  />
                </div>
              </div>
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <Award className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">Special Skills</h3>
                </div>
                <TagInput
                  tags={formData.special_skills}
                  setTags={(tags) =>
                    setFormData((prev) => ({
                      ...prev,
                      special_skills: tags,
                    }))
                  }
                />
              </div>
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <Star className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">
                    Teaching/Tuition Experience
                  </h3>
                </div>
                <DropDown
                  placeholder="- Select One -"
                  stringOnDisplay={formData.experience}
                  stateController={function (value: any): void {
                    setFormData((prev) => ({ ...prev, experience: value }));
                  }}
                  iterable={["0-1", "2-3", "4-5", "5-6", "7+"]}
                />
              </div>
              <div>
                <div className="flex items-center text-customDarkBlue mb-2">
                  <Clock className="w-5 h-5 mr-2 text-customOrange" />
                  <h3 className="text-lg font-semibold">Availability</h3>
                </div>
                <Input
                  name="availability"
                  placeholder="E.g., Tue/Thu evenings, Sat/Sun all day"
                  value={formData.availability}
                  onChange={handleChange}
                  type="text"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <Button
            type="submit"
            className="px-6 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors flex items-center justify-center whitespace-nowrap"
            loading={loading}
          >
            <Save size={20} className="mr-2" />
            Save Changes
          </Button>
        </div>
      </form>
    </motion.div>
  );
};
