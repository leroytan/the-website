import { Suspense } from "react";
import PaymentCancel from "./paymentCancelPage";

export default function page() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <PaymentCancel />
    </Suspense>
  );
}