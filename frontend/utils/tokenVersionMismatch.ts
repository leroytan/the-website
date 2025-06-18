import { redirect } from 'next/navigation';

// Wrapper for fetch that automatically handles token version mismatch
export async function fetchWithTokenCheck(input: RequestInfo | URL, init?: RequestInit) {
  const response = await fetch(input, init);
  
  // If response is not OK, check for token version mismatch
  if (!response.ok) {
    const data = await response.json();
    if (data.message && data.message.includes('Token version mismatch')) {
      redirect('/logout');
    }
  }
  
  return response;
}