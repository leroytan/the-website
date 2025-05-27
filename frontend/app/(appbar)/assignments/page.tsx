import { Suspense } from "react";
import { AssignmentList } from "./_components/assignmentList";
import { AssignmentDetailServer } from "./_components/assignmentDetailServer";
import { ListSkeleton, DetailSkeleton } from "./_components/skeletons";
import { FilterSortBar } from "./_components/filterSort";
import { BASE_URL } from "@/utils/constants";
import { TuitionListing, TuitionListingFilters } from "@/components/types";
import AddAssignmentOverlay from "./_components/addAssignmentOverlay";

interface AssignmentsResponse {
  results: TuitionListing[];
  totalPages: number;
  filters: TuitionListingFilters
  sortOptions: { value: string; label: string }[];
}

export default async function AssignmentsPage({
  searchParams,
}: {
  searchParams: Promise<{
    page?: string | string[];
    selected?: string;
    subject?: string | string[];
    level?: string | string[];
    sort?: string | string[];
    add?: string;
  }>;
}) {
  const searchParamsObj = await searchParams;

  // Parse search parameters for current state
  const pageParam = Array.isArray(searchParamsObj.page)
    ? searchParamsObj.page[0]
    : searchParamsObj.page;
  const page = pageParam ? parseInt(pageParam) : 1;
  const selectedId = searchParamsObj.selected;

  //Show add assignment overlay if 'add' param is true
  const showAddOverlay = searchParamsObj.add === "true";
  
  // Build query string for API request (excluding 'selected')
  const params = new URLSearchParams();
  const subjectParams = searchParamsObj.subject;
  const levelParams = searchParamsObj.level;
  const sortParam = Array.isArray(searchParamsObj.sort)
    ? searchParamsObj.sort[0]
    : searchParamsObj.sort;

  if (subjectParams) {
    const subjects = Array.isArray(subjectParams)
      ? subjectParams
      : [subjectParams];
    subjects.forEach((subj) => params.append("subject", subj));
  }
  if (levelParams) {
    const levels = Array.isArray(levelParams) ? levelParams : [levelParams];
    levels.forEach((lvl) => params.append("level", lvl));
  }
  if (sortParam) {
    params.set("sort", sortParam);
  }
  params.set("page", pageParam || "1");

  // Fetch assignments list data from backend API
  const res = await fetch(`${BASE_URL}/assignments?${params.toString()}`, {
    cache: "no-store",
  });
  const data: AssignmentsResponse = await res.json();

  // Pass filters and sort options to the FilterSortBar
  // Adjust destructuring to match TuitionListingFilters properties
  const subjects = data.filters?.subjects ?? [];
  const levels = data.filters?.levels ?? [];
  const sortOptions = data.sortOptions || [
    { value: "recent", label: "Recently Posted" },
    { value: "asc", label: "Ascending" },
    { value: "desc", label: "Descending" },
  ];
  const totalPages = data.totalPages || 6;

  return (
    <div className="flex flex-col items-center bg-customLightYellow h-[calc(100vh-64px)]">
      <FilterSortBar
        subjects={subjects}
        levels={levels}
        sortOptions={sortOptions}
      />
      <div className="flex flex-col md:flex-row bg-white rounded-xl shadow-lg w-full max-w-7xl h-full overflow-hidden">
        {/* Left Panel */}
        <div
          className={`md:w-1/2 h-full overflow-y-auto ${
            selectedId ? "hidden md:block" : "block"
          }`}
        >
          <Suspense fallback={<ListSkeleton />}>
            <AssignmentList
              searchParams={searchParamsObj}
              assignments={data.results}
              totalPages={totalPages}
            />
          </Suspense>
        </div>

        {/* Right Panel */}
        {selectedId && (
          <div className="md:w-1/2 w-full h-full bg-white p-6 overflow-y-auto border-t md:border-t-0 md:border-l">
            <Suspense fallback={<DetailSkeleton />}>
              <AssignmentDetailServer id={selectedId} />
            </Suspense>
          </div>
        )}
        {!selectedId && (
          <div className="md:w-1/2 w-full h-full bg-white p-6 flex items-center justify-center">
            <p className="text-gray-500">
              Select an assignment to view details
            </p>
          </div>
        )}
      </div>
      {showAddOverlay && (
        <AddAssignmentOverlay
          filters={data.filters}
        />
      )}
    </div>
    
  );
}
