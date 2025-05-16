export default function Loader() {
  return (
    <div className="flex justify-center items-center py-10">
      <span className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-400"></span>
      <span className="ml-2 text-orange-400">Loading assignments...</span>
    </div>
  );
}