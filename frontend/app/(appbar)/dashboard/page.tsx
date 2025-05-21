import { BASE_URL } from "@/utils/constants";
import { cookies } from "next/headers";
import { TuitionListing } from "@/components/types";
import ParentDashboardPage from "./_components/clientdashboard";
import TutorDashboardPage from "./_components/tutordashboard";

export default async function Page() {
  const cookieStore = await cookies();

  // Get user info

  let assignments = [];
  let role = "client";

  if (role === "client") {
    const res = await fetch(`${BASE_URL}/me/created-assignments`, {
      cache: "no-store",
      headers: { Cookie: cookieStore.toString() },
    });
    assignments = await res.json();
  } else if (role === "tutor") {
    const res = await fetch(`${BASE_URL}/me/applied-assignments`, {
      cache: "no-store",
      headers: { Cookie: cookieStore.toString() },
    });
    assignments = await res.json();
  }

  return role === "tutor" ? (
    <TutorDashboardPage assignments={assignments as TuitionListing[]} />
  ) : (
    <ParentDashboardPage assignments={assignments as TuitionListing[]} />
  );
}