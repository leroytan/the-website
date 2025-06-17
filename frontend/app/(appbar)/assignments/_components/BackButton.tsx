"use client";

import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/button";
import { useRouter } from "next/navigation";

const BackButton = () => {
  const router = useRouter();

  const handleBack = () => {
    if (document.referrer.includes("/assignments")) {
      // If the user came from the assignments page, go back to that page
      router.back();
    } else {
      // Otherwise, redirect to the assignments page
      router.push("/assignments");
    }
  };

  return (
    <Button
      onClick={handleBack}
      className="flex items-center gap-2 text-customDarkBlue font-semibold hover:text-customOrange transition-colors"
    >
      <ArrowLeft size={20} />
      Back to List
    </Button>
  );
};

export default BackButton;