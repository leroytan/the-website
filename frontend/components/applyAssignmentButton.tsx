"use client";
import { useState } from "react";
import { Button } from "./button";
import { TuitionListing } from "./types";

const ApplyAssignmentButton = ({ listing }: { listing: TuitionListing }) => {
  const [isApplied, setIsApplied] = useState<boolean>(listing.applied!);
  const isFilled = listing.status === "FILLED"
  async function handleSubmit() {
    !isApplied && setIsApplied((x) => !x);
    try {
      const data = await fetch(`/api/assignments/${listing.id}/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      const res = await data.json();
      if (!data.ok) throw new Error(`Failed to apply for the assignment: ${res.message}`);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setIsApplied((x) => !x);
        alert(error.message);
        return;
      }
    }
  }

  return (
    <Button
      disabled={isApplied || isFilled}
      className={`${
        isApplied || isFilled
          ? "bg-gray-300 text-gray-500 mt-2 cursor-not-allowed "
          : "px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200"
      } rounded-md px-4 py-2`}
      onClick={() => {
        handleSubmit();
      }}
    >
      {isFilled === true ? "Filled" : isApplied === true ? "Applied" : "Apply"}
    </Button>
  );
};

export default ApplyAssignmentButton;
