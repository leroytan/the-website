"use client";

import { useState } from "react";
import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import AppliedTutorsModal from "./appliedTutorsModal";
import { ExternalLink } from "lucide-react";
import { loadStripe } from "@stripe/stripe-js";
import { createCheckoutSession } from "@/app/pricing/createCheckoutSession";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function ClientDashboard({
  assignments,
}: {
  assignments: TuitionListing[];
}) {
  const router = useRouter();
  const [selectedRequests, setSelectedRequests] = useState<
    TuitionListing["requests"] | null
  >(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("open");

  const openApplicantsModal = (requests: TuitionListing["requests"]) => {
    setSelectedRequests(requests);
    setModalOpen(true);
  };

  const filteredAssignments = Array.isArray(assignments)
    ? assignments.filter((a) => {
        if (activeTab === "filled") return a.status === "FILLED";
        if (activeTab === "open") return a.status === "OPEN";
        return false;
      })
    : [];
  const priceId = process.env.NEXT_PUBLIC_STRIPE_PRICE_ID!;
  const handleAccept = async (requestId: number) => {
    try {
      //Call the backend to create a checkout session
      const session: { id: string; url: string } = await createCheckoutSession({
        mode: "payment",
        price_id: priceId,
        success_url: window.location.origin + "/payment-success",
        cancel_url: window.location.origin + "/payment-cancel",
      });

      router.push(session.url);
    } catch (err) {
      console.error("Stripe error:", err);
      alert(err);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF3E9] flex flex-col md:flex-row p-6 gap-4">
      <aside className="md:w-1/4 w-full md:pr-6">
        <h2 className="text-2xl font-bold text-customDarkBlue mb-6">
          My Dashboard
        </h2>
        <nav className="flex md:flex-col flex-row gap-2 overflow-x-auto whitespace-nowrap">
          {["open", "filled"].map((key) => (
            <button
              key={key}
              className={`text-left px-4 py-2 rounded-md font-medium transition-all duration-200 ${
                activeTab === key
                  ? "bg-customDarkBlue text-white"
                  : "text-customDarkBlue hover:underline"
              }`}
              onClick={() => setActiveTab(key)}
            >
              {key === "open" ? "Open Assignments" : "Filled Assignments"}
            </button>
          ))}
        </nav>
      </aside>

      <section className="md:w-3/4 w-full">
        {/* Desktop header */}
        <div className="hidden md:grid grid-cols-5 bg-customDarkBlue text-white font-semibold rounded-t-xl p-4 text-sm">
          <div>Level and Subject</div>
          <div>Tuition Address</div>
          <div>Rate</div>
          <div>Schedule</div>
          <div>Actions</div>
        </div>
        <div className="space-y-4 bg-white rounded-b-xl p-4">
          {filteredAssignments.length === 0 ? (
            <div className="text-gray-500 text-center py-8">
              No assignments found.
            </div>
          ) : (
            filteredAssignments.map((assignment) => (
              <div
                key={assignment.id}
                className="md:grid md:grid-cols-5 flex flex-col gap-4 bg-orange-50 p-4 rounded-xl text-customDarkBlue text-sm"
              >
                {/* Level and Subject */}
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Level & Subject:
                  </span>
                  {assignment.subjects.join(", ")}
                  <br />
                  {assignment.level}
                </div>
                {/* Tuition Address */}
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Tuition Address:
                  </span>
                  {assignment.location}
                </div>
                {/* Rate */}
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">Rate:</span>
                  {assignment.estimated_rate}
                </div>
                {/* Schedule */}
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Schedule:
                  </span>
                  {assignment.available_slots
                    .slice(0, 5)
                    .map((slot: TuitionListing["available_slots"][number]) => (
                      <div key={slot.id}>
                        {slot.day} {slot.start_time}-{slot.end_time}
                      </div>
                    ))}
                  {assignment.available_slots.length > 5 && (
                    <div className="text-customDarkBlue font-semibold">
                      +{assignment.available_slots.length - 5} More
                    </div>
                  )}
                </div>
                {/* Actions */}
                <div className="flex md:flex-col flex-row gap-2 md:col-span-1 items-center">
                  {assignment.status === "OPEN" ? (
                    <OpenAssignmentActions
                      assignment={assignment}
                      openApplicantsModal={openApplicantsModal}
                    />
                  ) : (
                    <FilledAssignmentActions assignment={assignment} />
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </section>

      {modalOpen && selectedRequests && (
        <AppliedTutorsModal
          requests={selectedRequests}
          onClose={() => setModalOpen(false)}
          onAccept={handleAccept}
          onChat={(id) => console.log("Chat", id)}
          onProfile={(id) => console.log("Profile", id)}
        />
      )}
    </div>
  );
}

// Show Applicants and Open for open assignments
function OpenAssignmentActions({
  assignment,
  openApplicantsModal,
}: {
  assignment: TuitionListing;
  openApplicantsModal: (requests: TuitionListing["requests"]) => void;
}) {
  return (
    <>
      <Button
        className="px-4 py-2 flex justify-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm w-full"
        onClick={() => openApplicantsModal(assignment.requests)}
      >
        Applicants
      </Button>
      <Button
        className="px-4 py-2 flex justify-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm w-full"
        onClick={function (): void {
          throw new Error("Function not implemented.");
        }}
      >
        Open
        <ExternalLink className="ml-2" size={16} color="white" />
      </Button>
    </>
  );
}

// Show Tutor and Chat for filled assignments
function FilledAssignmentActions({ assignment }: { assignment: TuitionListing }) {
  // Find the accepted tutor's name from requests
  const acceptedTutor = assignment.requests?.find(
    (r) => r.status === "ACCEPTED"
  );
  return (
    <>
      <div className="flex flex-row justify-center items-center gap-2">
        <Image
          src={
            acceptedTutor?.tutor_profile_photo_url ||
            "/default-avatar.png"
          }
          alt={acceptedTutor?.tutor_name || "Not Assigned"}
          width={40}
          height={40}
          className="rounded-full"
        />
        <span>{acceptedTutor?.tutor_name || "Not Assigned"}</span>
      </div>
      <Button
        className="px-4 py-2 flex justify-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm w-full"
        onClick={() => {
          throw new Error("Function not implemented.");
        }}
      >
        Chat
      </Button>
    </>
  );
}