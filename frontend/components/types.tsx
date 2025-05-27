export interface TuitionListing {
  id?: number;
  created_at?: string;
  updated_at?: string;
  title: string;
  location: string;
  owner_id?: number;
  applied?: boolean;
  estimated_rate: string;
  weekly_frequency: number;
  available_slots: {
    id: number;
    day: string;
    start_time: string;
    end_time: string;
  }[];
  special_requests: string;
  subjects: string[];
  level: string;
  status?: "OPEN" | "FILLED";
  request_status?: string;
  requests?: {
    id: number;
    tutor_id: number;
    tutor_name: string;
    tutor_profile_photo_url?: string;
    status: string;
    created_at: string;
    updated_at: string;
  }[];
}
export interface TuitionListingFilters {
  courses: {
    text: string;
    id: string;
  }[];
  subjects: {
    name: string;
    id: string;
  }[];
  levels: {
    name: string;
    id: string;
  }[];
}