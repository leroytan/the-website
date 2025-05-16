import { TuitionListing, TuitionListingFilters } from "@/components/types";
import AssignmentListing from "./assignmentlisting";
import { BASE_URL } from "@/utils/constants";
import { cookies } from "next/headers";
interface fetchedResponse {
  results: TuitionListing[];
  filters: TuitionListingFilters;
}
export default async function TuitionListings() {
  let tuitionListings: fetchedResponse;

  try {
    const apiUrl = `${BASE_URL}/assignments`;

    const cookieStore = await cookies();
    const data = await fetch(apiUrl, {
      headers: { Cookie: cookieStore.toString() },
    });

    if (!data.ok) {
      throw new Error(`Failed to fetch assignments: ${data.statusText}`);
    }

    const response = await data.json();
    tuitionListings = response as fetchedResponse;
  } catch (error) {
    console.error("Error fetching assignments:", error);
    return <div>Error loading assignments.</div>;
  }

  return (
    <AssignmentListing
      assignmentsArray={tuitionListings.results}
      assignmentsFilter={tuitionListings.filters}
    />
  );
}
