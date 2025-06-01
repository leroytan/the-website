import { Suspense } from "react";
import PaymentSuccess from "./paymentSuccessPage";

export default function page() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <PaymentSuccess />
    </Suspense>
  );
}