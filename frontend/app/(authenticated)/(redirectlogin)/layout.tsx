'use client'

import { useAuth } from "@/logic/AuthContent";
import { redirect } from "next/navigation";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, loading } = useAuth()
  if (!isAuthenticated) {
    redirect('/login')
  }
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
