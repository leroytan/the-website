import { Suspense } from "react";
import ResetPasswordForm from "../ResetPasswordForm";

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="spinner" /></div>}>
      <ResetPasswordForm />
    </Suspense>
  );
}