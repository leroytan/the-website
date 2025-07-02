"use client";

import { createCheckoutSession } from "@/app/pricing/createCheckoutSession";
import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import { loadStripe } from "@stripe/stripe-js";
import { ExternalLink, MessageCircleMore } from "lucide-react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";
import AppliedTutorsModal from "./appliedTutorsModal";
import AssignmentCard from "./assignmentCard";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";

export default function ClientDashboard({
  assignments,
}: {
  assignments: {
    tutorAssignments: TuitionListing[];
    clientAssignments: TuitionListing[];
  };
}) {
  const router = useRouter();
  const [selectedRequests, setSelectedRequests] = useState<TuitionListing["requests"]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("open");

  const openApplicantsModal = async (assignment: TuitionListing) => {
    const response = await fetchWithTokenCheck(`/api/assignments/${assignment.id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch assignment details");
    }
    const updatedAssignment: TuitionListing = await response.json();
    setSelectedRequests(updatedAssignment.requests || []);
    setModalOpen(true);
  };

  const handleAccept = async (requestId: number, hourlyRateCents: number, tutorId: number, chatId?: number) => {
    try {
      //Call the backend to create a checkout session
      const session: { id: string; url: string } = await createCheckoutSession({
        mode: "payment",
        success_url: window.location.origin + "/payment-success",
        cancel_url: window.location.origin + "/payment-cancel",
        assignment_request_id: requestId,
        tutor_id: tutorId,
        chat_id: chatId
      });

      router.push(session.url);
    } catch (err) {
      console.error("Stripe error:", err);
      alert(err);
    }
  };

  const handleChat = async (tutorId: number) => {
    try {
      const response = await fetchWithTokenCheck(`/api/chat/get-or-create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ other_user_id: tutorId }),
        credentials: "include",
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(`Failed to create chat: ${error.message}`);
      }

      const chatPreview = await response.json();
      router.push(`/chat?chatId=${chatPreview.id}`);
    } catch (error) {
      console.error("Error creating chat:", error);
    }
  };

  const filteredAssignments = Array.isArray(assignments.clientAssignments)
    ? assignments.clientAssignments.filter((a) => {
        if (activeTab === "filled") return a.status === "FILLED";
        if (activeTab === "open") return a.status === "OPEN";
        return false;
      })
    : [];
  // const priceId = process.env.NEXT_PUBLIC_STRIPE_PRICE_ID!;

  return (
    <div className="min-h-screen bg-customLightYellow/50 p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-customDarkBlue mb-2">My Dashboard</h1>
          <p className="text-gray-600">Manage your tuition assignments and tutor applications</p>
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-1/4">
            <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm p-6 border border-customLightYellow/60">
              <nav className="space-y-2">
                {["open", "filled"].map((key) => (
                  <button
                    key={key}
                    className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                      activeTab === key
                        ? "bg-customDarkBlue text-white shadow-sm"
                        : "text-customDarkBlue hover:bg-customLightYellow/30"
                    }`}
                    onClick={() => setActiveTab(key)}
                  >
                    {key === "open" ? "Open Assignments" : "Filled Assignments"}
                  </button>
                ))}
              </nav>
            </div>
          </aside>

          {/* Assignments List */}
          <section className="lg:w-3/4">
            {filteredAssignments.length === 0 ? (
              <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm p-8 text-center border border-customLightYellow/60">
                <p className="text-gray-500 mb-4">No assignments found</p>
                <p className="text-sm text-gray-400">Your {activeTab} assignments will appear here</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6">
                {filteredAssignments.map((assignment) => (
                  <AssignmentCard
                    key={assignment.id}
                    assignment={assignment}
                    view="client"
                    onChat={handleChat}
                    onViewApplicants={openApplicantsModal}
                    onViewDetails={() =>
                      router.push(`/assignments?selected=${assignment.id}`)
                    }
                  />
                ))}
              </div>
            )}
          </section>
        </div>
      </div>

      {modalOpen && (
        <AppliedTutorsModal
          requests={selectedRequests}
          onClose={() => setModalOpen(false)}
          onAccept={handleAccept}
          onChat={handleChat}
          onProfile={(id) => router.push(`/tutors/${id}`)}
        />
      )}
    </div>
  );
}