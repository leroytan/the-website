export interface TuitionListing {
  id?: number;
  created_at?: string;
  updated_at?: string;
  title: string;
  location: string;
  owner_id?: number;
  applied?: boolean;
  estimated_rate_hourly: number;
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
    available_slots: {
      day: string;
      start_time: string;
      end_time: string;
    }[];
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

export interface User {
  id: number;
  name: string;
  email: string;
  profile_photo_url: string;
  intends_to_be_tutor: boolean;
  created_at: string;
  updated_at: string;
}
export interface Tutor {
  id: number;
  name: string;
  email: string;
  photo_url: string;
  highest_education: string;
  rate: number;
  location: string;
  rating: number;
  about_me: string;
  subjects_teachable: string[];
  levels_teachable: string[];
  special_skills: string[];
  resume_url: string;
  experience: string;
  availability: string;
}