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
    id?: number;
    day: string;
    start_time: string;
    end_time: string;
  }[];
  special_requests: string;
  subjects: string[];
  levels: string[];
  status?: "OPEN" | "FILLED";
}
export interface TuitionListingFilters {
  course: {
    text: string;
    id: string;
  }[];
  subject: {
    name: string;
    id: string;
  }[];
  level: {
    name: string;
    id: string;
  }[];
}