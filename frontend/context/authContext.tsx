"use client";

import { Tutor, User } from "@/components/types";
import { createContext, useContext, useEffect, useState, useRef, useCallback } from "react";
import { fetchWithTokenCheck } from "../utils/tokenVersionMismatch";

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

  const fetchAuth = async (): Promise<{ user: User | null; tutor: Tutor | null }> => {
    // Prevent concurrent calls
    if (isFetching.current) {
      return { user, tutor };
    }
    
    isFetching.current = true;
    
    try {
      const res = await fetchWithTokenCheck(`/api/me`, {
        credentials: "include",
      });
      if (!res.ok) throw new Error("Not authenticated");
      const data = await res.json();
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
    }
  };
  
  // Fetch user and tutor data on mount - only once
  useEffect(() => {
    if (!hasInitialized.current && !isFetching.current) {
      fetchAuth();
    }
  }, []); // Empty dependency array - only run once on mount

  // Refetch function to manually refresh user and tutor data
  const refetch = useCallback(async (): Promise<{ user: User | null; tutor: Tutor | null }> => {
    setLoading(true); // optional; you could remove this if handled in fetchAuth
    return await fetchAuth();
  }, []); // Empty dependency array since fetchAuth uses refs and doesn't depend on state
  // Logout function to clear user and tutor data
  const logout = async () => {
    setUser(null);
    setTutor(null);
    setLoading(false);
    console.log("User logged out");
  };

  return (
    <AuthContext.Provider value={{ user, tutor, loading, refetch, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
