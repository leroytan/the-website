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

  type tokensWrapper = {
    access_token: string;
    refresh_token: string;
    access_cookie_params: cookieParams;
    refresh_cookie_params: cookieParams;
  }

  type cookieParams = {
    domain: string;
    path: string;
    httponly: boolean;
    secure: boolean;
    samesite: 'strict' | 'lax' | 'none';
  }

  useEffect(() => {
    logger.debug("LoginPage: useEffect triggered", {
      authLoading,
      hasUser: !!user,
      hasTutor: !!tutor,
      redirectTo,
      timestamp: new Date().toISOString()
    });

    // Decode tokens from the single query parameter
    const encodedTokens = searchParams.get("tokens");

    const handleAuthCallback = async () => {
      if (encodedTokens) {
        const decodedTokens: tokensWrapper = (()=>{
          try {
            // Add padding back for base64 decoding
            const paddingLength = 4 - (encodedTokens.length % 4);
            const paddedTokens = paddingLength > 0
              ? encodedTokens + '='.repeat(paddingLength)
              : encodedTokens;
            
            return JSON.parse(
              Buffer.from(paddedTokens, 'base64').toString('utf-8')
            );

          } catch (error) {
            logger.error("Failed to decode tokens", error);
            return {};
          }
        })();

        const accessToken: string = decodedTokens.access_token;
        const refreshToken: string = decodedTokens.refresh_token;
        const accessCookieParams: cookieParams = decodedTokens.access_cookie_params;
        const refreshCookieParams: cookieParams = decodedTokens.refresh_cookie_params;
        logger.debug(accessToken);
        logger.debug(refreshToken);
        logger.debug(accessCookieParams);
        logger.debug(refreshCookieParams);

        // HttpOnly; Max-Age=7200; Path=/; SameSite=strict; Secure
        const params2Str = (params: cookieParams): string => {
          return [
            params.domain && `Domain=${params.domain}`,
            params.path && `Path=${params.path}`,
            params.httponly && `HttpOnly`,
            params.secure && `Secure`,
            params.samesite && `SameSite=${params.samesite}`
          ]
            .filter(Boolean)     // removes falsy values (e.g., false or empty strings)
            .join('; ');
        };
        
        const accessCookieString = params2Str(accessCookieParams);
        const refreshCookieString = params2Str(refreshCookieParams);

        logger.debug(accessCookieString);
        logger.debug(refreshCookieString);

        document.cookie = `access_token=${accessToken}; ${accessCookieString}`;
        document.cookie = `refresh_token=${refreshToken}; ${refreshCookieString}`;

        await new Promise(r => setTimeout(r, 50));
        
        // Clear the tokens from the URL
        const { user, tutor } = await refetch(); // Refresh user and tutor data for authcontext
        
        logger.debug("LoginPage: Refetch completed:", {
          user: user ? { id: user.id, name: user.name, email: user.email } : null,
          tutor: tutor ? { id: tutor.id } : null
        });
        
        // Set helper cookies for middleware (similar to manual login)
        if (user?.intends_to_be_tutor && !tutor) {
          document.cookie = `intends_to_be_tutor=${!!user.intends_to_be_tutor}; path=/; SameSite=Lax; Secure`;
          document.cookie = `tutor_profile_complete=${!!tutor}; path=/; SameSite=Lax; Secure`;
        }
        
        router.replace(redirectTo, undefined);
      } else {
        setShowLogin(true);
      }
      setChecking(false);
    };

    handleAuthCallback();
  }, [redirectTo, searchParams]);

  if (checking) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner" />
      </div>
    );
  }
  return <>{showLogin && <LoginForm redirectTo={redirectTo} />}</>;
}
