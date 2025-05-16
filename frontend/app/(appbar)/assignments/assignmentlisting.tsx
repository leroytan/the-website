"use client";
import AssignmentCard from "@/components/assignmentCard";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import AddAssignmentOverlay from "@/components/addAssignmentButton";
import Checkbox from "@/components/checkbox";
import Input from "@/components/input";
import { TuitionListing, TuitionListingFilters } from "@/components/types";

const AssignmentListing = ({
  assignmentsArray,
  assignmentsFilter,
}: {
  assignmentsArray: TuitionListing[];
  assignmentsFilter: TuitionListingFilters;
}) => {
  const [listings, setListings] = useState(assignmentsArray);
  const [filters, setFilters] = useState<{
    subjects: { id: string; name: string }[];
    levels: { id: string; name: string }[];
  }>({
    subjects: [],
    levels: [],
  });
  const [sortOption, setSortOption] = useState("new");
  const searchParams = useSearchParams();
  const isAddOpen = searchParams.get("add");
  const router = useRouter();
  const handleFilterChange = (
    type: "subjects" | "levels",
    id: string,
    name: string
  ) => {
    setFilters((prev) => {
      const updatedValues = prev[type].some((item) => item.id === id)
        ? prev[type].filter((item) => item.id !== id)
        : [...prev[type], { id, name: name }];
      return { ...prev, [type]: updatedValues };
    });
  };
  const addListingController = (listing: TuitionListing) => {
    const newListing = listing;
    const now = new Date();
    const toLocalDateTimeString = (date: Date) =>
      `${date.getFullYear()}-${(date.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")} ${date
        .getHours()
        .toString()
        .padStart(2, "0")}:${date
        .getMinutes()
        .toString()
        .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
    newListing.created_at = toLocalDateTimeString(now);
    setListings((prev) => {
      return [...prev, newListing];
    });
  };
  const closeAddAssignmentOverlay = () => {
    const params = new URLSearchParams(searchParams.toString());
    params.delete("add"); // Remove the "add" query parameter
    router.push(`/assignments?${params.toString()}`);
  };

  const sortedListings = [...listings].slice().sort((a, b) => {
    if (sortOption === "price-asc") {
      return (
        Number(a.estimated_rate.slice(0, -5)) -
        Number(b.estimated_rate.slice(0, -5))
      );
    } else if (sortOption === "price-desc") {
      return (
        Number(b.estimated_rate.slice(0, -5)) -
        Number(a.estimated_rate.slice(0, -5))
      );
    }
    return b.id! - a.id!; // Default to newest first
  });
  const filteredListings = sortedListings.filter((listing) => {
    const subjectMatch =
      filters.subjects.length === 0 ||
      listing.subjects.some((subject) =>
        filters.subjects.some((filter) => filter.name === subject)
      );
    const levelMatch =
      filters.levels.length === 0 ||
      listing.levels.some((level) =>
        filters.levels.some((filter) => filter.name === level)
      );
    return subjectMatch && levelMatch;
  });
  return (
    <motion.section>
      <div className="flex flex-col md:flex-row gap-4 p-4 sm:p-6 bg-customLightYellow min-h-screen">
        {/* Sidebar */}
        <div className="w-full md:w-1/4 bg-white p-4 rounded-lg shadow-md md:block">
          <h2 className="font-semibold mb-4">Subjects</h2>
          <div className="space-y-2">
            {assignmentsFilter.subject.map((subject) => (
              <div key={subject.id} className="flex items-center gap-2">
                <Checkbox
                  defaultChecked={filters.subjects.some(
                    (filter) => filter.id === subject.id
                  )}
                  onChange={() =>
                    handleFilterChange("subjects", subject.id, subject.name)
                  }
                >
                  <span className={"text-customDarkBlue"}>{subject.name}</span>
                </Checkbox>
              </div>
            ))}
          </div>

          <h2 className="font-semibold mt-6 mb-4">Level</h2>
          <div className="space-y-2">
            {assignmentsFilter.level.map((level) => (
              <div key={level.id} className="flex items-center gap-2">
                <Checkbox
                  defaultChecked={filters.levels.some(
                    (filter) => filter.id === level.id
                  )}
                  onChange={() =>
                    handleFilterChange("levels", level.id, level.name)
                  }
                >
                  <span className={"text-customDarkBlue"}>{level.name}</span>
                </Checkbox>
              </div>
            ))}
          </div>
        </div>

        <div className="flex-1">
          <div className="flex flex-col sm:flex-row justify-between mb-4 gap-2">
            <Input
              placeholder="Search"
              type={""}
              name={""}
              value={""}
              onChange={function (
                e: React.ChangeEvent<HTMLInputElement>
              ): void {
                throw new Error("Function not implemented.");
              }}
            />
            {isAddOpen && (
              <AddAssignmentOverlay
                filters={assignmentsFilter}
                addListingController={addListingController}
                onClose={closeAddAssignmentOverlay}
              ></AddAssignmentOverlay>
            )}

            <div className="flex gap-2">
              {[
                { label: "New", value: "new" },
                { label: "Price ascending", value: "price-asc" },
                { label: "Price descending", value: "price-desc" },
              ].map(({ label, value }) => (
                <button
                  key={value}
                  className={`px-4 py-2 rounded-lg shadow-md transition-all duration-200 ${
                    sortOption === value
                      ? "bg-orange-400 text-white"
                      : "bg-white"
                  }`}
                  onClick={() => setSortOption(value)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <motion.div
            layout="position"
            transition={{ duration: 1, ease: "easeInOut" }}
            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"
          >
            <AnimatePresence>
              {filteredListings.map((listing) => (
                <motion.div
                  layout
                  key={listing.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                  exit={{ opacity: 0 }}
                >
                  <AssignmentCard {...listing} />
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
};

export default AssignmentListing;
