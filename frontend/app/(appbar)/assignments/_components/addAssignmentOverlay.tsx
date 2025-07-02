"use client";

import { useRef, useState } from "react";
import { Button } from "../../../../components/button";
import DropDown from "../../../../components/dropdown";
import MultiSelectButton from "../../../../components/multiSelectButton";
import { TuitionListingFilters } from "../../../../components/types";
import { Dialog } from "../../../../components/dialog";
import Input from "../../../../components/input";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronLeft, ChevronRight, Plus, X, CheckCircle2 } from "lucide-react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";
import Image from "next/image";

type Direction = "left" | "right";

function formatMinutes(minutesString: string) {
  const minutes = parseInt(minutesString, 10);
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  let result = "";
  if (hours > 0) result += `${hours} hour${hours > 1 ? "s" : ""}`;
  if (hours > 0 && mins > 0) result += " ";
  if (mins > 0) result += `${mins} minutes`;
  return result.trim();
}

const AddAssignmentOverlay = ({
  filters,
}: {
  filters: TuitionListingFilters;
}) => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [showOverlay, setShowOverlay] = useState(true);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    level: "",
    subjects: [] as string[],
    location: "",
    slots: [
      {
        day: "",
        hours: "",
        minutes: "",
        duration: "",
      },
    ],
    fees: "",
    lesson_duration: "",
    special_requests: "",
  });

  const [currentSlot, setCurrentSlot] = useState(0);
  const prevSlotRef = useRef(0);
  const directionRef = useRef<Direction>("right");
  const goToSlot = (newIndex: number) => {
    prevSlotRef.current = currentSlot;
    directionRef.current = newIndex > currentSlot ? "right" : "left";
    setCurrentSlot(newIndex);
  };

  const goToPrevSlot = () => {
    if (formData.slots.length <= 1 || currentSlot === 0) return;
    goToSlot(currentSlot - 1);
  };

  const goToNextSlot = () => {
    if (formData.slots.length <= 1 || currentSlot === formData.slots.length - 1)
      return;
    goToSlot(currentSlot + 1);
  };

  const handleAddSlot = () => {
    const newSlots = [
      ...formData.slots,
      {
        day: "",
        hours: "",
        minutes: "",
        duration: "",
      },
    ];
    setFormData((prev) => ({ ...prev, slots: newSlots }));
    goToSlot(newSlots.length - 1);
  };

  const handleRemoveSlot = () => {
    if (formData.slots.length <= 1) return;
    const newSlotIndex =
      currentSlot === formData.slots.length - 1 ? currentSlot - 1 : currentSlot;
    const newSlots = formData.slots.filter((_, idx) => idx !== currentSlot);
    setFormData((prev) => ({ ...prev, slots: newSlots }));
    goToSlot(newSlotIndex);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Remove ?add from the URL to close overlay
  const handleClose = () => {
    const params = new URLSearchParams(searchParams.toString());
    params.delete("add");
    router.push(`${pathname}?${params.toString()}`);
  };

  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault();
    // Check if fields are filled
    if (
      !formData.level ||
      formData.subjects.length === 0 ||
      !formData.location ||
      !formData.fees ||
      !formData.lesson_duration
    ) {
      alert("Please fill in all main fields.");
      return;
    }

    // Check all slots
    for (const slot of formData.slots) {
      if (
        slot.day === "" ||
        slot.hours === "" ||
        slot.minutes === "" ||
        slot.duration === ""
      ) {
        alert("Please fill in all slot fields.");
        return;
      }
    }

    // Compose available_slots
    const available_slots = formData.slots.map((slot) => {
      const startHour = parseInt(slot.hours, 10);
      const startMinute = parseInt(slot.minutes, 10);
      const [durationHour, durationMinute] = slot.duration
        .split(" ")[0]
        .split(".")
        .map(Number);

      const totalDurationMinutes =
        (durationHour ? durationHour : 0) * 60 + (durationMinute ? 30 : 0);

      const startDate = new Date(0, 0, 0, startHour, startMinute);
      const endDate = new Date(
        startDate.getTime() + totalDurationMinutes * 60000
      );

      const pad = (n: number) => n.toString().padStart(2, "0");

      return {
        day: slot.day,
        start_time: `${pad(startHour)}:${pad(startMinute)}`,
        end_time: `${pad(endDate.getHours())}:${pad(endDate.getMinutes())}`,
      };
    });

    // Compose title if not provided
    const title =
      formData.title || `${formData.level} ${formData.subjects.join(", ")}`;

    const listingToAdd = {
      title,
      estimated_rate_hourly: parseInt(formData.fees, 10),
      lesson_duration: parseInt(formData.lesson_duration, 10),
      weekly_frequency: formData.slots.length,
      available_slots,
      special_requests: formData.special_requests,
      subjects: formData.subjects,
      level: formData.level,
      location: formData.location,
    };

    try {
      const data = await fetchWithTokenCheck(`/api/assignments/new`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(listingToAdd),
        credentials: "include",
      });
      if (!data.ok) {
        throw new Error("Failed to create assignment");
      }
      // Show success dialog after successful creation
      setShowOverlay(false);
      setShowSuccessDialog(true);
    } catch (error) {
      alert(error);
    }
  }

  // Example fee options
  const feeOptions = ["25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100"];

  const locations = [
    "Ang Mo Kio",
    "Bedok North",
    "Bedok South",
    "Bishan",
    "Bukit Batok",
    "Bukit Merah",
    "Bukit Panjang",
    "Bukit Timah",
    "Central Area",
    "Changi",
    "Changi Bay",
    "Choa Chu Kang",
    "Clementi",
    "Geylang",
    "Hougang",
    "Jurong East",
    "Jurong West",
    "Kallang",
    "Lim Chu Kang",
    "Mandai",
    "Marine Parade",
    "Newton",
    "Novena",
    "Orchard",
    "Outram",
    "Pasir Ris",
    "Paya Lebar",
    "Pioneer",
    "Punggol",
    "Queenstown",
    "River Valley",
    "Rochor",
    "Seletar",
    "Sembawang",
    "Sengkang",
    "Serangoon",
    "Simpang",
    "Southern Islands",
    "Straits View",
    "Sungei Kadut",
    "Tampines",
    "Tanglin",
    "Tengah",
    "Thomson",
    "Toa Payoh",
    "Tuas",
    "Western Islands",
    "Western Water Catchment",
    "Woodlands",
    "Yishun",
    "Boon Lay",
    "Ghim Moh",
    "Gul",
    "Kent Ridge",
    "Nanyang",
    "Pasir Laba",
    "Teban Gardens",
    "Toh Tuck",
    "Tuas South",
    "West Coast",
  ];

  return (
    <>
      {showOverlay && (
        <Dialog className="relative">
          <Button
            onClick={handleClose}
            className="absolute top-4 right-4 text-customOrange hover:text-red-700 transition-colors duration-200 z-10"
            aria-label="Close"
          >
            <X size={24} />
          </Button>
          <div>
            <h2 className="text-xl font-semibold mb-4 text-center sm:text-left">
              Add Assignment
            </h2>
          </div>
          <div className="overflow-y-auto max-h-[80vh] p-4">
            <form className="gap-6 flex flex-col" onSubmit={handleSubmit}>
              {/* Level Dropdown */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Level <span className="text-red-500">*</span>
                </h3>
                <DropDown
                  placeholder="- Select One -"
                  stringOnDisplay={formData.level}
                  stateController={(value) => {
                    setFormData({ ...formData, level: value });
                  }}
                  iterable={filters.levels.map((level) => level.name)}
                  className="w-full rounded-md text-sm"
                />
              </div>

              {/* Subjects Multi-Select */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Subjects <span className="text-red-500">*</span>
                </h3>
                <MultiSelectButton
                  options={filters.subjects.map((subject) => subject.name)}
                  selected={formData.subjects}
                  onChange={(selected) =>
                    setFormData({ ...formData, subjects: selected })
                  }
                  placeholder="- Select Multiple -"
                  className="w-full rounded-md text-sm"
                />
              </div>
              {/* Title Field */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Title
                </h3>
                <Input
                  type="text"
                  name="title"
                  placeholder="(optional, auto-generated if left blank)"
                  value={formData.title}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-customYellow"
                />
              </div>
              {/* Location Field */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Location <span className="text-red-500">*</span>
                </h3>
                <DropDown
                  placeholder="- Select One -"
                  stringOnDisplay={formData.location}
                  stateController={(value) => {
                    setFormData({ ...formData, location: value });
                  }}
                  iterable={locations}
                  className="w-full rounded-md text-sm"
                />
              </div>

              {/* Slots Section */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Available Slots <span className="text-red-500">*</span>
                </h3>
                <div className="flex flex-row items-center justify-center">
                  {/* Shift left button (hide if first slot) */}
                  {currentSlot > 0 && (
                    <Button
                      type="button"
                      onClick={goToPrevSlot}
                      className="mr-2 text-customDarkBlue hover:text-customOrange"
                      aria-label="Previous Slot"
                    >
                      <ChevronLeft />
                    </Button>
                  )}

                  <div className="relative w-full min-h-[230px]">
                    <AnimatePresence mode="wait">
                      <motion.div
                        key={`slot-${currentSlot}`}
                        initial={{
                          x: directionRef.current === "right" ? 300 : -300,
                          opacity: 0,
                        }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ duration: 0.3 }}
                        className="w-full"
                      >
                        <div className="w-full gap-4 flex flex-col border-customDarkBlue bg-customLightYellow border-2 rounded-md p-4 shadow">
                          <div className="absolute top-0 right-0 p-4">
                            {formData.slots.length > 1 && (
                              <Button
                                type="button"
                                onClick={handleRemoveSlot}
                                aria-label="Remove Slot"
                                className="text-customOrange"
                              >
                                <X />
                              </Button>
                            )}
                          </div>
                          <span className="text-customDarkBlue text-lg font-semibold mb-2">
                            Slot {currentSlot + 1} / {formData.slots.length}
                          </span>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Day <span className="text-red-500">*</span>
                          </label>
                          <DropDown
                            placeholder="Select Day"
                            stringOnDisplay={formData.slots[currentSlot].day}
                            stateController={(value) => {
                              const newSlots = [...formData.slots];
                              newSlots[currentSlot].day = value;
                              setFormData({ ...formData, slots: newSlots });
                            }}
                            iterable={[
                              "Monday",
                              "Tuesday",
                              "Wednesday",
                              "Thursday",
                              "Friday",
                              "Saturday",
                              "Sunday",
                            ]}
                            className="w-full rounded-md text-sm"
                          />
                          <div className="mt-4">
                            <label className="block text-sm font-medium text-customDarkBlue mb-1">
                              Start Time <span className="text-red-500">*</span>
                            </label>
                            <div className="flex items-center gap-2">
                              <DropDown
                                placeholder="Hour"
                                stringOnDisplay={
                                  formData.slots[currentSlot].hours
                                }
                                iterable={Array.from({ length: 24 }, (_, i) =>
                                  i.toString().padStart(2, "0")
                                )}
                                stateController={(value) => {
                                  const newSlots = [...formData.slots];
                                  newSlots[currentSlot].hours = value;
                                  setFormData({ ...formData, slots: newSlots });
                                }}
                                className="w-full rounded-md text-sm"
                              />
                              <span className="text-customDarkBlue font-medium">
                                :
                              </span>
                              <DropDown
                                placeholder="Minute"
                                stringOnDisplay={
                                  formData.slots[currentSlot].minutes
                                }
                                iterable={Array.from({ length: 60 }, (_, i) =>
                                  i.toString().padStart(2, "0")
                                )}
                                stateController={(value) => {
                                  const newSlots = [...formData.slots];
                                  newSlots[currentSlot].minutes = value;
                                  setFormData({ ...formData, slots: newSlots });
                                }}
                                className="w-full rounded-md text-sm"
                              />
                            </div>
                          </div>
                          <div className="mt-4">
                            <label className="block text-sm font-medium text-customDarkBlue mb-1">
                              Duration <span className="text-red-500">*</span>
                            </label>
                            <DropDown
                              placeholder="Select Duration"
                              stringOnDisplay={
                                formData.slots[currentSlot].duration
                              }
                              iterable={[
                                "1 hour",
                                "1.5 hours",
                                "2 hours",
                                "2.5 hours",
                                "3 hours",
                              ]}
                              stateController={(value) => {
                                const newSlots = [...formData.slots];
                                newSlots[currentSlot].duration = value;
                                setFormData({ ...formData, slots: newSlots });
                              }}
                              className="w-full rounded-md text-sm"
                            />
                          </div>
                        </div>
                      </motion.div>
                    </AnimatePresence>
                  </div>

                  {/* Shift right button (hide if last slot) */}
                  {currentSlot < formData.slots.length - 1 && (
                    <Button
                      type="button"
                      onClick={goToNextSlot}
                      className="ml-2 text-customDarkBlue hover:text-customOrange"
                      aria-label="Next Slot"
                    >
                      <ChevronRight />
                    </Button>
                  )}
                </div>
                <div className="flex justify-end mt-2 space-x-4">
                  <Button
                    type="button"
                    onClick={handleAddSlot}
                    aria-label="Add Slot"
                    className="flex items-center text-customDarkBlue hover:text-customOrange"
                  >
                    <Plus />
                    <span>Add Slot</span>
                  </Button>
                </div>
              </div>

              {/* Fees Dropdown */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Fees <span className="text-red-500">*</span>
                </h3>
                <Image
                  src="/images/rates.png"
                  alt="Fees"
                  width={1000}
                  height={1000}
                  className="w-full"
                />
                <br/>
                <DropDown
                  stringOnDisplay={formData.fees}
                  placeholder="- Select One -"
                  iterable={feeOptions}
                  stateController={(value) =>
                    setFormData({ ...formData, fees: value })
                  }
                  className="w-full rounded-md text-sm"
                />
                
              </div>

              {/* Lesson Duration Field */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  First Lesson Duration <span className="text-red-500">*</span>
                </h3>
                <DropDown
                  placeholder="Select Duration"
                  stringOnDisplay={
                    formData.lesson_duration
                      ? formatMinutes(formData.lesson_duration)
                      : ""
                  }
                  iterable={[30, 60, 90, 120, 150, 180].map((min) => `${min}`)}
                  renderItem={(option) => <span>{formatMinutes(option)}</span>}
                  stateController={(value) =>
                    setFormData({ ...formData, lesson_duration: value })
                  }
                  className="w-full rounded-md text-sm"
                />
              </div>

              {/* Special Requests */}
              <div>
                <h3 className="text-base font-medium text-customDarkBlue mb-2">
                  Special Requests
                </h3>
                <textarea
                  name="special_requests"
                  placeholder="(optional)"
                  value={formData.special_requests}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-customYellow"
                />
              </div>

              {/* Submit and Cancel Buttons */}
              <div className="flex justify-end space-x-2">
                <Button
                  type="button"
                  onClick={handleClose}
                  className="px-4 py-2 bg-gray-200 text-customDarkBlue rounded-md hover:bg-gray-300 transition-colors duration-200"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleSubmit}
                  type="submit"
                  className="px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200"
                >
                  Submit
                </Button>
              </div>
            </form>
          </div>
        </Dialog>
      )}

      {/* Success Dialog */}
      {showSuccessDialog && (
        <Dialog
          variant="success"
          title="Assignment Created!"
          message="Your assignment has been successfully created. You can now view it in your dashboard."
        >
          <div className="flex gap-3">
            <Button
              onClick={() => {
                setShowSuccessDialog(false);
                handleClose();
              }}
              className="px-4 py-2 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors duration-200"
            >
              Close
            </Button>
            <Button
              onClick={() => {
                setShowSuccessDialog(false);
                handleClose();
                router.push("/dashboard");
              }}
              className="px-4 py-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200"
            >
              Go to Dashboard
            </Button>
          </div>
        </Dialog>
      )}
    </>
  );
};
export default AddAssignmentOverlay;
