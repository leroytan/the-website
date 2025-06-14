"use client";

import { useState } from "react";
import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import { useRouter } from "next/navigation";
import AssignmentCard from "./assignmentCard";
import { Repeat } from "lucide-react";

export default function TutorDashboard({
  assignments,
}: {
  assignments: {
    tutorAssignments: TuitionListing[];
    clientAssignments: TuitionListing[];
  };
}) {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("active");
  const [isTutorView, setIsTutorView] = useState(true);

  const handleChat = async (tutorId: number) => {
    try {
      const response = await fetch(`/api/chat/get-or-create`, {
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
  const filteredAssignments = Array.isArray(assignments.tutorAssignments) || Array.isArray(assignments.clientAssignments)
    ? (isTutorView ? assignments.tutorAssignments : assignments.clientAssignments).filter((a) => {
        if (activeTab === "active") return a.status === "FILLED";
        if (activeTab === "pending") return a.status === "OPEN";
        return false;
      })
    : [];

  return (
    <div className="min-h-screen bg-customLightYellow/50 p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section with Switch Button */}
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-customDarkBlue mb-2">My Dashboard</h1>
            <p className="text-gray-600">Manage your {isTutorView ? "tutoring assignments" : "client requests"} and applications</p>
          </div>
          <Button
            onClick={() => setIsTutorView(!isTutorView)}
            className="flex items-center gap-2 bg-customDarkBlue text-white px-4 py-2 rounded-lg hover:bg-customDarkBlue/90 transition-colors duration-200 shadow-sm"
          >
            <Repeat size={20} />
            <span>Switch to {isTutorView ? "Client" : "Tutor"} View</span>
          </Button>
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-1/4">
            <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm p-6 border border-customLightYellow/60">
              <nav className="space-y-2">
                {["active", "pending"].map((key) => (
                  <button
                    key={key}
                    className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                      activeTab === key
                        ? "bg-customDarkBlue text-white shadow-sm"
                        : "text-customDarkBlue hover:bg-customLightYellow/30"
                    }`}
                    onClick={() => setActiveTab(key)}
                  >
                    {key === "active" ? "Active Assignments" : "Pending Applications"}
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
                    view="tutor"
                    onChat={handleChat}
                    onViewDetails={() => router.push(`/assignments?selected=${assignment.id}`)}
                  />
                ))}
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
