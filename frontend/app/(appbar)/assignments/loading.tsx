import {
  AssignmentListSkeleton,
  AssignmentDetailSkeleton,
  FilterSortBarSkeleton,
} from "./_components/skeletons";

const Loading = () => {
  return (
    <div className="flex flex-col items-center bg-customLightYellow h-[calc(100vh-64px)]">
      <FilterSortBarSkeleton />
      <div className="flex flex-col md:flex-row bg-white rounded-xl shadow-lg w-full max-w-7xl h-full overflow-hidden">
        {/* Left Panel */}
        <div
          className={`md:w-1/2 h-full overflow-y-auto block`}
        >
          <AssignmentListSkeleton />
        </div>

        {/* Right Panel */}
          <div className="md:w-1/2 w-full h-full bg-white p-6 overflow-y-auto border-t md:border-t-0 md:border-l">
            <AssignmentDetailSkeleton />
          </div>
      </div>
    </div>
  );
};

export default Loading;
