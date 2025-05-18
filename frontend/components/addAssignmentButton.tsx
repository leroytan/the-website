import { useState } from "react";
import { Button } from "./button";
import DropDown from "./dropdown";
import Image from "next/image";
import { TuitionListing, TuitionListingFilters } from "./types";
import { Dialog } from "./dialog";
import Input from "./input";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function AddAssignmentOverlay({
  filters,
  addListingController,
  onClose,
}: {
  filters: TuitionListingFilters;
  addListingController: (listing: TuitionListing) => void;
  onClose: () => void;
}) {
  const router = useRouter()
  const [formData, setFormData] = useState({
    level: "Select Level",
    subject: "Select Subject",
    location: "",
    slots: [
      {
        day: "Select Day",
        hours: "Hour",
        minutes: "Minute",
        duration: "1 hour",
      },
    ],

    fees: "",
  });
  const [currentSlot, setCurrentSlot] = useState(0);
  const goToPrevSlot = () => setCurrentSlot((prev) => Math.max(prev - 1, 0));
  const goToNextSlot = () =>
    setCurrentSlot((prev) => Math.min(prev + 1, formData.slots.length - 1));
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  async function handleSubmit(): Promise<void> {
    //check if fields are filled
    if (
      formData.level === "Select Level" ||
      formData.subject === "Select Subject" ||
      !formData.location ||
      !formData.fees
    ) {
      alert("Please fill in all main fields.");
      return;
    }

    // Check all slots
    for (const slot of formData.slots) {
      if (
        slot.day === "Select Day" ||
        slot.hours === "Hour" ||
        slot.minutes === "Minute" ||
        slot.duration === ""
      ) {
        alert("Please fill in all slot fields.");
        return;
      }
    }
    onClose();
    const listingToAdd: TuitionListing = {
      title: formData.level + " " + formData.subject,
      estimated_rate: "$" + formData.fees + "/hour",
      weekly_frequency: formData.slots.length,
      available_slots: formData.slots.map((slot) => {
        // Parse start time
        const startHour = parseInt(slot.hours, 10);
        const startMinute = parseInt(slot.minutes, 10);
        const [durationHour, durationMinute] = slot.duration
          .split(" ")
          .shift()!
          .split(".")
          .map(Number);

        // Calculate duration in minutes
        const totalDurationMinutes = (durationHour ? durationHour : 0) * 60 +
          (durationMinute ? durationMinute * 6 : 0);

        // Calculate end time
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
      }),
      special_requests: "",
      subjects: [formData.subject],
      levels: [formData.level],
      location: formData.location
    };
    console.log(listingToAdd)
    addListingController(listingToAdd);
    try {
      const data = await fetch("/api/assignments/new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(listingToAdd),
      })
      if (!data.ok) {
        throw new Error("Failed to create assignment");
      }
    } catch (error) {
        console.log(error)
        alert(error)
    }
  }

  return (
    <Dialog>
      <div className="overflow-y-auto max-h-[80vh] overflow-x-hidden">
        <h2 className="text-xl font-semibold mb-4">Add Assignment</h2>
        <form className="gap-4 flex flex-col">
          <DropDown
            stringOnDisplay={formData.level}
            stateController={(value) =>
              setFormData({ ...formData, level: value })
            }
            iterable={filters.level.map((level) => level.name)}
          />
          <DropDown
            stringOnDisplay={formData.subject}
            stateController={(value) =>
              setFormData({ ...formData, subject: value })
            }
            iterable={filters.subject.map((subject) => subject.name)}
          />

          <Input
            type="text"
            name="location"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
            required
          />
          <div className="flex flex-row">
            <div className="flex justify-between mt-4">
              <Button onClick={goToPrevSlot} disabled={currentSlot === 0}>
                <ChevronLeft />
              </Button>
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={currentSlot}
                initial={{ x: 300, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: -300, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="w-full gap-4 flex flex-col border-black border-2 rounded-md p-3"
              >
                <span>
                  Slot {currentSlot + 1} / {formData.slots.length}
                </span>
                <DropDown
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
              </motion.div>
            </AnimatePresence>
            <div className="flex justify-between mt-4">
              <Button
                onClick={goToNextSlot}
                disabled={currentSlot === formData.slots.length - 1}
              >
                <ChevronRight />
              </Button>
            </div>
          </div>

          <div className="flex justify-end mt-2 space-x-2">
            {formData.slots.length > 1 && (
              <Button
                onClick={() => {
                  const newSlots = formData.slots.filter(
                    (_, idx) => idx !== currentSlot
                  );
                  setFormData({ ...formData, slots: newSlots });
                  setCurrentSlot((prev) => Math.max(prev - 1, 0));
                }}
              >
                Remove Slot
              </Button>
            )}
            <Button
              onClick={() =>
                setFormData({
                  ...formData,
                  slots: [
                    ...formData.slots,
                    {
                      day: "Select Day",
                      hours: "Hour",
                      minutes: "Minute",
                      duration: "1 hour",
                    },
                  ],
                })
              }
            >
              Add Slot
            </Button>
          </div>
          <DropDown
            stringOnDisplay={
              formData.fees || "Select Fees (Must select level first)"
            }
            iterable={[5]}
            stateController={(value) =>
              setFormData({ ...formData, fees: value })
            }
          />
          <div className="flex justify-center space-x-2">
            <Image
              src="/images/rates.png"
              alt="THE Logo"
              width={600}
              height={600}
            ></Image>
          </div>
          <div className="flex justify-end space-x-2">
            <Button onClick={() => router.back()} className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200">
              Cancel
            </Button>
            <Button
              onClick={() => handleSubmit()}
              className="px-4 py-2 bg-customYellow text-white rounded-md hover:bg-customOrange transition-colors duration-200"
            >
              Submit
            </Button>
          </div>
        </form>
      </div>
    </Dialog>
  );
}
