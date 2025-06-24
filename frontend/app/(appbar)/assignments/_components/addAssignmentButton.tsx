"use client";
import { Plus } from "lucide-react";
import { Button } from "../../../../components/button";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

const AddAssignmentButton = () => {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const searchParams = new URLSearchParams(params?.toString() || "");

  function handleOpenOverlay(): void {
    const params = new URLSearchParams(searchParams.toString());
    params.set("add", "true");
    router.push(`/assignments?${params.toString()}`);
  }

  return (
    <Button
      onClick={handleOpenOverlay}
      className="flex flex-row items-center bg-customOrange rounded-sm p-2 text-white text-sm"
    >
      <Plus />
      Assignment
    </Button>
  );
};

export default AddAssignmentButton;