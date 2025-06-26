import { Suspense } from "react";
import { AssignmentList } from "./_components/assignmentList";
import { AssignmentDetailServer } from "./_components/assignmentDetailServer";
import {
  AssignmentDetailSkeleton,
} from "./_components/skeletons";
import { FilterSortBar } from "./_components/filterSort";
import { BASE_URL } from "@/utils/constants";
import { TuitionListing, TuitionListingFilters } from "@/components/types";
import AddAssignmentOverlay from "./_components/addAssignmentOverlay";
import BackButton from "./_components/BackButton";

interface AssignmentsResponse {
  results: TuitionListing[];
  num_pages: number;
  filters: TuitionListingFilters;
  sorts: { id: string; name: string }[];
}

export default async function AssignmentsPage({
  searchParams,
}: {
  searchParams: Promise<{
    page_number?: string;
    page_size?: string;
    query?: string;
    filter_by?: string;
    sort_by?: string;

    selected?: string;
    add?: string;
  }>;
}) {
  const searchParamsObj = await searchParams;

  // Parse search parameters for current state
  const pageNumberParam = searchParamsObj.page_number
    ? parseInt(searchParamsObj.page_number)
    : 1;
  const selectedId = searchParamsObj.selected;
  const queryParam = searchParamsObj.query || ""; // Parse the query parameter
  const filterParams = searchParamsObj.filter_by || ""; // Parse the filters parameter

  // Parse filters into an array
  const filterIds = filterParams.split(",").filter(Boolean);

  //Show add assignment overlay if 'add' param is true
  const showAddOverlay = searchParamsObj.add === "true";

  // Build query string for API request (excluding 'selected')
  const params = new URLSearchParams();

  const sortParam = Array.isArray(searchParamsObj.sort_by)
    ? searchParamsObj.sort_by[0]
    : searchParamsObj.sort_by;

  if (queryParam) {
    params.set("query", queryParam);
  }
  if (filterIds.length > 0) {
    params.set("filter_by", filterIds.join(","));
  }
  if (sortParam) {
    params.set("sort_by", sortParam);
  }
  params.set("page_number", pageNumberParam.toString() || "1");
  params.set("page_size", "10"); // Default page size
  // Fetch assignments list data from backend API
  const res = await fetch(`${BASE_URL}/assignments?${params.toString()}`, {
    cache: "no-store",
  });
  const data: AssignmentsResponse = await res.json();

  // Pass filters and sort options to the FilterSortBar
  // Adjust destructuring to match TuitionListingFilters properties
  const subjects = data.filters?.subjects ?? [];
  const levels = data.filters?.levels ?? [];
  const locations = data.filters?.locations ?? [];
  const sortOptions = (data.sorts ?? []).map((option) => ({
    value: option.id,
    label: option.name,
  }));
  const totalPages = data.num_pages;

  return (
    <div className="flex flex-col items-center bg-customLightYellow/50 h-[calc(100vh-56px)]">
      {/* Show on all screens if no detail is selected, or only on md+ if detail is selected */}
      {!selectedId ? (
        <FilterSortBar
          subjects={subjects}
          levels={levels}
          locations={locations}
          sortOptions={sortOptions}
        />
      ) : (
        <div className="hidden md:block w-full">
          <FilterSortBar
            subjects={subjects}
            levels={levels}
            locations={locations}
            sortOptions={sortOptions}
          />
        </div>
      )}
      <div className="flex flex-col md:flex-row bg-white rounded-xl shadow-lg w-full max-w-7xl h-full overflow-hidden">
        {/* Left Panel */}
        <div
          className={`md:w-1/2 h-full overflow-y-auto ${
            selectedId ? "hidden md:block" : "block"
          }`}
        >
          <AssignmentList
            searchParams={await searchParamsObj}
            assignments={data.results}
            totalPages={totalPages}
          />
        </div>

        {/* Right Panel */}
        {selectedId && (
          <div className="md:block md:w-1/2 w-full h-full bg-white p-6 overflow-y-auto border-t md:border-t-0 md:border-l">
            <Suspense fallback={<AssignmentDetailSkeleton />}>
              <div className="flex items-center mb-4 md:hidden">
                <BackButton />
              </div>
              <AssignmentDetailServer id={selectedId} />
            </Suspense>
          </div>
        )}
        {!selectedId && (
          <div className="hidden md:flex md:w-1/2 w-full h-full bg-white p-6 items-center justify-center">
            <p className="text-gray-500">
              Select an assignment to view details
            </p>
          </div>
        )}
      </div>
      {showAddOverlay && <AddAssignmentOverlay filters={data.filters} />}
    </div>
  );
}
