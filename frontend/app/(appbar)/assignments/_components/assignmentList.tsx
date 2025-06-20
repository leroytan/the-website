import Link from "next/link";
import { Pagination } from "./pagination";
import { MapPin, CalendarDays, Book } from "lucide-react";
import { TuitionListing } from "@/components/types";
import { timeAgo } from "@/utils/date";

// Define the Assignment type if not already imported

interface AssignmentListProps {
  assignments: TuitionListing[];
  totalPages: number;
  searchParams: {
    page_number?: string;
    page_size?: string;
    query?: string;
    filters?: string;
    sort?: string;

    selected?: string;
    add?: string;
  };
}

export function AssignmentList({
  assignments,
  totalPages,
  searchParams,
}: AssignmentListProps) {
  // Determine currently selected assignment ID (to highlight it in the list, if needed)
  const selectedId = searchParams.selected;
  // Determine the current page number
  const currentPage = searchParams.page_number
    ? parseInt(searchParams.page_number as string)
    : 1;

  return (
    <div className="space-y-4">
      {/* Assignment Cards List */}
      <div>
        {assignments.map((assign) => {
          const isSelected = assign.id == Number(selectedId);
          return (
            <Link
              prefetch={false}
              key={assign.id}
              href={createSelectedURL(searchParams, assign.id!.toString())}
              className={`relative block px-10 py-5 border transition-colors ${
                isSelected
                  ? "bg-yellow-50 border-blue-100 text-customDarkBlue"
                  : "border-gray-200 text-customDarkBlue hover:bg-gray-100 hover:border-gray-300 shadow-sm"
              } `}
            >
              <div className="absolute top-4 right-4 text-green-600 bg-green-100 font-bold px-3 py-1 rounded-lg">
                ${assign.estimated_rate_hourly}/hour
              </div>
              <h3 className="text-xl font-semibold mb-2">{assign.title}</h3>
              <p className="text-sm text-gray-600">
                <span className="flex items-center">
                  <MapPin className="mr-1" />
                  {assign.location}
                </span>
                <span className="flex items-center mt-1">
                  <Book className="mr-1" />
                  {assign.subjects.slice(0, 5).join(", ")}
                  {assign.subjects.length > 5 && (
                    <> +{assign.subjects.length - 5} more</>
                  )}{" "}
                  - {assign.level}
                </span>
                <span className="flex items-center mt-1">
                  <CalendarDays className="mr-1" />
                  {assign.available_slots &&
                  assign.available_slots.length > 0 ? (
                    <>
                      {assign.available_slots.slice(0, 3).map((slot, idx) => (
                        <span key={slot.id}>
                          {idx > 0 && ", "}
                          {`${slot.day} ${slot.start_time}-${slot.end_time}`}
                        </span>
                      ))}
                      {assign.available_slots.length > 3 && (
                        <> +{assign.available_slots.length - 3} more</>
                      )}
                    </>
                  ) : (
                    "No slots"
                  )}
                </span>
              </p>
              <span className="flex text-sm text-gray-500 mt-2">
                posted&nbsp;
                {timeAgo(assign.created_at!)}
              </span>
            </Link>
          );
        })}
        {assignments.length === 0 && (
          <p className="text-gray-500 text-center p-4">
            No assignments found for the selected filters.
          </p>
        )}
      </div>
      {/* End of List Message */}
      {assignments.length > 0 && currentPage === totalPages && (
        <div className="text-center text-gray-500 mt-4">
          <p>You’ve reached the end of the list.</p>
        </div>
      )}

      {/* Pagination Controls */}
      <div className="mt-6">
        <Pagination totalPages={totalPages} />
      </div>
    </div>
  );
}

// Helper to construct URL for selecting an assignment (preserves current filters and page)
function createSelectedURL(
  currentParams: { [key: string]: string | string[] | undefined },
  id: string
) {
  const params = new URLSearchParams();
  // Preserve page, filters, sort from currentParams
  for (const key in currentParams) {
    if (key === "selected" || currentParams[key] === undefined) continue;
    const value = currentParams[key];
    if (Array.isArray(value)) {
      value.forEach((val) => params.append(key, val));
    } else {
      params.set(key, value);
    }
  }
  // Set the selected assignment ID
  params.set("selected", id);
  return `/assignments?${params.toString()}`;
}
