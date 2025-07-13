"use client";

import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import Input from "@/components/input";
import MultiSelectButton from "@/components/multiSelectButton";
import { CloudUpload, Save, User, X } from "lucide-react";
import { useRef, useState } from "react";
import Image from "next/image";
import { useError } from "@/context/errorContext";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";
import MultiRangeSlider from "@/components/RangeSlider/multiRangeSlider";
import ProfilePictureUploader from "@/components/ProfilePictureUploader";
import { useAuth } from "@/context/authContext";

type TutorProfileFormData = {
  bio: string;
  education: string;
  availability: string;
  resumeUrl: string;
  experience: string;
  locations: string;
  subjects: string[];
  levels: string[];
  skills: string;
  min_rate: number;
  max_rate: number;
};

function TutorProfileForm({ nextStep, cancel }: { nextStep: () => void, cancel: () => void }) {
  const { setError } = useError();
  const router = useRouter();
  const { refetch } = useAuth();
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const oldAvatarUrl = useRef<string>("");
  const [formData, setFormData] = useState<TutorProfileFormData>({
    bio: "",
    education: "",
    availability: "",
    resumeUrl: "",
    experience: "",
    locations: "",
    subjects: [],
    levels: [],
    skills: "",
    min_rate: 10,
    max_rate: 100,
  });
  const [modalOpen, setModalOpen] = useState(false);
  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleMultiSelect = (
    field: "subjects" | "levels",
    selected: string[]
  ) => {
    setFormData((prev) => ({ ...prev, [field]: selected }));
  };

  const handleSubmit = async () => {
    if (
      !formData.bio.trim() ||
      !formData.education ||
      !formData.availability.trim() ||
      !formData.experience ||
      !formData.locations.trim() ||
      formData.subjects.length === 0 ||
      formData.levels.length === 0
    ) {
      setError("Please fill in all required fields.");
      return;
    }
    const payload = {
      photo_url: avatarUrl, //remove later
      highest_education: formData.education,
      availability: formData.availability,
      resume_url: formData.resumeUrl,
      min_rate: formData.min_rate,
      max_rate: formData.max_rate,
      location: formData.locations,
      about_me: formData.bio,
      experience: formData.experience,
      subjects_teachable: formData.subjects,
      levels_teachable: formData.levels,
      special_skills: formData.skills
        ? formData.skills
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean)
        : [],
      rating: 0, //remove later
    };
    try {
      const response = await fetchWithTokenCheck(`/api/tutors/new`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const res = await response.json();
        throw new Error(res.message || "Failed to save profile");
      }
      await refetch();
      nextStep(); // Proceed to the next step in the onboarding process
      // Optionally redirect or update UI here
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  const handleCancel = async () => {
    try {
      // Update backend to indicate user no longer intends to be a tutor
      const response = await fetchWithTokenCheck(`/api/me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          intends_to_be_tutor: false
        })
      });

      if (!response.ok) {
        throw new Error("Failed to update user status");
      }
    } catch (error) {
      console.error("Error updating user status:", error);
    } finally {
      cancel();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-3xl shadow-md py-10 px-28 w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <h1 className="col-span-full text-3xl font-bold text-customDarkBlue mb-4">
          Create a Tutor Profile
        </h1>

        <ProfilePictureUploader/>
        <div className="flex flex-col gap-2">
          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>About me</span>
          </label>
          <textarea
            name="bio"
            placeholder="Tell clients more about yourself"
            className="border rounded-md p-4 w-full h-32 text-gray-700 px-3 py-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
            value={formData.bio}
            onChange={handleChange}
          />
        </div>

        <div className="flex flex-col gap-2">
          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Highest Education</span>
          </label>
          <DropDown
            placeholder="- Select One -"
            stringOnDisplay={formData.education}
            stateController={function (value: any): void {
              setFormData((prev) => ({ ...prev, education: value }));
            }}
            iterable={["Secondary", "Polytechnic", "JC", "University"]}
          />

          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Availability</span>
            <br />
            <span className="text-xs text-gray-500">
              (Provide a clear and concise schedule)
            </span>
          </label>
          <Input
            name="availability"
            placeholder="e.g. Monday 1500-1900, Tuesday all day"
            value={formData.availability}
            onChange={handleChange}
            type={"text"}
          />

          <label className="font-semibold text-customDarkBlue">
            Resume URL
          </label>
          <Input
            name="resumeUrl"
            type="url"
            value={formData.resumeUrl}
            onChange={handleChange}
            placeholder={""}
          />

          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Teaching/Tuition Experience</span>
          </label>
          <DropDown
            placeholder="- Select One -"
            stringOnDisplay={formData.experience}
            stateController={function (value: any): void {
              setFormData((prev) => ({ ...prev, experience: value }));
            }}
            iterable={["0-1", "2-3", "4-5", "5-6", "7+"]}
          />

          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Locations</span>
          </label>
          <Input
            name="locations"
            type="text"
            placeholder="e.g. Bukit Batok, Jurong East"
            value={formData.locations}
            onChange={handleChange}
          />
        </div>

        <div className="flex flex-col gap-2">
          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Subjects Teachable</span>
          </label>
          <MultiSelectButton
            placeholder="- Select Multiple -"
            options={[
              "English",
              "Math",
              "Science",
              "Chinese",
              "Malay",
              "Tamil",
            ]}
            selected={formData.subjects}
            onChange={(selected) => handleMultiSelect("subjects", selected)}
          ></MultiSelectButton>

          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Levels Teachable</span>
          </label>
          <MultiSelectButton
            placeholder="- Select Multiple -"
            options={[
              "Primary 1",
              "Primary 2",
              "Primary 3",
              "Primary 4",
              "Primary 5",
              "Primary 6",
            ]}
            selected={formData.levels}
            onChange={(selected) => handleMultiSelect("levels", selected)}
          ></MultiSelectButton>

          <label className="font-semibold text-customDarkBlue">
            Special Skills
          </label>
          <Input
            name="skills"
            type="text"
            placeholder="e.g. Piano, Guitar, Coding"
            value={formData.skills}
            onChange={handleChange}
          />

          <label className="font-semibold text-customDarkBlue">
            <span className="text-red-500">* </span>
            <span>Hourly Rate Range</span>
          </label>
          <div className="relative w-full">
          <MultiRangeSlider
            min={10}
            max={100}
            onChange={(output) => {
              setFormData((prev) => ({
                ...prev,
                min_rate: output.min,
                max_rate: output.max
              }));
            }}
            formatter={(x) => `$${x}/hr`}
          />
          </div>
        </div>

        <div className="col-span-full flex justify-end gap-4">
          <Button
            className="px-4 py-2 bg-gray-400 text-white rounded-md hover:bg-customOrange transition-colors duration-200 flex items-center"
            onClick={handleCancel}
          >
            <X className="w-5 h-5 mr-1" />
            <span>I do not wish to be a tutor</span>
          </Button>
          <Button
            className="px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200 flex items-center"
            onClick={handleSubmit}
          >
            <Save className="w-5 h-5 mr-1" />
            <span>Save</span>
          </Button>
        </div>
      </form>
    </motion.div>
  );
}

export default TutorProfileForm;
