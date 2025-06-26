"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import LoginForm from "./LoginForm";
import { useAuth } from "@/context/authContext";
import { Tutor, User } from "@/components/types";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirectTo") || "/";
  const { refetch } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");

    const handleAuthCallback = async () => {
      if (accessToken && refreshToken) {
        // Set tokens in cookies
        document.cookie = `access_token=${accessToken}; path=/; SameSite=Lax; Secure`;
        document.cookie = `refresh_token=${refreshToken}; path=/; SameSite=Lax; Secure`;
        
        // Clear the tokens from the URL
        await refetch(); // Refresh user and tutor data for authcontext
        router.replace(redirectTo, undefined);
        setChecking(false);
        return;
      }

      const tryRefresh = async () => {
        try {
          const res = await fetch(`/api/auth/refresh`, {
            method: "POST",
            credentials: "include",
          });

          if (res.ok) {
            await refetch(); // refresh user and tutor data for authcontext
            // Fetch user state and set cookies
            const meRes = await fetchWithTokenCheck(`/api/me"`);
            const { user, tutor }: { user: User; tutor: Tutor | null } =
              await meRes.json();

            // Set helper cookies for middleware
            if (user.intends_to_be_tutor && !tutor) {
              document.cookie = `intends_to_be_tutor=${!!user.intends_to_be_tutor}; path=/; SameSite=Lax; Secure`;
              document.cookie = `tutor_profile_complete=${!!tutor}; path=/; SameSite=Lax; Secure`;
            }
            router.replace(redirectTo); // silently redirect, no flash
            router.refresh(); // refresh the page to get updated data
          } else {
            setShowLogin(true); // show form only if refresh fails
          }
        } catch (err) {
          console.error("Refresh failed:", err);
          setShowLogin(true);
        } finally {
          setChecking(false);
        }
      };

      tryRefresh();
    };

    handleAuthCallback();
  }, [redirectTo, router, searchParams, refetch]);

  if (checking) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner" />
      </div>
    );
  }
  return <>{showLogin && <LoginForm redirectTo={redirectTo} />}</>;
}
