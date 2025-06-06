"use client";

import { useRef, useState } from "react";
import { Button } from "../../../../components/button";
import DropDown from "../../../../components/dropdown";
import MultiSelectButton from "../../../../components/multiSelectButton";
import Image from "next/image";
import { TuitionListingFilters } from "../../../../components/types";
import { Dialog } from "../../../../components/dialog";
import Input from "../../../../components/input";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronLeft, ChevronRight, Plus, Minus } from "lucide-react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

type Direction = "left" | "right";

const AddAssignmentOverlay = ({
  filters,
}: {
  filters: TuitionListingFilters;
}) => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

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
    console.log(directionRef.current);
  };

  const goToNextSlot = () => {
    if (formData.slots.length <= 1 || currentSlot === formData.slots.length - 1)
      return;
    goToSlot(currentSlot + 1);
    console.log(directionRef.current);
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
      formData.level === "Select Level" ||
      formData.subjects.length === 0 ||
      !formData.location ||
      !formData.fees
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
      estimated_rate_hourly: `$${formData.fees}/hour`,
      weekly_frequency: formData.slots.length,
      available_slots,
      special_requests: formData.special_requests,
      subjects: formData.subjects,
      level: formData.level,
      location: formData.location,
    };

    try {
      const data = await fetch("/api/assignments/new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(listingToAdd),
      });
      if (!data.ok) {
        throw new Error("Failed to create assignment");
      }
      // Close overlay after successful add
      handleClose();
    } catch (error) {
      console.log(error);
      alert(error);
    }
  }

  // Example fee options
  const feeOptions = ["25", "30", "35", "40", "45"];

  return (
    <Dialog>
      <div className="overflow-y-auto max-h-[80vh] overflow-x-hidden p-2">
        <h2 className="text-xl font-semibold mb-4">Add Assignment</h2>
        <form className="gap-4 flex flex-col" onSubmit={handleSubmit}>
          <Input
            type="text"
            name="title"
            placeholder="Title (optional, auto-generated if left blank)"
            value={formData.title}
            onChange={handleChange}
          />
          <DropDown
            placeholder="Select Level"
            stringOnDisplay={formData.level}
            stateController={(value) =>
              setFormData({ ...formData, level: value })
            }
            iterable={filters.levels.map((level) => level.name)}
          />
          <MultiSelectButton
            options={filters.subjects.map((subject) => subject.name)}
            selected={formData.subjects}
            onChange={(selected) =>
              setFormData({ ...formData, subjects: selected })
            }
            placeholder="Select Subjects"
          />
          <Input
            type="text"
            name="location"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
            required
          />
          <div className="flex flex-row items-center justify-center">
            {/* Shift left button (hide if first slot) */}
            {currentSlot > 0 && (
              <Button
                type="button"
                onClick={goToPrevSlot}
                className="mr-2"
                aria-label="Previous Slot"
              >
                <ChevronLeft />
              </Button>
            )}

            <div className="relative w-full min-h-[230px]">
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={`slot-${currentSlot}-${formData.slots[currentSlot].day}`}
                  initial={{
                    x: directionRef.current === "right" ? 300 : -300,
                    opacity: 0,
                  }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  className="absolute top-0 left-0 w-full"
                >
                  <div className="w-full gap-4 flex flex-col border-customDarkBlue bg-customLightYellow border-2 rounded-md p-3 shadow">
                    <span className="text-customDarkBlue text-lg font-semibold mb-2">
                      Slot {currentSlot + 1} / {formData.slots.length}
                    </span>
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
                    />
                    <div className="flex flex-row space-x-4 items-center w-full">
                      <DropDown
                        placeholder="Hour"
                        stringOnDisplay={formData.slots[currentSlot].hours}
                        iterable={Array.from({ length: 24 }, (_, i) =>
                          i.toString().padStart(2, "0")
                        )}
                        stateController={(value) => {
                          const newSlots = [...formData.slots];
                          newSlots[currentSlot].hours = value;
                          setFormData({ ...formData, slots: newSlots });
                        }}
                      />
                      <p>:</p>
                      <DropDown
                        placeholder="Minute"
                        stringOnDisplay={formData.slots[currentSlot].minutes}
                        iterable={Array.from({ length: 60 }, (_, i) =>
                          i.toString().padStart(2, "0")
                        )}
                        stateController={(value) => {
                          const newSlots = [...formData.slots];
                          newSlots[currentSlot].minutes = value;
                          setFormData({ ...formData, slots: newSlots });
                        }}
                      />
                    </div>
                    <DropDown
                      placeholder="Duration"
                      stringOnDisplay={formData.slots[currentSlot].duration}
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
                    />
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>

            {/* Shift right button (hide if last slot) */}
            {currentSlot < formData.slots.length - 1 && (
              <Button
                type="button"
                onClick={goToNextSlot}
                className="ml-2"
                aria-label="Next Slot"
              >
                <ChevronRight />
              </Button>
            )}
          </div>
          {/* Add/Remove icons centered below slot card */}
          <div className="flex justify-center mt-2 space-x-4">
            {formData.slots.length > 1 && (
              <Button
                type="button"
                onClick={handleRemoveSlot}
                aria-label="Remove Slot"
              >
                <Minus />
              </Button>
            )}
            <Button type="button" onClick={handleAddSlot} aria-label="Add Slot">
              <Plus />
            </Button>
          </div>
          <DropDown
            stringOnDisplay={formData.fees || "Select Fees"}
            iterable={feeOptions}
            stateController={(value) =>
              setFormData({ ...formData, fees: value })
            }
          />
          <textarea
            name="special_requests"
            placeholder="Special requests (optional)"
            value={formData.special_requests}
            onChange={handleChange}
            className={`w-full border px-3 py-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84]`}
          />
          <div className="flex justify-center space-x-2">
            <Image
              src="/images/rates.png"
              alt="THE Logo"
              width={600}
              height={600}
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              onClick={handleClose}
              className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
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
  );
};
export default AddAssignmentOverlay;
