import { BASE_URL } from "@/utils/constants";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

async function getMe(accessToken?: string) {
  const res = await fetch(`${BASE_URL}/me`, {
    cache: "no-store", // Disable caching to always get fresh data
    headers: {
      Cookie: accessToken ? `access_token=${accessToken}` : "",
    },
  });

  if (!res.ok) {
    return null;
  }

  return await res.json();
}

export default async function ProfilePage() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  const me = await getMe(accessToken);

  if (!me?.user) {
    redirect("/login?redirectTo=/profile");
  }

  if (me?.tutor) {
    redirect(`/tutors/${me.tutor.id}`);
  }

  redirect("/profile/tutee");
}
