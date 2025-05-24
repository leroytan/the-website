import { Button } from "@/components/button";
import { TuitionListing } from "@/components/types";
import { timeAgo } from "@/utils/date";
import { ExternalLink, MessageCircle, X } from "lucide-react";
import Image from "next/image";

export default function AppliedTutorsModal({
  requests,
  onClose,
  onAccept,
  onChat,
  onProfile,
}: {
  requests: TuitionListing["requests"];
  onClose: () => void;
  onAccept: (requestId: number, priceId: string) => void;
  onChat: (tutorId: number) => void;
  onProfile: (tutorId: number) => void;
}) {
  // Helper to compute "applied X days ago"

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-xl md:mx-0 mx-4 rounded-lg shadow-lg relative">
        {/* Header */}
        <div className="flex justify-between items-center px-4 md:px-6 py-4 border-b">
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
        <div className="px-4 md:px-6 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          {!requests || requests.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No tutors have applied yet.
            </div>
          ) : (
            requests?.map((request) => (
              <div
                key={request.id}
                className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 p-3 border rounded-lg shadow-sm"
              >
                <div className="flex items-center gap-3">
                  {/* Tutor Profile Photo */}
                  <Image
                    src={
                      request.tutor_profile_photo_url || "/default-avatar.png"
                    }
                    alt={request.tutor_name}
                    width={40}
                    height={40}
                    className="w-10 h-10 rounded-full"
                  />
                  <div>
                    <p className="font-semibold text-blue-800">
                      {request.tutor_name}
                    </p>
                    <p className="text-xs text-gray-500">
                      applied {timeAgo(request.created_at)}
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row md:items-center gap-2 md:ml-auto">
                  <Button
                    className="px-3 py-2 flex justify-center items-center bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200 text-sm whitespace-nowrap"
                    onClick={() => onAccept(request.id, "")}
                  >
                    Accept & Pay
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
