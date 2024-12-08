// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token');

  // No ID (token)? You're going back to the entrance (login)
  if (!token && request.nextUrl.pathname.startsWith('/protected')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Has ID? Go right ahead
  return NextResponse.next();
}

// Which doors does this bouncer watch?
export const config = {
  matcher: ['/protected/:path*']  // Only checks people trying to enter VIP areas
};