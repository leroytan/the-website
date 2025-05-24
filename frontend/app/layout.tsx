import "@/app/globals.css";
import { AuthProvider } from "@/context/authContext";
import { cookies } from "next/headers";
import { ErrorProvider } from "@/context/errorContext";
import ErrorDialog from "@/components/errorDialog";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  const isAuthenticated = !!accessToken;
  return (
    <html lang="en">
      <body>
        <AuthProvider isAuthenticated={isAuthenticated}>
          <ErrorProvider>
            {children}
            <ErrorDialog />
          </ErrorProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
