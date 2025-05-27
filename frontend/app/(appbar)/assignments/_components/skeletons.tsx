// app/assignments/Skeletons.tsx
export function ListSkeleton() {
  // Skeleton for the list: we'll render a few dummy cards
  const dummyItems = Array.from({ length: 5 });
  return (
    <div className="px-4 py-4 md:p-6">
      {/* Skeleton filter bar */}
      <div className="bg-gray-100 h-20 rounded-md animate-pulse" />
      <div className="mt-4 space-y-4">
        {dummyItems.map((_, idx) => (
          <div key={idx} className="p-4 rounded border border-gray-200 shadow-sm">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2 animate-pulse" />
            <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function DetailSkeleton() {
  // Skeleton for the detail panel
  return (
    <div className="p-6">
      <div className="h-6 bg-gray-200 rounded w-1/2 mb-4 animate-pulse" />  {/* title */}
      <div className="h-4 bg-gray-200 rounded w-1/3 mb-2 animate-pulse" />  {/* subject */}
      <div className="h-4 bg-gray-200 rounded w-1/3 mb-2 animate-pulse" />  {/* level */}
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-2 animate-pulse" />  {/* location */}
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-4 animate-pulse" />  {/* rate */}
      <div className="h-4 bg-gray-200 rounded w-full mb-2 animate-pulse" /> {/* description lines */}
      <div className="h-4 bg-gray-200 rounded w-full mb-2 animate-pulse" />
      <div className="h-4 bg-gray-200 rounded w-2/3 mb-2 animate-pulse" />
      <div className="h-10 bg-gray-200 rounded w-24 mt-4 animate-pulse" />   {/* apply button */}
    </div>
  );
}
