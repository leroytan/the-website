import { fetchCore } from './fetchCore';
import { redirect } from 'next/navigation';

export async function fetchServer(input: RequestInfo | URL, init?: RequestInit) {
  const { response, tokenMismatch } = await fetchCore(input, init);

  if (tokenMismatch) {
    // Server-side redirect to the logout page
    redirect('/logout');
  }

  return response;
}
