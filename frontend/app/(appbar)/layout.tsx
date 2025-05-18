import "@/app/globals.css";
import ComponentLayout from "@/components/layout";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <ComponentLayout>{children}</ComponentLayout>;
}
