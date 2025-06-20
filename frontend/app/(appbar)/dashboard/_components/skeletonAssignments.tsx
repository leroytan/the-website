export default function SkeletonAssignments() {
  return (
    <div className="min-h-screen bg-customLightYellow/45 p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="mb-8">
          <div className="h-8 bg-gray-200 rounded-lg w-48 animate-pulse mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-64 animate-pulse"></div>
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-1/4">
            <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm p-6 border border-customLightYellow/60">
              <nav className="space-y-2">
                {["Active Assignments", "Pending Applications"].map((label, i) => (
                  <div
                    key={i}
                    className="h-12 bg-gray-200 animate-pulse rounded-lg"
                  />
                ))}
              </nav>
            </div>
          </aside>

          {/* Assignment list skeleton */}
          <section className="lg:w-3/4">
            <div className="grid grid-cols-1 gap-6">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm p-6 border border-customLightYellow/60 animate-pulse"
                >
                  <div className="flex flex-col md:flex-row justify-between gap-4">
                    <div className="flex-1 space-y-3">
                      {/* Title skeleton */}
                      <div className="h-6 bg-gray-200 rounded-lg w-3/4"></div>
                      
                      {/* Description skeleton */}
                      <div className="space-y-2">
                        <div className="h-4 bg-gray-200 rounded w-full"></div>
                        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                      </div>
                      
                      {/* Tags skeleton */}
                      <div className="flex gap-2">
                        <div className="h-6 bg-gray-200 rounded-full w-20"></div>
                        <div className="h-6 bg-gray-200 rounded-full w-24"></div>
                        <div className="h-6 bg-gray-200 rounded-full w-16"></div>
                      </div>
                    </div>
                    
                    {/* Action buttons skeleton */}
                    <div className="flex gap-2">
                      <div className="h-10 bg-gray-200 rounded-lg w-24"></div>
                      <div className="h-10 bg-gray-200 rounded-lg w-24"></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}