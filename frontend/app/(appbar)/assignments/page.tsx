"use client";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

const tuitionListings = [
  {
    id: 1,
    time: "FRI 07:00 PM",
    title: "Sec 2 Express Science",
    location: "15 Flora Drive 506854",
    duration: "1.5h",
    price: "$30-45/h",
    averagePrice: 35,
    status: "apply",
    level: "Secondary",
    subject: "Science",
  },
  {
    id: 2,
    time: "SUN 02:00 PM",
    title: "P3 English",
    location: "1 Lorong 5 Toa Payoh 319458",
    duration: "1.5h",
    price: "$25-35/h",
    averagePrice: 30,
    status: "apply",
    level: "Primary",
    subject: "English",
  },
  {
    id: 3,
    time: "WED 09:00 PM",
    title: "P5 Science",
    location: "231 Bishan Street 23 570231",
    duration: "2h",
    price: "$30-40/h",
    averagePrice: 35,
    status: "applied",
    level: "Primary",
    subject: "Science",
  },
  {
    id: 4,
    time: "FRI 07:00 PM",
    title: "Sec 2 Math",
    location: "662C Jurong West Street 64 643662",
    duration: "1.5h",
    price: "$30-45/h",
    averagePrice: 35,
    status: "applied",
    level: "Secondary",
    subject: "Mathematics",
  },
  {
    id: 5,
    time: "MON 06:00 PM",
    title: "Sec 3 Higher Chinese",
    location: "12B Marsiling Lane 732012",
    duration: "2h",
    price: "$30-45/h",
    averagePrice: 35,
    status: "apply",
    level: "Secondary",
    subject: "Chinese",
  },
  {
    id: 6,
    time: "FRI 06:00 PM",
    title: "P2 Chinese",
    location: "",
    duration: "1.5h",
    price: "$25-35/h",
    averagePrice: 30,
    status: "apply",
    level: "Primary",
    subject: "Chinese",
  },
  {
    id: 7,
    time: "SAT 07:00 PM",
    title: "P5 Science",
    location: "32 Cassia Crescent 390032",
    duration: "1.5h",
    price: "$30-40/h",
    averagePrice: 35,
    status: "apply",
    level: "Primary",
    subject: "Science",
  },
  {
    id: 8,
    time: "FRI 08:00 PM",
    title: "P3 English",
    location: "31 Jalan Sempadan 457403",
    duration: "2h",
    price: "$25-35/h",
    averagePrice: 30,
    status: "apply",
    level: "Primary",
    subject: "English",
  },
];

function Checkbox({
  defaultChecked,
  className,
  children,
  onChange,
}: {
  defaultChecked: boolean;
  className?: string;
  children?: React.ReactNode;
  onChange?: () => void;
}) {
  return (
    <motion.label
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`flex items-center gap-2 cursor-pointer ${className}`}
    >
      <input
        type="checkbox"
        defaultChecked={defaultChecked}
        className={`${className} accent-customYellow w-5 h-5 rounded-full`}
        onChange={onChange}
      />
      <span>{children}</span>
    </motion.label>
  );
}

function Input({ placeholder }: { placeholder: string }) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      className="w-full sm:w-1/3 p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#fabb84]"
    />
  );
}

function Button({
  children,
  className,
  onClick,
}: {
  children: React.ReactNode;
  className: string;
  onClick: () => void;
}) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`px-4 py-2 rounded-lg shadow-md ${className}`}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}

function Card({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`p-4 rounded-lg shadow-md bg-white duration-300 transform hover:-translate-y-1 ${className}`}
    >
      {children}
    </div>
  );
}

export default function TuitionListings() {
  const [filters, setFilters] = useState({
    subjects: ["English", "Mathematics", "Science", "Chinese"],
    levels: ["Primary", "Secondary"],
  });
  const [sortOption, setSortOption] = useState("new");
  const handleFilterChange = (type: "subjects" | "levels", value: string) => {
    setFilters((prev) => {
      const updatedValues = prev[type].includes(value)
        ? prev[type].filter((item) => item !== value)
        : [...prev[type], value];
      return { ...prev, [type]: updatedValues };
    });
  };
  const sortedListings = [...tuitionListings].sort((a, b) => {
    if (sortOption === "price-asc") {
      return a.averagePrice - b.averagePrice;
    } else if (sortOption === "price-desc") {
      return b.averagePrice - a.averagePrice;
    }
    return b.id - a.id; // Default to newest first
  });
  const filteredListings = sortedListings.filter(
    (listing) =>
      filters.subjects.includes(listing.subject) &&
      filters.levels.includes(listing.level)
  );
  return (
    <motion.section>
      <div className="flex flex-col md:flex-row gap-4 p-4 sm:p-6 bg-customLightYellow min-h-screen">
        {/* Sidebar */}
        <div className="w-full md:w-1/4 bg-white p-4 rounded-lg shadow-md md:block">
          <h2 className="font-semibold mb-4">Subjects</h2>
          <div className="space-y-2">
            {["English", "Mathematics", "Science", "Chinese"].map((subject) => (
              <div key={subject} className="flex items-center gap-2">
                <Checkbox
                  defaultChecked={filters.subjects.includes(subject)}
                  onChange={() => handleFilterChange("subjects", subject)}
                >
                  <span className={"text-customDarkBlue"}>{subject}</span>
                </Checkbox>
              </div>
            ))}
          </div>

          <h2 className="font-semibold mt-6 mb-4">Level</h2>
          <div className="space-y-2">
            {["Primary", "Secondary", "Junior College", "University/Poly"].map(
              (level) => (
                <div key={level} className="flex items-center gap-2">
                  <Checkbox
                    defaultChecked={filters.levels.includes(level)}
                    onChange={() => handleFilterChange("levels", level)}
                  >
                    <span className={"text-customDarkBlue"}>{level}</span>
                  </Checkbox>
                </div>
              )
            )}
          </div>
        </div>

        <div className="flex-1">
          <div className="flex flex-col sm:flex-row justify-between mb-4 gap-2">
            <Input placeholder="Search" />
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
                  <Card key={listing.id}>
                    <div className="text-xs bg-black text-white px-2 py-1 inline-block rounded-md mb-2">
                      {listing.time}
                    </div>
                    <h3 className="text-blue-600 font-semibold">
                      {listing.title}
                    </h3>
                    <p className="text-sm text-gray-600">{listing.location}</p>
                    <p className="text-sm">{listing.duration}</p>
                    <p className="text-sm font-semibold">{listing.price}</p>
                    <Button
                      className={
                        listing.status === "applied"
                          ? "bg-orange-400 text-white mt-2"
                          : "bg-customDarkBlue text-white mt-2"
                      }
                      onClick={function (): void {
                        throw new Error("Function not implemented.");
                      }}
                    >
                      {listing.status === "applied" ? "Applied" : "Apply"}
                    </Button>
                  </Card>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}
