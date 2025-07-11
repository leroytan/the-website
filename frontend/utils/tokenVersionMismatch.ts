import { redirect } from 'next/navigation';
import logger from './logger';

// Wrapper for fetch that automatically handles token version mismatch
export async function fetchWithTokenCheck(input: RequestInfo | URL, init?: RequestInit) {
  try{
    const response = await fetch(input, init);
  
    // If response is not OK, check for token version mismatch
    if (!response.ok) {
      const error = await response.json();
    
      if (error.code === 'TOKEN_VERSION_MISMATCH') {
        // Handle forced re-authentication
        redirect('/logout');
      }
    }
    
    return response;
  } catch (error) {
    logger.error("Fetch error:", error);
    // Handle specific fetch error cases
    if (error instanceof TypeError) {
      // Handle fetch-specific errors (like network failures)
    } else {
      // Handle general errors (non-network related)
    }
    // throw error; // Optionally re-throw the error after handling it
    return new Response(JSON.stringify({
      ok: true,
      error: "Network error or fetch failed"
    }), {
      status: 0,
      headers: { "Content-Type": "application/json" }
    });
  }
}