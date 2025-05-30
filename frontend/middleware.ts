import { NextRequest, NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get("access_token")?.value;
  const refreshToken = request.cookies.get("refresh_token")?.value;
  const intendsToBeTutor = request.cookies.get("intends_to_be_tutor")?.value;
  const tutorProfileComplete = request.cookies.get("tutor_profile_complete")?.value;

  const isAuthenticated = !!accessToken;

  const unauthenticatedRoutes = ["/", "/login", "/signup"];
  const authenticatedRoutes = ["/dashboard", "/chat"];

  const { pathname } = request.nextUrl;

  const isUnauthenticatedRoute = unauthenticatedRoutes.includes(pathname);
  const isAuthenticatedRoute = authenticatedRoutes.some((route) =>
    pathname.startsWith(route)
  );

  // If user is logged in and tries to access login/signup
  if (isUnauthenticatedRoute && isAuthenticated) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // If user is accessing protected route and is not authenticated
  if (isAuthenticatedRoute && !isAuthenticated) {
    if (!refreshToken) {
      // Redirect to login with redirectTo
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirectTo", pathname);
      return NextResponse.redirect(loginUrl);
    }

    return NextResponse.redirect(
      new URL(`/login?redirectTo=${pathname}`, request.url)
    );
  }
  // Redirect tutors who need to complete onboarding
  if (intendsToBeTutor === "true" && tutorProfileComplete !== "true" && pathname !== '/onboarding/tutor') {
    return NextResponse.redirect(new URL('/onboarding/tutor', request.url));
  }
  //Redirect users who have completed onboarding to dashboard
  if (pathname === '/onboarding/tutor' && !tutorProfileComplete) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  return NextResponse.next();
  
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
