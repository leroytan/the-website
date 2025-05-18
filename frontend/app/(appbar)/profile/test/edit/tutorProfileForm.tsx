"use client";

import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import Input from "@/components/input";
import MultiSelectButton from "@/components/multiSelectButton";
import Modal from "./_components/modal";
import { CloudUpload, Save } from "lucide-react";
import { useRef, useState } from "react";
import Image from "next/image";
import { useError } from "@/context/errorContext";
import { useRouter } from "next/navigation";

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
  rate: string;
};

function TutorProfileForm() {
  const { setError } = useError();
  const router = useRouter()
  const [avatarUrl, setAvatarUrl] = useState<string>("/default-avatar.png");
  const oldAvatarUrl = useRef<string>("/default-avatar.png");
  const updateAvatar = async (avatarDataUrl: string | null) => {
    if (!avatarDataUrl) return;

    // Store the current avatar before changing
    oldAvatarUrl.current = avatarUrl;
    setAvatarUrl(avatarDataUrl); // Show the new avatar immediately

    // Convert Data URL to Blob
    const res = await fetch(avatarDataUrl);
    const blob = await res.blob();

    // Prepare form data
    const formData = new FormData();
    formData.append("file", blob, "avatar.png");

    // Upload to your API
    try {
      const response = await fetch("/api/user/upload-profile-photo", {
        method: "POST",
        body: formData,
        credentials: "include",
      });
      if (!response.ok) throw new Error("Upload failed");
    } catch (err) {
      setError("Failed to upload avatar. Please try again later.");
      setAvatarUrl(oldAvatarUrl.current); // Revert to original on error
    }
  };
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
    rate: "",
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
    console.log("Submitting tutor profile:", formData);
    if (
      !formData.bio.trim() ||
      !formData.education ||
      !formData.availability.trim() ||
      !formData.experience ||
      !formData.locations.trim() ||
      formData.subjects.length === 0 ||
      formData.levels.length === 0 ||
      !formData.rate.trim()
    ) {
      setError("Please fill in all required fields.");
      return;
    }
    const payload = {
      photo_url: avatarUrl,
      highest_education: formData.education,
      availability: formData.availability,
      resume_url: formData.resumeUrl,
      rate: formData.rate,
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
      const response = await fetch("/api/tutors/new", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const res = await response.json();
        throw new Error(res.message || "Failed to save profile");
      }
      alert("Profile saved!");
      // Optionally redirect or update UI here
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF3E9] flex justify-center items-center p-6">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-3xl shadow-md p-10 w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <h1 className="col-span-full text-3xl font-bold text-customDarkBlue mb-4">
          Edit Tutor Profile
        </h1>

        <div className="flex flex-col items-center gap-2">
          <Image
            src={avatarUrl}
            alt="Avatar"
            width={200}
            height={200}
            className="rounded-full border-4 border-customYellow"
          />
          <Button
            className="bg-customYellow text-white px-4 py-2 rounded-full text-sm flex items-center gap-2 hover:bg-customOrange transition-colors duration-200"
            onClick={() => {
              setModalOpen(true);
            }}
          >
            <CloudUpload className="w-6 h-auto mr-1" />
            Upload Profile Pic
          </Button>
        </div>
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
            stringOnDisplay={formData.education || "- Select One -"}
            stateController={function (value: any): void {
              setFormData((prev) => ({ ...prev, education: value }));
            }}
            iterable={["Secondary", "Polytechnic", "JC", "University"]}
          />

          <label className="font-semibold text-customDarkBlue">
            <span className="text-customOrange">* </span>
            <span>Availability</span>
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
            <span>Experience</span>
          </label>
          <DropDown
            stringOnDisplay={formData.experience || "- Select One -"}
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
            <span>Rate</span>
          </label>
          <div className="flex items-center">
  <span className="px-3 py-2 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md text-gray-500">
    S$
  </span>
  <Input
    name="rate"
    type="text"
    placeholder=""
    value={formData.rate}
    onChange={handleChange}
    className="rounded-l-none rounded-r-none mx-0.5"
  />
  <span className="px-3 py-2 bg-gray-200 border border-l-0 border-gray-300 rounded-r-md text-gray-500">
    /hour
  </span>
</div>
        </div>

        <div className="col-span-full flex justify-end gap-4">
          <Button
            className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
            onClick={() => router.back()}
          >
            <span>Cancel</span>
          </Button>
          <Button
            className="px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200 flex items-center"
            onClick={handleSubmit}
          >
            <Save className="w-5 h-5 mr-1" />
            <span>Save changes</span>
          </Button>
        </div>
      </form>
      {modalOpen && (
        <Modal
          updateAvatar={updateAvatar}
          closeModal={() => setModalOpen(false)}
        />
      )}
    </div>
  );
}

export default TutorProfileForm;
