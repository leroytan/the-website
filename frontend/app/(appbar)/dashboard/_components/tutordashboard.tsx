"use client";

import { useState } from "react";
import SkeletonAssignments from "./skeletonAssignments";
import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import { ExternalLink, MessageCircleMore } from "lucide-react";

export default function TutorDashboardPage({
  assignments,
}: {
  assignments: TuitionListing[];
}) {
  const [activeTab, setActiveTab] = useState("active");

  const filteredAssignments = Array.isArray(assignments)
    ? assignments.filter((a) => {
        if (activeTab === "active") return a.request_status === "ACCEPTED";
        if (activeTab === "pending") return a.request_status === "PENDING";
        return false;
      })
    : [];

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
        <div className="hidden md:grid grid-cols-5 bg-customDarkBlue text-white font-semibold rounded-t-xl p-4 text-sm">
          <div>Title</div>
          <div>Level and Subject</div>
          <div>Tuition Address</div>
          <div>Schedule</div>
          <div>Actions</div>
        </div>

        <div className="space-y-4 bg-white rounded-b-xl p-4">
          {!assignments ? (
            <SkeletonAssignments />
          ) : filteredAssignments.length === 0 ? (
            <p className="text-sm text-gray-600">No assignments found.</p>
          ) : (
            filteredAssignments.map((item) => (
              <div
                key={item.id}
                className="md:grid md:grid-cols-5 flex flex-col gap-4 bg-orange-50 p-4 rounded-xl text-customDarkBlue font-medium text-sm shadow-sm"
              >
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">Title:</span>
                  {item.title}
                </div>
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Level & Subject:
                  </span>
                  {item.level} {item.subjects.join(", ")}
                </div>
                <div className="whitespace-pre-line md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Address:
                  </span>
                  {item.location}
                </div>
                <div className="md:col-span-1">
                  <span className="block md:hidden font-semibold">
                    Schedule:
                  </span>
                  {item.available_slots.slice(0, 5).map((slot) => (
                    <div key={slot.id}>
                      {slot.day} {slot.start_time}-{slot.end_time}
                    </div>
                  ))}
                  {item.available_slots.length > 5 && (
                    <div className="text-customDarkBlue font-semibold">
                      +{item.available_slots.length - 5} More
                    </div>
                  )}
                </div>
                <div className="flex md:flex-col flex-row gap-2 md:col-span-1">
                  <Button
                    className="px-4 py-2 flex justify-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm w-full"
                    onClick={function (): void {
                      throw new Error("Function not implemented.");
                    }}
                  >
                    Chat
                    <MessageCircleMore
                      className="ml-2"
                      size={16}
                      color="white"
                    />
                  </Button>
                  <Button
                    className="px-4 py-2 flex justify-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm w-full"
                    onClick={function (): void {
                      throw new Error("Function not implemented.");
                    }}
                  >
                    Open
                    <ExternalLink
                      className="ml-2"
                      size={16}
                      color="white"
                    />
                  </Button>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
