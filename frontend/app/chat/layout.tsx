import "@/app/globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
