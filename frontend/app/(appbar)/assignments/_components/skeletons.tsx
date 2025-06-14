"use client";
import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import MultiSelectButton from "@/components/multiSelectButton";

// app/assignments/Skeletons.tsx
export function AssignmentListSkeleton() {
  const dummyItems = Array.from({ length: 5 }); // Render 5 placeholder cards

  return (
    <div>
      {/* Skeleton cards */}
      {dummyItems.map((_, idx) => (
        <div
          key={idx}
          className="relative block px-10 py-5 border border-gray-200 rounded-md shadow-sm animate-pulse"
        >
          {/* Estimated Rate */}
          <div className="absolute top-4 right-4 h-6 w-24 bg-gray-200 rounded-md"></div>

          {/* Title */}
          <div className="h-6 bg-gray-200 rounded-md w-3/4 mb-4"></div>

          {/* Location */}
          <div className="h-4 bg-gray-200 rounded-md w-1/2 mb-2"></div>

          {/* Subjects */}
          <div className="h-4 bg-gray-200 rounded-md w-2/3 mb-2"></div>

          {/* Available Slots */}
          <div className="h-4 bg-gray-200 rounded-md w-1/3 mb-2"></div>

          {/* Posted Time */}
          <div className="h-4 bg-gray-200 rounded-md w-1/4 mt-2"></div>
        </div>
      ))}

      {/* End of List Message */}
      <div className="text-center text-gray-500 mt-4">
        <div className="h-4 bg-gray-200 rounded-md w-1/2 mx-auto"></div>
      </div>

      {/* Pagination Controls */}
      <div className="mt-6 flex justify-center items-center space-x-2">
        {/* Previous Button */}
        <div className="h-8 w-8 bg-gray-200 rounded-lg animate-pulse"></div>

        {/* Page Numbers */}
        {Array.from({ length: 5 }).map((_, idx) => (
          <div
            key={idx}
            className="h-8 w-8 bg-gray-200 rounded-lg animate-pulse"
          ></div>
        ))}

        {/* Next Button */}
        <div className="h-8 w-8 bg-gray-200 rounded-lg animate-pulse"></div>
      </div>
    </div>
  );
}

export function AssignmentDetailSkeleton() {
  // Skeleton for the detail panel
  return (
    <div className="p-6">
      {/* Title */}
      <div className="h-6 bg-gray-200 rounded w-1/2 mb-4 animate-pulse" />

      {/* Subject */}
      <div className="h-4 bg-gray-200 rounded w-1/3 mb-2 animate-pulse" />

      {/* Level */}
      <div className="h-4 bg-gray-200 rounded w-1/3 mb-2 animate-pulse" />

      {/* Location */}
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-2 animate-pulse" />

      {/* Rate */}
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-4 animate-pulse" />

      {/* Description */}
      <div className="h-4 bg-gray-200 rounded w-full mb-2 animate-pulse" />
      <div className="h-4 bg-gray-200 rounded w-full mb-2 animate-pulse" />
      <div className="h-4 bg-gray-200 rounded w-2/3 mb-2 animate-pulse" />

      {/* Apply Button */}
      <div className="h-10 bg-gray-200 rounded w-24 mt-4 animate-pulse" />
    </div>
  );
}
export function FilterSortBarSkeleton() {
  return (
    <div className="sticky top-14 z-10 bg-white px-6 pt-4 pb-3 shadow-md w-full">
      <div className="flex flex-wrap gap-4 justify-start items-end">
        {/* MultiSelect for Subjects */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={[]}
            selected={[]}
            onChange={() => {}}
            placeholder="Loading Subjects..."
          />
        </div>
        {/* MultiSelect for Levels */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={[]}
            selected={[]}
            onChange={() => {}}
            placeholder="Loading Levels..."
          />
        </div>
        {/* Sort select with dropdown */}
        <div className="min-w-[180px]">
          <DropDown
            placeholder="Loading Sort Options..."
            stringOnDisplay={""}
            stateController={() => {}}
            iterable={[]}
            renderItem={() => <span>Loading...</span>}
          />
        </div>
        {/* Filter Button */}
        <Button
          className="ml-2 px-6 py-2 bg-customYellow text-white rounded-full font-semibold hover:bg-customOrange hover:cursor-not-allowed transition-colors"
          onClick={() => {}}
          disabled={true}
        >
          Clear All Filters
        </Button>
      </div>
    </div>
  );
}
