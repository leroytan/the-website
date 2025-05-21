export default function SkeletonAssignments() {
  return (
    <div className="min-h-screen bg-[#FFF3E9] flex flex-col md:flex-row p-6 gap-4">
      {/* Sidebar (static to maintain layout structure) */}
      <aside className="md:w-1/4 w-full md:pr-6">
        <h2 className="text-2xl font-bold text-customDarkBlue mb-6">
          My Dashboard
        </h2>
        <nav className="flex md:flex-col flex-row gap-2 overflow-x-auto whitespace-nowrap">
          {["Active Assignments", "Pending Assignments"].map((label, i) => (
            <div
              key={i}
              className="h-10 bg-gray-300 animate-pulse rounded-md"
            />
          ))}
        </nav>
      </aside>

      {/* Assignment list skeleton */}
      <section className="md:w-3/4 w-full">
        <div className="hidden md:grid grid-cols-5 bg-customDarkBlue text-white font-semibold rounded-t-xl p-4 text-sm">
          <div>Level and Subject</div>
          <div>Tuition Address</div>
          <div>Rate</div>
          <div>Schedule</div>
          <div>Actions</div>
        </div>

        <div className="space-y-4 bg-white rounded-b-xl p-4">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="md:grid md:grid-cols-5 flex flex-col gap-4 bg-orange-100 p-4 rounded-xl animate-pulse"
            >
              <div className="h-4 w-full bg-gray-300 rounded" />
              <div className="h-4 w-full bg-gray-300 rounded" />
              <div className="h-4 w-full bg-gray-300 rounded" />
              <div className="space-y-1">
                <div className="h-3 w-3/4 bg-gray-300 rounded" />
                <div className="h-3 w-2/3 bg-gray-300 rounded" />
              </div>
              <div className="flex flex-col gap-2">
                <div className="h-8 bg-gray-300 rounded-full" />
                <div className="h-8 bg-gray-300 rounded-full" />
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}