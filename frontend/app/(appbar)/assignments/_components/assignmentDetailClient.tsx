"use client";
import ApplyAssignmentButton from "@/app/(appbar)/assignments/_components/applyAssignmentButton";
import { TuitionListing } from "@/components/types";
import { timeAgo } from "@/utils/date";
import { Book, CalendarDays, Clock, Hourglass, MapPin } from "lucide-react";

export function AssignmentDetailClient({
  assignment,
}: {
  assignment: TuitionListing;
}) {
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-start">
        <h2 className="text-2xl font-bold text-[#2b2b2b]">
          {assignment.title}
        </h2>
        <div className="text-green-600 bg-green-100 font-bold px-3 py-1 rounded-lg">
          {assignment.estimated_rate_hourly}
        </div>
      </div>
      <div className="text-sm text-gray-500">
        Posted {timeAgo(assignment.created_at!)}
      </div>

      <div className="flex items-center text-customDarkBlue">
        <MapPin size={20} className="mr-1" />
        <span className="font-semibold">{assignment.location}</span>
      </div>

      <div className="flex items-center text-customDarkBlue">
        <Book size={20} className="mr-1" />
        <span className="font-semibold">
          {assignment.subjects?.join(", ")} / {assignment.level}
        </span>
      </div>

      {/* Apply Button */}
      <div className="mt-4">

        <ApplyAssignmentButton assignmentId={assignment.id!} appliedStatus={assignment.applied!} status={assignment.status!}/>
      </div>

      {/* Special Request */}
      <div className="mt-4">
        <h4 className="text-customDarkBlue font-bold mb-1">Special Request</h4>
        <div className="border rounded-md p-3 min-h-[80px]">
          {assignment.special_requests || "No special requests provided."}
        </div>
      </div>

      {/* Available Slots */}
      <div className="mt-4 space-y-3">
        {assignment.available_slots?.map((slot) => {
          const start = slot.start_time;
          const end = slot.end_time;
          const [sh, sm] = start.split(":").map(Number);
          const [eh, em] = end.split(":").map(Number);
          const durationHours = eh + em / 60 - sh - sm / 60;

          return (
            <div
              key={slot.id}
              className="flex justify-between items-center bg-customLightYellow px-4 py-2 rounded-xl"
            >
              <span className="font-bold text-customDarkBlue">{slot.day}</span>
              <div className="flex flex-col items-end text-customDarkBlue text-sm">
                <div className="flex items-center gap-1">
                  <Clock size={14} /> {start} - {end}
                </div>
                <div className="flex items-center gap-1">
                  <Hourglass size={14} /> {durationHours.toFixed(1)} hours
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
