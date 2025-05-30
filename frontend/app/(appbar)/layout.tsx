import ComponentLayout from "@/components/layout";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return <ComponentLayout>{children}</ComponentLayout>;
}
