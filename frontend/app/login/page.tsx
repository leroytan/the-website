import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import LoginForm from "@/app/login/LoginForm";

export const dynamic = 'force-dynamic';

export default function LoginPage() {

  return (
    <div>
      <LoginForm />
    </div>
  );
}