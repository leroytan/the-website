"use client";
import { useEffect, useState } from "react";
import { Button } from "../../../../components/button";
import { useAuth } from "../../../../context/authContext";

const ApplyAssignmentButton = ({ assignmentId, appliedStatus, status }: { assignmentId: number, appliedStatus: boolean, status: "OPEN" | "FILLED" }) => {
  const [isApplied, setIsApplied] = useState<boolean>(appliedStatus);
  const [isFilled, setIsFilled] = useState<boolean>(status === "FILLED");
  useEffect(() => {
    setIsApplied(appliedStatus);
  }, [appliedStatus]);

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
        body: JSON.stringify({ available_slots: [] }),
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

  const {tutor } = useAuth();

  return (
    tutor? (
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
    ) : null
  );
};

export default ApplyAssignmentButton;
