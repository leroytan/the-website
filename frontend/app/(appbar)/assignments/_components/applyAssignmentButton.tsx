"use client";
import { useEffect, useState } from "react";
import { Button } from "../../../../components/button";
import { useAuth } from "../../../../context/authContext";
import { TutorRequestDialog } from "./tutorRequestDialog";
import { Dialog } from "../../../../components/dialog";
import { useRouter } from "next/navigation";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";

interface TimeSlot {
  day: string;
  start_time: string;
  end_time: string;
}

const ApplyAssignmentButton = ({ 
  assignmentId, 
  appliedStatus, 
  status,
  availableSlots 
}: { 
  assignmentId: number, 
  appliedStatus: boolean, 
  status: "OPEN" | "FILLED",
  availableSlots: TimeSlot[]
}) => {
  const [isApplied, setIsApplied] = useState<boolean>(appliedStatus);
  const [isFilled, setIsFilled] = useState<boolean>(status === "FILLED");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setIsApplied(appliedStatus);
  }, [appliedStatus]);

  useEffect(() => {
    setIsFilled(status === "FILLED");
  }, [status]);

  async function handleSubmit(data: { requested_rate_hourly: number; available_slots: TimeSlot[] }) {
    !isApplied && setIsApplied((x) => !x);
    try {
      const res = await fetchWithTokenCheck(`/api/assignment-requests/new`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          assignment_id: assignmentId,
          requested_rate_hourly: data.requested_rate_hourly,
          available_slots: data.available_slots,
        }),
        credentials: "include",
      });
      const json = await res.json();
      if (!res.ok) throw new Error(`Failed to apply for the assignment: ${json.message}`);
      setShowSuccessDialog(true);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setIsApplied((x) => !x);
        alert(error.message);
        return;
      }
    }
  }

  const { tutor } = useAuth();

  return (
    tutor ? (
      <>
        <Button
          disabled={isApplied || isFilled}
          className={`${
            isApplied || isFilled
              ? "bg-gray-300 text-gray-500 mt-2 cursor-not-allowed "
              : "px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200"
          } rounded-md px-4 py-2`}
          onClick={() => setIsDialogOpen(true)}
        >
          {isFilled ? "Filled" : isApplied ? "Applied" : "Apply"}
        </Button>
        <TutorRequestDialog
          isOpen={isDialogOpen}
          onClose={() => setIsDialogOpen(false)}
          onSubmit={handleSubmit}
          clientSlots={availableSlots}
        />

        {/* Success Dialog */}
        {showSuccessDialog && (
          <Dialog
            variant="success"
            title="Application Submitted!"
            message="Your application has been successfully submitted. The client will review your application and get back to you soon."
          >
            <div className="flex gap-3">
              <Button
                onClick={() => setShowSuccessDialog(false)}
                className="px-4 py-2 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors duration-200"
              >
                Close
              </Button>
              <Button
                onClick={() => {
                  setShowSuccessDialog(false);
                  router.push('/dashboard');
                }}
                className="px-4 py-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200"
              >
                Go to Dashboard
              </Button>
            </div>
          </Dialog>
        )}
      </>
    ) : null
  );
};

export default ApplyAssignmentButton;
