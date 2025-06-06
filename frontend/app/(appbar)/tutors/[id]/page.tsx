import { BASE_URL } from "@/utils/constants";
import TutorProfile from "./tutorProfile";

// Force dynamic fetch to always get fresh data (no caching)
export const dynamic = "force-dynamic";

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  // Fetch tutor data from the API (assuming it returns JSON)
  const res = await fetch(`${BASE_URL}/tutors/${id}`, {
    cache: "no-store", // Ensure no caching for fresh data
  });
  if (!res.ok) {
    // Handle error or not-found (could throw to trigger not-found page)
    throw new Error("Failed to load tutor data");
  }
  const tutor = await res.json();
  console.log("Fetched tutor data:", tutor);
  return <TutorProfile tutor={tutor} />;
}
