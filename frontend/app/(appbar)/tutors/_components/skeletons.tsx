"use client";
import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import MultiSelectButton from "@/components/multiSelectButton";

export function TutorGridSkeleton() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: 6 }).map((_, idx) => (
        <div
          key={idx}
          className="animate-pulse rounded-lg border border-gray-200 bg-white p-6 shadow-md flex flex-col h-full"
        >
          {/* Skeleton for Image */}
          <div className="flex items-start mb-4">
            <div className="w-16 h-16 bg-gray-200 rounded-full mr-4 border-2 border-customYellow" />
            <div className="flex flex-col space-y-2">
              <div className="h-4 bg-gray-200 rounded w-32" />
              <div className="h-3 bg-gray-200 rounded w-20" />
            </div>
          </div>

          {/* Skeleton for Details */}
          <div className="mb-4 space-y-2 flex-grow">
            <div className="flex items-start">
              <div className="w-4 h-4 bg-gray-200 rounded-full mr-2" />
              <div className="h-3 bg-gray-200 rounded w-3/4" />
            </div>
            <div className="flex items-start">
              <div className="w-4 h-4 bg-gray-200 rounded-full mr-2" />
              <div className="h-3 bg-gray-200 rounded w-2/3" />
            </div>
            <div className="flex items-start">
              <div className="w-4 h-4 bg-gray-200 rounded-full mr-2" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
            <div className="flex items-start">
              <div className="h-3 bg-gray-200 rounded w-5/6" />
            </div>
            <div className="flex items-start">
              <div className="h-3 bg-gray-200 rounded w-4/5" />
            </div>
          </div>

          {/* Skeleton for Button */}

          <div className="h-10 bg-gray-200 rounded w-full" />
        </div>
      ))}
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
          Filter
        </Button>
      </div>
    </div>
  );
}
