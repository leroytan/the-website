import { NextRequest, NextResponse } from "next/server";
import { BASE_URL } from "./utils/constants";

export async function middleware(request: NextRequest) {
  const accesstoken = request.cookies.get("access_token");
  const refreshtoken = request.cookies.get("refresh_token");
  const isAuthenticated = !!accesstoken;

  const unauthenticatedRoutes = ["/login", "/signup"];
  const authenticatedRoutes = ["/dashboard", "/chat"];

  const path = request.nextUrl.pathname;

  const isUnauthenticatedRoute = unauthenticatedRoutes.includes(path);
  const isAuthenticatedRoute = authenticatedRoutes.some((route) =>
    path.startsWith(route)
  );

  // Handle unauthenticated routes
  if (isUnauthenticatedRoute) {
    if (isAuthenticated) {
      // If user is logged in, redirect away from login/signup pages
      return NextResponse.redirect(new URL("/", request.url));
    }
    return NextResponse.next();
  }

  // Handle authenticated routes
  if (isAuthenticatedRoute) {
    if (!isAuthenticated) {
      if (!refreshtoken) {
        return NextResponse.redirect(new URL("/login", request.url));
      }

      // Try refreshing access token
      const refreshResponse = await fetch(`${BASE_URL}/auth/refresh`, {
        method: "POST",
      });

      if (refreshResponse.ok) {
        return NextResponse.next();
      } else {
        return NextResponse.redirect(new URL("/login", request.url));
      }
    }
    return NextResponse.next();
  }

  // For routes that are neither authenticated nor unauthenticated
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
