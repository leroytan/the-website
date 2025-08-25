import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import { UserImage } from "@/components/userImage";
import { timeAgo } from "@/utils/date";
import { ChevronDown, ChevronUp, Clock, ExternalLink, Hourglass, MessageCircle, X } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

export default function AppliedTutorsModal({
  requests,
  onClose,
  onAccept,
  onChat,
  onProfile,
}: {
  requests: TuitionListing["requests"];
  onClose: () => void;
  onAccept: (requestId: number, hourlyRateCents: number, tutorId: number, chatId?: number) => void;
  onChat: (tutorId: number) => void;
  onProfile: (tutorId: number) => void;
}) {
  const [expandedTutors, setExpandedTutors] = useState<number[]>([]);

  const toggleExpand = (tutorId: number) => {
    setExpandedTutors(prev => 
      prev.includes(tutorId) 
        ? prev.filter(id => id !== tutorId)
        : [...prev, tutorId]
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-xl md:mx-0 mx-4 rounded-lg shadow-lg relative max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center px-4 md:px-6 py-4 border-b sticky top-0 bg-white">
          <h2 className="text-lg md:text-xl font-bold text-customDarkBlue">
            Applied Tutors
          </h2>
          <button
            onClick={onClose}
            className="text-customOrange hover:text-red-700 transition-colors duration-200"
          >
            <X size={20} />
          </button>
        </div>

        {/* Request List */}
        <div className="p-4 space-y-4">
          {!requests || requests.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No tutors have applied yet.
            </div>
          ) : (
            requests?.map((request) => (
              <div
                key={request.id}
                className="flex flex-col gap-4 p-4 border rounded-lg shadow-sm relative"
              >
                {request.requested_rate_hourly && (
                  <div className="absolute top-4 right-4 text-green-600 bg-green-100 font-bold px-3 py-1 rounded-lg">
                    ${request.requested_rate_hourly}/hour
                  </div>
                )}
                {/* Tutor Info */}
                <div className="flex items-center gap-3">
                  <div className="flex-[30%]">
                    <UserImage user={{ photo_url: request.tutor_profile_photo_url, name: request.tutor_name, gender: request.tutor_gender }} />
                  </div>
                  <div className="flex-[70%]">
                    <p className="font-semibold text-customDarkBlue">
                      {request.tutor_name}
                    </p>
                    <p className="text-xs text-gray-500">
                      applied {timeAgo(request.created_at)}
                    </p>
                  </div>
                </div>

                {/* Available Slots */}
                <div className="space-y-2">
                  <h3 className="text-sm font-medium text-customDarkBlue">
                    Available Slots
                  </h3>
                  {request.available_slots && request.available_slots.length > 0 ? (
                    <div className="space-y-2">
                      {(expandedTutors.includes(request.tutor_id) 
                        ? request.available_slots 
                        : request.available_slots.slice(0, 3)
                      ).map((slot, index) => {
                        const start = slot.start_time;
                        const end = slot.end_time;
                        const [sh, sm] = start.split(":").map(Number);
                        const [eh, em] = end.split(":").map(Number);
                        const durationHours = eh + em / 60 - sh - sm / 60;

                        return (
                          <div
                            key={`slot-${index}-${slot.day}-${start}-${end}`}
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
                      {request.available_slots.length > 3 && (
                        <button
                          onClick={() => toggleExpand(request.tutor_id)}
                          className="w-full text-center text-sm text-customDarkBlue hover:text-customOrange transition-colors duration-200 flex items-center justify-center gap-1"
                        >
                          {expandedTutors.includes(request.tutor_id) ? (
                            <>
                              Show Less <ChevronUp size={16} />
                            </>
                          ) : (
                            <>
                              +{request.available_slots.length - 3} More Slots <ChevronDown size={16} />
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  ) : (
                    <div className="text-sm text-gray-500 italic bg-gray-50 px-4 py-2 rounded-xl">
                      This tutor has not indicated any available slots yet.
                    </div>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-2 justify-end">
                  <Button
                    className="px-3 py-2 flex justify-center items-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm whitespace-nowrap"
                    onClick={() => onAccept(request.id, 3500, request.tutor_id)}
                  >
                    Accept
                  </Button>
                  <Button
                    className="px-3 py-2 flex justify-center items-center bg-white border border-orange-400 text-orange-400 text-sm rounded-full"
                    onClick={() => onChat(request.tutor_id)}
                  >
                    Chat
                    <MessageCircle className="ml-1" size={16} />
                  </Button>
                  <Button
                    className="px-3 py-2 flex justify-center items-center bg-white border border-orange-400 text-orange-400 text-sm rounded-full"
                    onClick={() => onProfile(request.tutor_id)}
                  >
                    Profile
                    <ExternalLink className="ml-2" size={16} />
                  </Button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
