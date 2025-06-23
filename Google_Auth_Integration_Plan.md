# Detailed Plan for Google Signup/Login Integration

This plan outlines the steps to integrate Google authentication, allowing both Google-only sign-ups/logins and linking Google accounts to existing email/password accounts.

## I. Backend Modifications (Python/FastAPI)

1.  **Google API Project Setup**:
    *   Create a new project in the Google Cloud Console.
    *   Enable the Google People API (if needed for user profile info).
    *   Configure OAuth consent screen.
    *   Create OAuth 2.0 Client IDs (Web application type).
    *   Note down `Client ID` and `Client Secret`.
    *   Add authorized redirect URIs (e.g., `http://localhost:8000/api/auth/google/callback` for development, and your production URL).

2.  **Configuration (`api/config.py`)**:
    *   Add Google OAuth credentials to `settings`:
        ```python
        # api/config.py
        class Settings:
            # ... existing settings ...
            GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
            GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
            GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")
        ```
    *   Update `.env.example` accordingly.

3.  **Database Model Update (`api/storage/models.py`)**:
    *   Modify the `User` model to include a `google_id` field. This field will store the unique identifier provided by Google for users who sign up or link their accounts via Google. It should be nullable, as not all users will have a Google ID.
    *   Consider making the `password` field nullable if a user can *only* sign up with Google and never set a password. This requires careful handling in the authentication logic.
        ```python
        # api/storage/models.py
        from typing import Optional
        # ...
        class User(BaseModel):
            # ... existing fields ...
            google_id: Optional[str] = Field(None, unique=True, index=True)
            password: Optional[str] = None # Make password optional if Google-only users don't have one
        ```

4.  **Authentication Service (`api/auth/auth_service.py`)**:
    *   **New Method: `authenticate_google_user`**:
        *   This method will take the Google authorization code.
        *   Exchange the code for access tokens with Google's OAuth2 endpoint.
        *   Use the access token to fetch user information from Google (e.g., email, name, Google ID).
        *   **Logic**:
            *   Check if a user with the `google_id` already exists. If yes, log them in.
            *   Check if a user with the *same email* exists but without a `google_id`. If yes, link the Google ID to this existing account and log them in.
            *   If no existing user, create a new user account with the Google ID and provided email/name.
            *   Generate and return application-specific access and refresh tokens.
        *   This method will likely interact with `api.storage.storage_service.StorageService` to query/create users.

5.  **Logic Layer (`api/logic/user_logic.py` or `api/logic/logic.py`)**:
    *   Create a new function, e.g., `handle_google_login_signup`, that orchestrates the `AuthService` and `StorageService` calls. This function will encapsulate the business logic for Google authentication, including user creation, linking, and token generation.

6.  **API Endpoints (`api/router/auth.py`)**:
    *   **`/api/auth/google/login` (GET)**:
        *   This endpoint will redirect the user to Google's OAuth consent screen.
        *   It will construct the Google authorization URL using `GOOGLE_CLIENT_ID`, `GOOGLE_REDIRECT_URI`, and desired scopes (e.g., `email`, `profile`).
        ```python
        # api/router/auth.py
        from starlette.responses import RedirectResponse
        from api.config import settings
        # ...
        @router.get("/api/auth/google/login")
        async def google_login():
            google_auth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"response_type=code&"
                f"client_id={settings.GOOGLE_CLIENT_ID}&"
                f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
                f"scope=openid%20email%20profile&"
                f"access_type=offline&" # To get refresh token from Google if needed
                f"prompt=consent" # To ensure consent screen is shown
            )
            return RedirectResponse(google_auth_url)
        ```
    *   **`/api/auth/google/callback` (GET)**:
        *   This is the redirect URI Google will call after user authentication.
        *   It will receive the `code` (authorization code) from Google as a query parameter.
        *   Call the new logic function (e.g., `Logic.handle_google_login_signup`) with the `code`.
        *   Upon successful authentication, set the application's JWTs as HTTP-only cookies and redirect the user to the frontend dashboard or a success page.
        *   Handle errors (e.g., invalid code, user denied access).
        ```python
        # api/router/auth.py
        @router.get("/api/auth/google/callback")
        async def google_callback(request: Request, response: Response, code: str = None, error: str = None):
            if error:
                raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
            
            if not code:
                raise HTTPException(status_code=400, detail="Authorization code missing")

            try:
                tokens = Logic.handle_google_login_signup(code) # This is the new logic function
                RouterAuthUtils.update_tokens(tokens, response)
                # Redirect to frontend dashboard or success page
                return RedirectResponse(url="/dashboard") # Adjust this URL as needed
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Google login failed: {str(e)}")
        ```

## II. Frontend Modifications (Next.js/React)

1.  **Google Client ID Configuration**:
    *   Add `NEXT_PUBLIC_GOOGLE_CLIENT_ID` to your `.env.example` and `.env.local` files in the `frontend` directory. This will be used by the frontend to initiate the Google OAuth flow.
        ```
        # frontend/.env.example
        NEXT_PUBLIC_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
        ```

