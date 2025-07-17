export async function fetchCore(
  input: RequestInfo | URL, 
  init?: RequestInit
) {
  try {
    const response = await fetch(input, init);

    // If response is not OK, check for token version mismatch
    if (!response.ok) {
      const error = await response.json();

      if (error.code === 'TOKEN_VERSION_MISMATCH') {
        // Return an indicator of token mismatch
        return { response, tokenMismatch: true };
      }
    }

    return { response, tokenMismatch: false };
  } catch (error) {
    console.error('Fetch error:', error);
    return {
      response: new Response(
        JSON.stringify({ ok: true, error: 'Network error or fetch failed' }),
        { status: 0, headers: { 'Content-Type': 'application/json' } }
      ),
      tokenMismatch: false
    };
  }
}
