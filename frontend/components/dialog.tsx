export function Dialog({
  children,
  className
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[900]">
      <div className={`bg-white p-6 rounded-lg shadow-lg w-1/2 ${className}`}>{children}</div>
    </div>
  );
}