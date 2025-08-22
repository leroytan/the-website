"use client";

import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Mail, GraduationCap, School, Save } from "lucide-react";
import ProfilePictureUploader from "@/components/ProfilePictureUploader";
import { fetchClient } from "@/utils/fetch/fetchClient";
import ToggleSwitch from "@/components/ToggleSwitch";

interface UserProfile {
  id: number;
  name: string;
  gender: string;
  email: string;
  profile_photo_url: string | undefined;
  intends_to_be_tutor: boolean;
  created_at: string;
  updated_at: string;
}

export default function TuteeProfileEditPage() {
  const { user, loading, refetch } = useAuth();
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [newImage, setNewImage] = useState<File | null>(null);

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push("/login?redirectTo=/profile/tutee/edit");
        return;
      }

      // Fetch user profile data
      const fetchProfile = async () => {
        try {
          const response = await fetchClient(`/api/me`);
          if (!response.ok) throw new Error("Failed to fetch profile");
          const data = await response.json();
          setProfile(data.user);
        } catch (error) {
          console.error("Error fetching profile:", error);
        }
      };

      fetchProfile();
    }
  }, [user, loading, router]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    if (profile) {
      setProfile((prev) => ({ ...prev!, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile) return;

    try {
      const formData = new FormData();
      if (newImage) {
        formData.append("file", newImage);
        const uploadResponse = await fetchClient(
          `/api/me/upload-profile-photo`,
          {
            method: "POST",
            body: formData,
            credentials: "include",
          }
        );
        if (!uploadResponse.ok) throw new Error("Failed to upload photo");
      }

      // Update profile data
      const response = await fetchClient(`/api/me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: profile.name,
          intends_to_be_tutor: profile.intends_to_be_tutor,
        }),
      });

      if (!response.ok) throw new Error("Failed to update profile");
      refetch(); // Refresh user data in auth context
      router.push("/profile/tutee");
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  if (loading || !profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-customLightYellow/50 px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center gap-6 relative">
        <div className="absolute top-4 right-4">
          <div className="flex items-center text-customOrange border-2 rounded-lg p-2 border-customOrange">
            <span>Edit view</span>
          </div>
        </div>
        <div className="relative">
          <ProfilePictureUploader
            photoUrl={profile.profile_photo_url}
            gender={profile.gender}
          />
        </div>

        <div className="flex-1">
          <input
            type="text"
            name="name"
            value={profile.name}
            onChange={handleChange}
            className="text-2xl font-semibold text-customDarkBlue w-full bg-transparent border-b-2 border-customDarkBlue focus:outline-none focus:border-customOrange mb-2"
          />
          <div className="space-y-2 mt-4">
            <div className="flex items-center text-customDarkBlue">
              <Mail className="w-5 h-5 mr-2 text-customOrange" />
              <span>{profile.email}</span>
            </div>
          </div>
          <div className="space-y-2 mt-4">
          <ToggleSwitch
          disabled={true}
            label="Gender"
            options={["Male", "Female"]}
            value={profile.gender}
            onChange={(value: string) =>
              setProfile((prev) => (prev ? { ...prev, gender: value } : prev))
            }
          />
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 bg-white shadow-lg rounded-xl p-6"></div>

        <div className="md:col-span-2 bg-white shadow-lg rounded-xl p-6">
          <h3 className="text-customDarkBlue font-semibold text-lg mb-4">
            Account Information
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center text-customDarkBlue mb-2">
                <School className="w-5 h-5 mr-2 text-customOrange" />
                <h4 className="font-semibold">Member Since</h4>
              </div>
              <p className="text-gray-600">
                {new Date(profile.created_at).toLocaleDateString()}
              </p>
            </div>
            <div>
              <div className="flex items-center text-customDarkBlue mb-2">
                <GraduationCap className="w-5 h-5 mr-2 text-customOrange" />
                <h4 className="font-semibold">Last Updated</h4>
              </div>
              <p className="text-gray-600">
                {new Date(profile.updated_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end mt-6">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSubmit}
          className="flex px-6 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors"
        >
          <Save size={20} className="mr-2" />
          Save Changes
        </motion.button>
      </div>
    </div>
  );
}
