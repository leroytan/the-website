import { cookies } from "next/headers";
import ComponentLayout from "@/components/layout";
import { BASE_URL } from "@/utils/constants";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  let userWithRole = null;

  if (accessToken) {
    try {
      const res = await fetch(`${BASE_URL}/me`, {
        headers: {
          Cookie: accessToken ? `access_token=${accessToken}` : "",
        },
        cache: "no-store",
      });

      if (res.ok) {
        const data = await res.json();
        const isTutor = data.tutor !== null;
        userWithRole = {
          ...data.user,
          role: isTutor ? "tutor" : "client",
          tutorProfile: data.tutor ?? null,
        };
      }
    } catch (e) {
      console.error("Error fetching user info:", e);
    }
  }

  return <ComponentLayout user={userWithRole}>{children}</ComponentLayout>;
}
