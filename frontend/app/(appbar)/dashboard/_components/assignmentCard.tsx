'use client'

import { TuitionListing } from "@/components/types"
import { Button } from "@/components/button"
import { ExternalLink, MessageCircleMore } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"

interface AssignmentCardProps {
  assignment: TuitionListing
  view: 'tutor' | 'client'
  onChat?: (id: number) => void
  onViewDetails?: (id: number) => void
  onViewApplicants?: (assignment: TuitionListing) => void
}

export default function AssignmentCard({
  assignment,
  view,
  onChat,
  onViewDetails,
  onViewApplicants
}: AssignmentCardProps) {
  const router = useRouter()

  return (
    <div className="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200">
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-start mb-4">
          <div>
            <div className="flex flex-wrap gap-2 mb-2">
              <span className="px-3 py-1 bg-orange-100 text-customDarkBlue rounded-full text-sm">
                {assignment.level}
              </span>
              {assignment.subjects.map((subject) => (
                <span key={subject} className="px-3 py-1 bg-orange-100 text-customDarkBlue rounded-full text-sm">
                  {subject}
                </span>
              ))}
            </div>
            <h3 className="text-lg font-semibold text-customDarkBlue">
              {assignment.title}
            </h3>
          </div>
          <div className="flex gap-2">
            {view === 'client' && assignment.status === "OPEN" && (
              <Button
                className="px-4 py-2 flex items-center bg-customYellow text-white rounded-xl hover:bg-customOrange transition-colors duration-200 text-sm shadow-sm"
                onClick={() => onViewApplicants?.(assignment)}
              >
                <MessageCircleMore className="mr-2" size={16} />
                View Applicants
              </Button>
            )}
            {view === 'client' && assignment.status === "FILLED" && (
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 px-4 py-2 bg-orange-50 rounded-xl">
                  <Image
                    src={assignment.requests?.find(r => r.status === "ACCEPTED")?.tutor_profile_photo_url || "/default-avatar.png"}
                    alt={assignment.requests?.find(r => r.status === "ACCEPTED")?.tutor_name || "Not Assigned"}
                    width={32}
                    height={32}
                    className="rounded-full"
                  />
                  <span className="text-customDarkBlue font-medium">
                    {assignment.requests?.find(r => r.status === "ACCEPTED")?.tutor_name || "Not Assigned"}
                  </span>
                </div>
                <Button
                  className="px-4 py-2 flex items-center bg-customYellow text-white rounded-xl hover:bg-customOrange transition-colors duration-200 text-sm shadow-sm"
                  onClick={() => onChat?.(assignment.requests?.find(r => r.status === "ACCEPTED")?.tutor_id || 0)}
                >
                  <MessageCircleMore className="mr-2" size={16} />
                  Chat
                </Button>
              </div>
            )}
            {view === 'tutor' && (
              <div className="flex gap-2">
                <Button
                  className="px-4 py-2 flex items-center bg-customYellow text-white rounded-xl hover:bg-customOrange transition-colors duration-200 text-sm shadow-sm"
                  onClick={() => onChat && assignment.owner_id && onChat(assignment.owner_id)}
                >
                  <MessageCircleMore className="mr-2" size={16} />
                  Chat
                </Button>
                <Button
                  className="px-4 py-2 flex items-center bg-white text-customDarkBlue border border-customDarkBlue rounded-xl hover:bg-orange-50 transition-colors duration-200 text-sm shadow-sm"
                  onClick={() => onViewDetails && assignment.id && onViewDetails(assignment.id)}
                >
                  <ExternalLink className="mr-2" size={16} />
                  View Details
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Details */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* Location */}
          <div className="flex items-start gap-3">
            <div className="p-2 bg-orange-50 rounded-lg">
              <svg className="w-5 h-5 text-customDarkBlue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">Location</h4>
              <p className="text-customDarkBlue">{assignment.location}</p>
            </div>
          </div>

          {/* Rate */}
          <div className="flex items-start gap-3">
            <div className="p-2 bg-orange-50 rounded-lg">
              <svg className="w-5 h-5 text-customDarkBlue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">Rate</h4>
              <p className="text-customDarkBlue font-medium">
                ${assignment.estimated_rate_hourly ? assignment.estimated_rate_hourly : 0}/hr
              </p>
            </div>
          </div>

          {/* Schedule */}
          <div className="flex items-start gap-3">
            <div className="p-2 bg-orange-50 rounded-lg">
              <svg className="w-5 h-5 text-customDarkBlue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">Schedule</h4>
              <div className="space-y-1">
                {assignment.available_slots.slice(0, 3).map((slot) => (
                  <div key={slot.id} className="text-sm text-customDarkBlue">
                    {slot.day} {slot.start_time}-{slot.end_time}
                  </div>
                ))}
                {assignment.available_slots.length > 3 && (
                  <div className="text-customDarkBlue text-sm font-medium">
                    +{assignment.available_slots.length - 3} More
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 