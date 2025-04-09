import ComponentLayout from "@/components/layout";
import "@/app/globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ComponentLayout>{children}</ComponentLayout>
      </body>
    </html>
  );
}
