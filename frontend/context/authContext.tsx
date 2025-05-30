"use client";

import { Tutor, User } from "@/components/types";
import { createContext, useContext, useEffect, useState } from "react";

interface AuthContextType {
  user: User | null;
  tutor: Tutor | null;
  loading: boolean;
  refetch: () => void;
  logout: () => void;
}
const AuthContext = createContext<AuthContextType>({
  user: null,
  tutor: null,
  loading: true,
  refetch: () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [tutor, setTutor] = useState<Tutor | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAuth = async () => {
    try {
      const res = await fetch("/api/me", {
        credentials: "include",
      });
      if (!res.ok) throw new Error("Not authenticated");
      const data = await res.json();
      setUser(data.user);
      setTutor(data.tutor);
    } catch (err) {
      setUser(null);
      setTutor(null);
    } finally {
      setLoading(false);
    }
  };
  // Fetch user and tutor data on mount
  useEffect(() => {
    fetchAuth();
  }, []);

  // Refetch function to manually refresh user and tutor data
  const refetch = async () => {
    setLoading(true);
    await fetchAuth();
    console.log(user, tutor);
  };
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
