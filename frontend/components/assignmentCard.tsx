import { Calendar, Hourglass, MapPin, MapPinHouse } from "lucide-react";
import ApplyAssignmentButton from "../app/(appbar)/assignments/_components/applyAssignmentButton";
import { TuitionListing } from "./types";

const AssignmentCard = (listing: TuitionListing) => {
  return (
    <div
      className={`p-4 rounded-lg shadow-md bg-white duration-300 transform hover:-translate-y-1 min-h-52 max-h-screen flex flex-col justify-between`}
    >
      <div>
        <h3 className="text-blue-600 font-semibold max-h-12 overflow-hidden">{listing.title}</h3>
        <div className="flex flex-col gap-2 mt-2">
          <div className="flex flex-row text-sm text-gray-600 items-center gap-1 max-h-8 overflow-hidden">
            <MapPinHouse size={20} />
            {listing.location}
          </div>
          <div className="flex flex-row text-sm text-gray-600 overflow-hidden items-center gap-1 max-h-8">
            <Calendar size={20} />
            {listing.available_slots
              .flatMap((slot) => [slot.day, ", "])
              .slice(0, -1)}
          </div>
          <div className="flex flex-row text-sm text-gray-600 items-center gap-1 max-h-8 overflow-hidden">
            <Hourglass size={20} />
            {Array.from(
              new Set(
                listing.available_slots.flatMap((slot) => [
                  `${(
                    (new Date().setHours(
                      Number(slot.end_time.split(":")[0]),
                      Number(slot.end_time.split(":")[1])
                    ) -
                      new Date().setHours(
                        Number(slot.start_time.split(":")[0]),
                        Number(slot.start_time.split(":")[1])
                      )) /
                    3600000
                  ).toFixed(1)} hours`,
                ])
              )
            ).join(", ")}
          </div>
        </div>
      </div>
      <div className="mt-2">
        <p className="text-sm font-semibold text-gray-600">
          {listing.estimated_rate}
        </p>
        <div className="text-xs text-gray-600 flex flex-row justify-between items-end">
          <span>
            posted&nbsp;
            {(() => {
              const createdAt = new Date(listing.created_at!);
              const now = new Date();
              const diffInMs = now.getTime() - createdAt.getTime();
              const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
              const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
              const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
              if (diffInHours < 1) {
                return `${diffInMinutes} minutes ago`;
              } else if (diffInHours < 2) {
                return `${diffInHours} hour ago`;
              } else if (diffInHours < 24) {
                return `${diffInHours} hours ago`;
              } else if (diffInDays <= 30) {
                return `${diffInDays} days ago`;
              } else {
                return "more than 30 days ago";
              }
            })()}
          </span>
          <ApplyAssignmentButton
          assignmentId={listing.id || 1}
          appliedStatus={listing.request_status != `NOT_SUBMITTED` }
          status={listing.status || `OPEN`} />
        </div>
      </div>
    </div>
  );
};

export default AssignmentCard;