2.  **Login Page (`frontend/app/login/LoginForm.tsx`)**:
    *   Add a "Sign in with Google" button.
    *   When clicked, this button will redirect the user to the backend's Google login endpoint (`/api/auth/google/login`).
    *   Consider adding a separator (e.g., "OR") between traditional login and Google login.

    ```tsx
    // frontend/app/login/LoginForm.tsx
    // ... existing imports ...
    import { FcGoogle } from "react-icons/fc"; // You might need to install react-icons

    // ... inside LoginForm component ...

    const handleGoogleLogin = () => {
        window.location.href = `${BASE_URL}/api/auth/google/login`; // Redirect to backend's Google login endpoint
    };

    return (
        // ... existing JSX ...
        <form onSubmit={handleSubmit}>
            {/* ... existing email/password fields ... */}
            <motion.button
                type="submit"
                // ... existing styles ...
            >
                Log In
            </motion.button>
        </form>

        <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
                <span className="bg-white px-2 text-gray-500">Or continue with</span>
            </div>
        </div>

        <motion.button
            type="button"
            onClick={handleGoogleLogin}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full flex items-center justify-center bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors duration-200 shadow-sm"
        >
            <FcGoogle className="mr-2 h-5 w-5" />
            Sign in with Google
        </motion.button>

        {/* ... existing signup link and footer ... */}
    );
    ```

3.  **Signup Page (`frontend/app/signup/SignupForm.tsx`)**:
    *   Similar to the login page, add a "Sign up with Google" button that redirects to the backend's Google login endpoint.

    ```tsx
    // frontend/app/signup/SignupForm.tsx
    // ... existing imports ...
    import { FcGoogle } from "react-icons/fc"; // You might need to install react-icons

    // ... inside SignupPage component ...

    const handleGoogleSignup = () => {
        window.location.href = `${BASE_URL}/api/auth/google/login`; // Redirect to backend's Google login endpoint
    };

    return (
        // ... existing JSX ...
        <form onSubmit={handleSubmit}>
            {/* ... existing signup fields ... */}
            <motion.button
                type="submit"
                // ... existing styles ...
            >
                Sign Up
            </motion.button>
        </form>

        <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
                <span className="bg-white px-2 text-gray-500">Or continue with</span>
            </div>
        </div>

        <motion.button
            type="button"
            onClick={handleGoogleSignup}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full flex items-center justify-center bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors duration-200 shadow-sm"
        >
            <FcGoogle className="mr-2 h-5 w-5" />
            Sign up with Google
        </motion.button>

        {/* ... existing login link and footer ... */}
    );
    ```

4.  **Handling Redirects**:
    *   The backend's `/api/auth/google/callback` endpoint will redirect the user back to the frontend (e.g., `/dashboard`). The `AuthContext` in the frontend should automatically pick up the new cookies and update the user's authentication state.

## III. High-Level Flow Diagram

```mermaid
graph TD
    A[Frontend Login/Signup Page] --> B{Click "Sign in with Google"};
    B --> C[Redirect to Backend /api/auth/google/login];
    C --> D[Backend Redirects to Google OAuth Consent Screen];
    D --> E{User Authenticates with Google};
    E --> F[Google Redirects to Backend /api/auth/google/callback with Code];
    F --> G[Backend Exchanges Code for Tokens with Google];
    G --> H{Backend Fetches Google User Info};
    H --> I{Check User in DB};
    I -- User exists with Google ID --> J[Log in existing Google user];
    I -- User exists with matching email, no Google ID --> K[Link Google ID to existing account & Log in];
    I -- No existing user --> L[Create new user with Google ID];
    J --> M[Backend Generates App JWTs];
    K --> M;
    L --> M;
    M --> N[Backend Sets JWTs as HTTP-only Cookies];
    N --> O[Backend Redirects to Frontend Dashboard];
    O --> P[Frontend AuthContext Updates State];
    P --> Q[User is Logged In];
```

## IV. Clarifications and Considerations

*   **Error Handling**: Implement robust error handling on both frontend and backend for Google OAuth failures, network issues, and database errors.
*   **User Experience**: Provide clear feedback to the user during the authentication process (e.g., loading states, success/error messages).
*   **Security**: Ensure all sensitive information (client secrets) are stored securely and not exposed on the frontend. Use HTTPS in production.
*   **Scopes**: Request only necessary Google API scopes (e.g., `email`, `profile`, `openid`).
*   **Token Management**: The existing JWT token management (access and refresh tokens) should be leveraged. The Google authentication flow will ultimately result in the issuance of these application-specific JWTs.
*   **User Profile Data**: Decide what user data (name, profile picture, etc.) you want to retrieve from Google and store in your database.
*   **Password Nullability**: If `password` is made `Optional[str]`, ensure that any existing logic that assumes a password is present (e.g., password reset, password change) handles `None` values gracefully for Google-only accounts.