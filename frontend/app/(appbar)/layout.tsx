import ComponentLayout from "@/components/layout";
import { ErrorProvider } from "@/context/errorContext";
import { AlertProvider } from "@/context/alertContext";
import AlertDialog from "@/components/alertDialog";
import ErrorDialog from "@/components/errorDialog";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <ErrorProvider>
        <AlertProvider>
          <ComponentLayout>
            {children}
          </ComponentLayout>
          <AlertDialog />
          <ErrorDialog />
        </AlertProvider>
      </ErrorProvider>
    </>
  );
}
