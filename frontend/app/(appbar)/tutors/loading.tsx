// app/(appbar)/tutors/loading.tsx

import { FilterSortBarSkeleton, TutorGridSkeleton } from "./_components/skeletons";

export default function Loading() {
  return (
    <>
      <div className="flex flex-col items-center bg-customLightYellow/50 min-h-[calc(100vh-64px)]">
        <FilterSortBarSkeleton />
        <div className="p-4 w-full max-w-7xl">
          <TutorGridSkeleton />
        </div>
      </div>
    </>
  );
}
