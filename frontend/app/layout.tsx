import "@/app/globals.css";
import { AuthProvider } from "@/context/authContext";
import { ErrorProvider } from "@/context/errorContext";
import { AlertProvider } from "@/context/alertContext";
import { WebSocketProvider } from "@/context/WebSocketContext";
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
            <AlertProvider>
              <WebSocketProvider>
                {children}
                <ErrorDialog />
              </WebSocketProvider>
            </AlertProvider>
          </ErrorProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
