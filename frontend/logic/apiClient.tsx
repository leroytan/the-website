export const apiClient = async (
    url: string,
    options: RequestInit = {},
    logout: () => void // Accept the logout function as a parameter
  ) => {
    const response = await fetch(url, options)
  
    if (response.status === 401) {
      // Attempt to refresh the token
      const refreshResponse = await fetch('/api/auth/refresh', { method: 'POST' })
  
      if (refreshResponse.status === 200) {
        // Retry the original request after refreshing the token
        return fetch(url, options)
      } else {
        // If the refresh token is expired, log the user out
        logout() // Call the logout function
        throw new Error('Session expired. Please log in again.')
      }
    }
  
    return response
  }