'use client';

import { fetchCore } from './fetchCore';
import { useRouter } from 'next/navigation';

export async function fetchClient(input: RequestInfo | URL, init?: RequestInit) {
  const { response, tokenMismatch } = await fetchCore(input, init);

  if (tokenMismatch) {
    // Client-side redirect using useRouter
    const router = useRouter();
    router.push('/logout'); // Redirect to the logout page
  }

  return response;
}
