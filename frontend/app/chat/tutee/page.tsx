import { Suspense } from "react";
import ChatApp from "./ChatApp";

export default function page() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <ChatApp />
    </Suspense>
  );
}