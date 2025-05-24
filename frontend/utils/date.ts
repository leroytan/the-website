// This file contains utility functions for formatting dates and times.


/**
 * Returns a human-readable string representing how much time has passed since the given date.
 *
 * Examples:
 *   - "5 minutes ago"
 *   - "2 hours ago"
 *   - "1 day ago"
 *   - "more than 30 days ago"
 *
 * @param dateString - The date to compare to now (as a string or Date object)
 * @returns A string describing the elapsed time in minutes, hours, days, or "more than 30 days ago"
 */
export function timeAgo(dateString: string | Date): string {
  const createdAt = new Date(dateString);
  const now = new Date();
  const diffInMs = now.getTime() - createdAt.getTime();
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  if (diffInMinutes == 0) {
    return "now";
  } else if (diffInHours < 1) {
    return `${diffInMinutes} minute${diffInMinutes === 1 ? "" : "s"} ago`;
  } else if (diffInHours < 2) {
    return `1 hour ago`;
  } else if (diffInHours < 24) {
    return `${diffInHours} hours ago`;
  } else if (diffInDays <= 30) {
    return `${diffInDays} day${diffInDays === 1 ? "" : "s"} ago`;
  } else {
    return "more than 30 days ago";
  }
}


export function to12HourTime(input: string): string {
  // Parse the input date string into a Date object
  const date = new Date(input.replace(/\.(\d{3})\d+$/, ".$1"));
  if (isNaN(date.getTime())) throw new Error("Invalid date");

  // Get the timezone offset (in minutes) and adjust the UTC time
  const localOffset = date.getTimezoneOffset(); // Local timezone offset in minutes
  const localDate = new Date(date.getTime() - localOffset * 60000); // Adjust UTC by local timezone offset

  // Extract hours, minutes, seconds
  const [h, m, s] = [
    localDate.getHours(),
    localDate.getMinutes(),
    localDate.getSeconds(),
  ];
  const hour12 = h % 12 || 12;
  const ampm = h < 12 ? "AM" : "PM";

  // Return the formatted time
  return `${hour12}:${m.toString().padStart(2, "0")}:${s
    .toString()
    .padStart(2, "0")} ${ampm}`;
}