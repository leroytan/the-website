'use client';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { FormEvent, useRef } from 'react';

export default function SearchBar() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const term = inputRef.current?.value || '';
    const params = new URLSearchParams(searchParams.toString());
    if (term) {
      params.set('query', term);
    } else {
      params.delete('query');
    }
    // Navigate to the same page with updated query param
    router.replace(`${pathname}?${params.toString()}`);
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <input 
        type="search"
        ref={inputRef}
        placeholder="Search tutors..." 
        defaultValue={searchParams.get('query') ?? ''} 
        className="w-full rounded border px-3 py-2"
      />
      <button type="submit" className="sr-only">Search</button>
      {/* (Optional) A magnifying glass icon could be absolutely positioned for UX */}
    </form>
  );
}
