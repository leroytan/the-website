'use client';
import Link from 'next/link';
import { useSearchParams, usePathname } from 'next/navigation';

interface PaginationProps {
  totalPages: number;
}

export function Pagination({ totalPages }: PaginationProps) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const currentPage = Number(searchParams.get('page')) || 1;

  if (totalPages <= 1) return null;  // no pagination needed

  // Helper to create URL for a given page number
  const createPageURL = (page: number) => {
    const params = new URLSearchParams(searchParams.toString());
    if (page === 1) {
      // Remove page param if page 1 (optional: to keep URL clean)
      params.delete('page');
    } else {
      params.set('page', page.toString());
    }
    // Clear selected param on page change
    params.delete('selected');
    return `${pathname}?${params.toString()}`;
  };

  // Create an array of page numbers to display (you can adjust window size if many pages)
  const pageNumbers = [];
  for (let p = 1; p <= totalPages; p++) {
    pageNumbers.push(p);
  }

  return (
    <div className="flex items-center justify-center space-x-2 text-md">
      {/* Previous Page Button */}
      {currentPage > 1 && (
        <Link href={createPageURL(currentPage - 1)} className="px-2 py-1 border rounded-lg hover:bg-gray-100">
          « Prev
        </Link>
      )}
      {/* Page Number Links */}
      {pageNumbers.map((page) => (
        <Link
          key={page}
          href={createPageURL(page)}
          className={`px-3 py-1 border rounded-lg ${page === currentPage ? 'bg-customDarkBlue text-white border-customDarkBlue' : 'hover:bg-gray-100'}`}
        >
          {page}
        </Link>
      ))}
      {/* Next Page Button */}
      {currentPage < totalPages && (
        <Link href={createPageURL(currentPage + 1)} className="px-2 py-1 border rounded hover:bg-gray-100">
          Next » 
        </Link>
      )}
    </div>
  );
}
