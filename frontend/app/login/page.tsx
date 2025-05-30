import { Suspense } from "react";
import LoginPage from "./LoginPage";

export default function page() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <LoginPage />
    </Suspense>
  );
}