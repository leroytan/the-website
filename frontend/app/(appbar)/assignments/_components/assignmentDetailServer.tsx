import { BASE_URL } from "@/utils/constants";
import { AssignmentDetailClient } from "./assignmentDetailClient";
import { TuitionListing } from "@/components/types";
import { cookies } from "next/headers";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatch";

// Server Component: fetches assignment detail by ID
export async function AssignmentDetailServer({ id }: { id: string }) {
  // Get cookies from the request context (if needed for auth)
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  // Fetch assignment detail from API
  const res = await fetchWithTokenCheck(`${BASE_URL}/assignments/${id}`, {
    cache: "no-store", // Disable caching to always get fresh data
    headers: {
      Cookie: accessToken ? `access_token=${accessToken}` : "",
    },
  });
  const assignment: TuitionListing = await res.json();
  // Render the client component with fetched data
  return <AssignmentDetailClient assignment={assignment} />;
}
