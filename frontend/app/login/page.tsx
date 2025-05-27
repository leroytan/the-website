"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import LoginForm from "./LoginForm";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirectTo") || "/";
  const [showLogin, setShowLogin] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const tryRefresh = async () => {
      try {
        const res = await fetch("/api/auth/refresh", {
          method: "POST",
          credentials: "include", // 🔥 crucial for cookie-based tokens
        });

        if (res.ok) {
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
  }, [redirectTo, router]);

  if (checking) {
    return (
    <div className="flex justify-center items-center h-screen">
      <div className="spinner" /> {/* your custom loader */}
    </div>
    );
  }
  return <>{showLogin && <LoginForm redirectTo={redirectTo} />}</>;
}
