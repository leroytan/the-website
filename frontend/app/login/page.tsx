import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import LoginForm from "./LoginForm";
import { BASE_URL } from "@/utils/constants";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{redirectTo: string | undefined}>;
}) {
  const params = await searchParams;
  const redirectTo = params.redirectTo || "/dashboard";
  const cookieStore = await cookies();

  const accessToken = cookieStore.get("access_token")?.value;
  const refreshToken = cookieStore.get("refresh_token")?.value;

  // 1. Try checking if access_token exists
  if (accessToken) {
    redirect(redirectTo);
  }

  // 2. If no access, but refresh exists: try refreshing
  if (refreshToken) {
    const refreshRes = await fetch(`${BASE_URL}/auth/refresh`, {
      method: "POST",
      headers: {
        Cookie: `refresh_token=${refreshToken}`,
      },
    });

    if (refreshRes.ok) {
      redirect(redirectTo);
    }
  }

  // 3. If refresh fails, render login form
  return (
    <div>
      <LoginForm redirectTo={redirectTo} />
    </div>
  );
}
