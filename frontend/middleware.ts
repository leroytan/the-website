import { NextRequest, NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get("access_token")?.value;
  const refreshToken = request.cookies.get("refresh_token")?.value;
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
      // Redirect to login with callback
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("callbackUrl", pathname);
      return NextResponse.redirect(loginUrl);
    }

    return NextResponse.redirect(
      new URL(`/login?callbackUrl=${pathname}`, request.url)
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
