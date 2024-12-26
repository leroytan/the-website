import ComponentLayout from "@/components/layout";

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
