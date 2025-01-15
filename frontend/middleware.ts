// middleware.ts
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token');

  // No token? Redirect to login
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Has token? Let them in
  return NextResponse.next();
}


export const config = {
  matcher: ['/protected/:path*']
};