"use client";

import { Tutor, User } from "@/components/types";
import { createContext, useContext, useEffect, useState, useRef, useCallback } from "react";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatch";
import logger from "@/utils/logger";

interface AuthContextType {
  user: User | null;
  tutor: Tutor | null;
  loading: boolean;
  refetch: () => Promise<{ user: User | null; tutor: Tutor | null }>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  tutor: null,
  loading: true,
  refetch: async () => ({ user: null, tutor: null }),
  logout: () => {},
});


export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [tutor, setTutor] = useState<Tutor | null>(null);
  const [loading, setLoading] = useState(true);
  const hasInitialized = useRef(false);
  const isFetching = useRef(false);
  const currentFetchPromise = useRef<Promise<{ user: User | null; tutor: Tutor | null }> | null>(null);

  const fetchAuth = async (): Promise<{ user: User | null; tutor: Tutor | null }> => {
    // If already fetching, wait for the current fetch to complete
    if (isFetching.current && currentFetchPromise.current) {
      return await currentFetchPromise.current;
    }
    
    isFetching.current = true;
    
    // Create and store the fetch promise
    const fetchPromise = (async () => {
      setLoading(true);
      
      try {
        const refreshRes = await fetch(`/api/auth/refresh`, {
          method: "POST",
          credentials: "include",
        });
        if (!refreshRes.ok) throw new Error("Not authenticated");
        const res = await fetchWithTokenCheck(`/api/me`, {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Not authenticated");
        const data = await res.json();
        
        logger.debug("AuthContext: fetchAuth successful, setting user state:", {
          user: data.user ? { id: data.user.id, name: data.user.name, email: data.user.email } : null,
          tutor: data.tutor ? { id: data.tutor.id } : null,
          timestamp: new Date().toISOString()
        });
        
        setUser(data.user);
        setTutor(data.tutor);
        return { user: data.user, tutor: data.tutor };
      } catch (err) {
        setUser(null);
        setTutor(null);
        return { user: null, tutor: null };
      } finally {
        setLoading(false);
        hasInitialized.current = true;
        isFetching.current = false;
        currentFetchPromise.current = null;
      }
    })();
    
    currentFetchPromise.current = fetchPromise;
    return await fetchPromise;
  };
  
  // Fetch user and tutor data on mount - only once
  useEffect(() => {
    if (!hasInitialized.current && !isFetching.current) {
      fetchAuth();
    }
  }, []); // Empty dependency array - only run once on mount

  // Refetch function to manually refresh user and tutor data
  const refetch = useCallback(async (): Promise<{ user: User | null; tutor: Tutor | null }> => {
    return await fetchAuth();
  }, []); // Empty dependency array since fetchAuth uses refs and doesn't depend on state
  // Logout function to clear user and tutor data
  const logout = () => {
    setUser(null);
    setTutor(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider value={{ user, tutor, loading, refetch, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
