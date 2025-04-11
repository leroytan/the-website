import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import SignupForm from "./SignupForm";

export const dynamic = 'force-dynamic';
export default function SignupPage() {

  return (
    <div>
      <SignupForm />
    </div>
  );
}
