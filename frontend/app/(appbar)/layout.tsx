import ComponentLayout from "@/components/layout";
import "@/app/globals.css";
import { AuthProvider } from "@/components/AuthContent";
import { cookies } from "next/headers";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  const isAuthenticated = !!accessToken;
  return (
      <>
        <AuthProvider isAuthenticated={isAuthenticated}>
        <ComponentLayout>{children}</ComponentLayout>
        </AuthProvider>
      </>
  );
}
