"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import LoginForm from "./LoginForm";
import { useAuth } from "@/context/authContext";
import logger from "@/utils/logger";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirectTo") || "/";
  const { refetch, loading: authLoading, user, tutor } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");

    const handleAuthCallback = async () => {
      if (accessToken && refreshToken) {
        logger.debug("Google login callback detected with tokens");
        
        // Set tokens in cookies
        document.cookie = `access_token=${accessToken}; path=/; SameSite=Lax; Secure`;
        document.cookie = `refresh_token=${refreshToken}; path=/; SameSite=Lax; Secure`;

        await new Promise(r => setTimeout(r, 50));
        
        logger.debug("Tokens set in cookies, calling refetch...");
        
        // Clear the tokens from the URL
        const { user, tutor } = await refetch(); // Refresh user and tutor data for authcontext
        
        logger.debug("Refetch completed:", {
          user: user ? { id: user.id, name: user.name, email: user.email } : null,
          tutor: tutor ? { id: tutor.id } : null
        });
        
        // Set helper cookies for middleware (similar to manual login)
        if (user?.intends_to_be_tutor && !tutor) {
          document.cookie = `intends_to_be_tutor=${!!user.intends_to_be_tutor}; path=/; SameSite=Lax; Secure`;
          document.cookie = `tutor_profile_complete=${!!tutor}; path=/; SameSite=Lax; Secure`;
          logger.debug("Helper cookies set for middleware");
        }
        
        logger.debug("Navigating to:", redirectTo);
        router.replace(redirectTo, undefined);
      } else {
        setShowLogin(true);
      }
      setChecking(false);
    };

    handleAuthCallback();
  }, [redirectTo, router, searchParams, refetch, authLoading, user, tutor]);

  if (checking) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner" />
      </div>
    );
  }
  return <>{showLogin && <LoginForm redirectTo={redirectTo} />}</>;
}
