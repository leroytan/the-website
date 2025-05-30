import "@/app/globals.css";
import { AuthProvider } from "@/context/authContext";
import { ErrorProvider } from "@/context/errorContext";
import ErrorDialog from "@/components/errorDialog";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <ErrorProvider>
              {children}
            <ErrorDialog />
          </ErrorProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
