import { Suspense } from "react";
import ForgotPasswordForm from "../ForgotPasswordForm";

export default function ForgotPasswordPage() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <ForgotPasswordForm />
    </Suspense>
  );
}