import { useState } from "react";
import { Button } from "./button";
import { TuitionListing } from "./types";

const AssignmentCard = (listing: TuitionListing, className: string) => {
  const [isApplied, setIsApplied] = useState(listing.status === "applied");
  return (
    <div
      className={`p-4 rounded-lg shadow-md bg-white duration-300 transform hover:-translate-y-1 ${className}`}
    >
      <div className="text-xs bg-black text-white px-2 py-1 inline-block rounded-md mb-2">
        {listing.time}
      </div>
      <h3 className="text-blue-600 font-semibold">{listing.title}</h3>
      <p className="text-sm text-gray-600">{listing.location}</p>
      <p className="text-sm text-gray-600">{listing.duration}</p>
      <p className="text-sm font-semibold text-gray-600">{listing.price}</p>
      <Button
        className={
          listing.status === "disabled"
            ? "bg-gray-300 text-gray-500 mt-2"
            : isApplied === true
            ? "bg-orange-400 text-white mt-2"
            : "bg-customDarkBlue text-white mt-2"
        }
        onClick={() => {
          listing.status!= "disabled" && setIsApplied((x) => !x);
        }}
      >
        {isApplied === true ? "Applied" : "Apply"}
      </Button>
    </div>
  );
};

export default AssignmentCard;
