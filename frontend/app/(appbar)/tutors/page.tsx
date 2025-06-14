import { Suspense } from "react";
import { BASE_URL } from "@/utils/constants";
import { FilterSortBar } from "./_components/filterSort";
import { TutorGrid } from "./_components/tutorGrid";
import { Pagination } from "./_components/pagination";
import { TutorGridSkeleton } from "./_components/skeletons";
import { TuitionListingFilters, Tutor } from "@/components/types";

interface TutorResponse {
  results: Tutor[];
  num_pages: number;
  filters: TuitionListingFilters;
  sorts: { id: string; name: string }[];
}
export default async function TutorsPage({
  searchParams,
}: {
  searchParams: Promise<{
    page_number?: string;
    page_size?: string;
    query?: string;
    filter_by?: string;
    sort_by?: string;
  }>;
}) {
  const searchParamsObj = await searchParams;
  const url = new URL("/api/tutors", BASE_URL);
  if (searchParamsObj.query)
    url.searchParams.set("query", searchParamsObj.query);
  if (searchParamsObj.filter_by)
    url.searchParams.set("filter_by", searchParamsObj.filter_by);
  if (searchParamsObj.sort_by)
    url.searchParams.set("sort_by", searchParamsObj.sort_by);
  url.searchParams.set("page_number", searchParamsObj.page_number || "1");
  url.searchParams.set("page_size", searchParamsObj.page_size || "6");

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch tutors");
  const data: TutorResponse = await res.json();

  return (
    <>
      <div className="flex flex-col items-center bg-customLightYellow/50 min-h-[calc(100vh-64px)]">
        <FilterSortBar
          subjects={data.filters.subjects}
          levels={data.filters.levels}
          sortOptions={data.sorts.map(({ id, name }) => ({
            value: id,
            label: name,
          }))}
        />
        <div className="p-4 w-full max-w-7xl">
          <Suspense fallback={<TutorGridSkeleton />}>
            <TutorGrid tutors={data.results} />
          </Suspense>

          <div className="mt-6">
            <Pagination totalPages={data.num_pages} />
          </div>
        </div>
      </div>
    </>
  );
}
