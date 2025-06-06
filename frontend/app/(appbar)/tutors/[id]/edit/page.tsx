import { BASE_URL } from "@/utils/constants";

import { Tutor } from "@/components/types";
import EditProfileForm from "./editProfileForm";


export const dynamic = "force-dynamic";

export default async function EditPage({ params}: {params: Promise<{ id: string }>}) {
  const { id } = await params;
  // Fetch current tutor data to prefill the edit form
  const res = await fetch(`${BASE_URL}/tutors/${id}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error("Failed to load tutor data");
  }
  const tutor: Tutor = await res.json();
  return <EditProfileForm tutor={tutor} />;
}
