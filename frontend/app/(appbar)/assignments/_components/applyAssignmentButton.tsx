"use client";
import { useEffect, useState } from "react";
import { Button } from "../../../../components/button";

const ApplyAssignmentButton = ({ assignmentId, AppliedStatus, status }: { assignmentId: number, AppliedStatus: boolean, status: "OPEN" | "FILLED" }) => {
  const [isApplied, setIsApplied] = useState<boolean>(AppliedStatus);
  const [isFilled, setIsFilled] = useState<boolean>(status === "FILLED");
  useEffect(() => {
    setIsApplied(AppliedStatus);
  }, [AppliedStatus]);

  useEffect(() => {
    setIsFilled(status === "FILLED");
  }, [status]);
  async function handleSubmit() {
    !isApplied && setIsApplied((x) => !x);
    try {
      const data = await fetch(`/api/assignments/${assignmentId}/request`, {
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
      {isFilled ? "Filled" : isApplied ? "Applied" : "Apply"}
    </Button>
  );
};

export default ApplyAssignmentButton;
