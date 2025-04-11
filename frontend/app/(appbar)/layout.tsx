import ComponentLayout from "@/components/layout";
import "@/app/globals.css";
import { AuthProvider } from "@/components/AuthContent";
import { cookies } from "next/headers";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = cookies();
  const accessToken = cookieStore.get("access_token");
  const isAuthenticated = !!accessToken;
  return (
    <html lang="en">
      <body>
        <AuthProvider isAuthenticated={isAuthenticated}>
        <ComponentLayout>{children}</ComponentLayout>
        </AuthProvider>
      </body>
    </html>
  );
}
