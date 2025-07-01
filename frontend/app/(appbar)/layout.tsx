import ComponentLayout from "@/components/layout";
import AlertDialog from "@/components/alertDialog";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <ComponentLayout>
        {children}
      </ComponentLayout>
      <AlertDialog />
    </>
  );
}
