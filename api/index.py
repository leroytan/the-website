from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from models import (
    LoginRequest,
    LoginResponse,
    LoginPageResponse,
    SignupRequest,
    SignupResponse,
    HomepageResponse,
    ProfileResponse,
    UpdateProfileRequest,
    TutorOnboardingRequest,
    ClientOnboardingRequest
)

# Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# OAuth2 scheme for JWT bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function for authentication
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement JWT token validation here
    # For now, we'll just return a dummy user
    return {"id": "user_id", "email": "user@example.com", "userType": "tutor"}

# Routes
@app.get("/api/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.get("/api/auth/login", response_model=LoginPageResponse)
async def login_page(request: Request):
    """
    Get the login page data.
    This endpoint returns the necessary information for rendering the login form.
    """
    return LoginPageResponse(
        title="Login to THE (Teach Learn Excel)",
        description="Please enter your email and password to log in.",
        fields=[
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "required": True,
                "placeholder": "Enter your email"
            },
            {
                "name": "password",
                "type": "password",
                "label": "Password",
                "required": True,
                "placeholder": "Enter your password"
            }
        ]
    )

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    # Implement login logic here
    return {"token": "dummy_token", "userType": "tutor"}

@app.post("/api/auth/signup", response_model=SignupResponse, status_code=201)
async def signup(signup_data: SignupRequest):
    # Implement signup logic here
    return {
        "id": "new_user_id",
        "email": signup_data.email,
        "name": signup_data.name,
        "userType": signup_data.userType
    }

@app.get("/api/homepage", response_model=HomepageResponse)
async def get_homepage(current_user: dict = Depends(get_current_user)):
    # Implement homepage data retrieval logic here
    return {
        "userType": current_user["userType"],
        "featuredContent": [
            {"title": "Featured Item 1", "description": "Description 1", "url": "http://example.com/1"}
        ]
    }

@app.get("/api/profile", response_model=ProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    # Implement profile retrieval logic here
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": "User Name",
        "userType": current_user["userType"],
        "profileComplete": True
    }

@app.put("/api/profile")
async def update_profile(profile_data: UpdateProfileRequest, current_user: dict = Depends(get_current_user)):
    # Implement profile update logic here
    return {"message": "Profile updated successfully"}

@app.post("/api/onboarding/tutor")
async def complete_tutor_onboarding(onboarding_data: TutorOnboardingRequest, current_user: dict = Depends(get_current_user)):
    # Implement tutor onboarding logic here
    return {"message": "Tutor onboarding completed successfully"}

@app.post("/api/onboarding/client")
async def complete_client_onboarding(onboarding_data: ClientOnboardingRequest, current_user: dict = Depends(get_current_user)):
    # Implement client onboarding logic here
    return {"message": "Client onboarding completed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)