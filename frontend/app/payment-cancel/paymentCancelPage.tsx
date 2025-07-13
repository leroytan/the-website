"use client";

import { AlertTriangle } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/button";

const PaymentCancelPage = () => {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#fff2de] via-[#fabb84]/30 to-[#4a58b5]/10">
      <div className="bg-white/90 rounded-3xl shadow-2xl px-8 py-12 flex flex-col items-center max-w-md w-full">
        <div className="mb-6">
          <AlertTriangle size={72} className="text-[#fc6453] drop-shadow-lg" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#4a58b5] mb-2 text-center">
          Payment Cancelled
        </h1>
        <p className="text-[#4a58b5] mb-8 text-base sm:text-lg text-center">
          Your payment was not completed.
          <br />
          If this was a mistake, you can try again or return to the home page.
        </p>
        <div className="flex gap-3 w-full justify-center">
          <Button
            onClick={() => router.back()}
            className="px-4 py-2 flex items-center bg-white text-customDarkBlue border border-customDarkBlue rounded-full hover:bg-orange-50 transition-colors duration-200 shadow-sm"
          >
            Try Again
          </Button>
          <Link href="/" className="w-36">
            <Button className="px-4 py-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 w-full">
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PaymentCancelPage;
