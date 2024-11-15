export const checkAuth = async () => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      // In Next.js, we use this instead of credentials: 'include'
      credentials: 'same-origin'
    });

    if (!response.ok) {
      throw new Error('Unauthorized');
    }

    const data = await response.json();
    return { authenticated: true, data };
  } catch (error) {
    return { authenticated: false, error };
  }
};