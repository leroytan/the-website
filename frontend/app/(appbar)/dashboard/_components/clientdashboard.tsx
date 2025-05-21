"use client";

import { useState } from "react";
import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import AppliedTutorsModal from "./appliedTutorsModal";
import { ExternalLink } from "lucide-react";

export default function ClientDashboard({
  assignments,
}: {
  assignments: TuitionListing[];
}) {
  const [selectedRequests, setSelectedRequests] = useState<
    TuitionListing["requests"] | null
  >(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("active");

  const openApplicantsModal = (requests: TuitionListing["requests"]) => {
    setSelectedRequests(requests);
    setModalOpen(true);
  };

  const filteredAssignments = Array.isArray(assignments)
    ? assignments.filter((a) => {
        if (activeTab === "active") return a.request_status === "ACCEPTED";
        if (activeTab === "pending") return a.request_status === "PENDING";
        return false;
      })
    : [];

  // Handler for accepting a tutor request
  const handleAccept = async (requestId: number) => {
    try {
      const res = await fetch(
        `/api/assignment-requests/${requestId}/change-status?status=ACCEPTED`,
        { method: "PUT", credentials: "include" }
      );
      if (!res.ok) throw new Error("Failed to accept request");
      // Optionally, update UI or refetch assignments here
      alert("Tutor accepted!");
      setModalOpen(false);
    } catch (err) {
      alert("Failed to accept tutor. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF3E9] flex flex-col md:flex-row p-6 gap-4">
      <aside className="md:w-1/4 w-full md:pr-6">
        <h2 className="text-2xl font-bold text-customDarkBlue mb-6">
          My Dashboard
        </h2>
        <nav className="flex md:flex-col flex-row gap-2 overflow-x-auto whitespace-nowrap">
          {["active", "pending"].map((key) => (
            <button
              key={key}
              className={`text-left px-4 py-2 rounded-md font-medium transition-all duration-200 ${
                activeTab === key
                  ? "bg-customDarkBlue text-white"
                  : "text-customDarkBlue hover:underline"
              }`}
              onClick={() => setActiveTab(key)}
            >
              {key === "active" ? "Active Assignments" : "Pending Assignments"}
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
          {assignments.length === 0 ? (
            <div className="text-gray-500 text-center py-8">
              No assignments found.
            </div>
          ) : (
            assignments.map((assignment) => (
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
                <div className="flex md:flex-col flex-row gap-2 md:col-span-1">
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
