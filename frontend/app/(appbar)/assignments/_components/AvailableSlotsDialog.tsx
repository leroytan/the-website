import { useRef, useState } from "react";
import { Dialog } from "../../../../components/dialog";
import { Button } from "../../../../components/button";
import { X, ChevronLeft, ChevronRight, Plus, Clock, Hourglass } from "lucide-react";
import DropDown from "../../../../components/dropdown";
import { motion, AnimatePresence } from "framer-motion";

type Direction = "left" | "right";

interface TimeSlot {
  day: string;
  hours: string;
  minutes: string;
  duration: string;
}

interface ClientTimeSlot {
  day: string;
  start_time: string;
  end_time: string;
}

interface AvailableSlotsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (slots: { day: string; start_time: string; end_time: string }[]) => void;
  clientSlots?: ClientTimeSlot[];
}

const DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];
const DURATIONS = ["1 hour", "1.5 hours", "2 hours", "2.5 hours", "3 hours"];

export const AvailableSlotsDialog = ({
  isOpen,
  onClose,
  onSubmit,
  clientSlots = [],
}: AvailableSlotsDialogProps) => {
  const [slots, setSlots] = useState<TimeSlot[]>([
    {
      day: "",
      hours: "",
      minutes: "",
      duration: "",
    },
  ]);
  const [currentSlot, setCurrentSlot] = useState(0);
  const prevSlotRef = useRef(0);
  const directionRef = useRef<Direction>("right");

  const goToSlot = (newIndex: number) => {
    prevSlotRef.current = currentSlot;
    directionRef.current = newIndex > currentSlot ? "right" : "left";
    setCurrentSlot(newIndex);
  };

  const addSlot = () => {
    const newSlots = [
      ...slots,
      {
        day: "",
        hours: "",
        minutes: "",
        duration: "",
      },
    ];
    setSlots(newSlots);
    goToSlot(newSlots.length - 1);
  };

  const removeSlot = () => {
    if (slots.length <= 1) return;
    const newSlotIndex =
      currentSlot === slots.length - 1 ? currentSlot - 1 : currentSlot;
    const newSlots = slots.filter((_, idx) => idx !== currentSlot);
    setSlots(newSlots);
    goToSlot(newSlotIndex);
  };

  const goToPrevSlot = () => {
    if (slots.length <= 1 || currentSlot === 0) return;
    goToSlot(currentSlot - 1);
  };

  const goToNextSlot = () => {
    if (slots.length <= 1 || currentSlot === slots.length - 1) return;
    goToSlot(currentSlot + 1);
  };

  const handleSubmit = () => {
    // Validate slots
    const hasEmptyFields = slots.some(
      (slot) => !slot.day || !slot.hours || !slot.minutes || !slot.duration
    );
    if (hasEmptyFields) {
      alert("Please fill in all fields for each slot");
      return;
    }

    // Convert slots to the required format
    const formattedSlots = slots.map((slot) => {
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

    onSubmit(formattedSlots);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <Dialog className="w-[95vw] max-w-[600px] max-h-[90vh] overflow-y-auto overflow-x-hidden">
      <div className="space-y-4 p-4 sm:p-6">
        <div className="flex justify-between items-center border-b pb-4">
          <h2 className="text-xl font-semibold text-customDarkBlue">
            Select Your Available Time Slots
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-customOrange transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Client's Available Slots */}
        {clientSlots.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-base font-medium text-customDarkBlue">
              Client's Available Slots
            </h3>
            <div className="space-y-2">
              {clientSlots.map((slot, index) => {
                const start = slot.start_time;
                const end = slot.end_time;
                const [sh, sm] = start.split(":").map(Number);
                const [eh, em] = end.split(":").map(Number);
                const durationHours = eh + em / 60 - sh - sm / 60;

                return (
                  <div
                    key={`client-slot-${index}-${slot.day}-${start}-${end}`}
                    className="flex justify-between items-center bg-customLightYellow px-4 py-2 rounded-xl"
                  >
                    <span className="font-bold text-customDarkBlue">{slot.day}</span>
                    <div className="flex flex-col items-end text-customDarkBlue text-sm">
                      <div className="flex items-center gap-1">
                        <Clock size={14} /> {start} - {end}
                      </div>
                      <div className="flex items-center gap-1">
                        <Hourglass size={14} /> {durationHours.toFixed(1)} hours
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
        {/* Tutor's Available Slots */}
        <div className="border-t pt-4">
          <h3 className="text-base font-medium text-customDarkBlue mb-4">
            Your Available Slots
          </h3>
          <div className="space-y-4">
            <div className="flex flex-row items-center justify-center">
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

              <div className="relative w-full min-h-[280px]">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={`slot-${currentSlot}`}
                    initial={{
                      x: directionRef.current === "right" ? 300 : -300,
                      opacity: 0,
                    }}
                    animate={{ x: 0, opacity: 1 }}
                    exit={{
                      x: directionRef.current === "right" ? -300 : 300,
                      opacity: 0,
                    }}
                    transition={{ duration: 0.3 }}
                    className="top-0 left-0 w-full"
                  >
                    <div className="w-full gap-4 flex flex-col border-customDarkBlue bg-customLightYellow border-2 rounded-md p-4 shadow">
                      <div className="absolute top-2 right-2">
                        {slots.length > 1 && (
                          <Button
                            type="button"
                            onClick={removeSlot}
                            aria-label="Remove Slot"
                            className="text-gray-500 hover:text-customOrange/80"
                          >
                            <X size={20} />
                          </Button>
                        )}
                      </div>
                      <span className="text-customDarkBlue text-lg font-semibold mb-4">
                        Slot {currentSlot + 1} / {slots.length}
                      </span>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Day <span className="text-red-500">*</span>
                          </label>
                          <DropDown
                            placeholder="Select Day"
                            stringOnDisplay={slots[currentSlot].day}
                            stateController={(value) => {
                              const newSlots = [...slots];
                              newSlots[currentSlot].day = value;
                              setSlots(newSlots);
                            }}
                            iterable={DAYS}
                            className="w-full rounded-md text-sm"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Start Time <span className="text-red-500">*</span>
                          </label>
                          <div className="flex items-center gap-2">
                            <DropDown
                              placeholder="Hour"
                              stringOnDisplay={slots[currentSlot].hours}
                              iterable={Array.from({ length: 24 }, (_, i) =>
                                i.toString().padStart(2, "0")
                              )}
                              stateController={(value) => {
                                const newSlots = [...slots];
                                newSlots[currentSlot].hours = value;
                                setSlots(newSlots);
                              }}
                              className="w-full rounded-md text-sm"
                            />
                            <span className="text-customDarkBlue font-medium">
                              :
                            </span>
                            <DropDown
                              placeholder="Minute"
                              stringOnDisplay={slots[currentSlot].minutes}
                              iterable={Array.from({ length: 60 }, (_, i) =>
                                i.toString().padStart(2, "0")
                              )}
                              stateController={(value) => {
                                const newSlots = [...slots];
                                newSlots[currentSlot].minutes = value;
                                setSlots(newSlots);
                              }}
                              className="w-full rounded-md text-sm"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Duration <span className="text-red-500">*</span>
                          </label>
                          <DropDown
                            placeholder="Select Duration"
                            stringOnDisplay={slots[currentSlot].duration}
                            iterable={DURATIONS}
                            stateController={(value) => {
                              const newSlots = [...slots];
                              newSlots[currentSlot].duration = value;
                              setSlots(newSlots);
                            }}
                            className="w-full rounded-md text-sm"
                          />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              {currentSlot < slots.length - 1 && (
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
                onClick={addSlot}
                aria-label="Add Slot"
                className="flex items-center text-customDarkBlue hover:text-customOrange"
              >
                <Plus />
                <span>Add Slot</span>
              </Button>
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-2 pt-4 border-t">
          <Button
            className="px-4 py-2 bg-white border border-customDarkBlue text-customDarkBlue rounded-full hover:bg-customLightYellow transition-colors duration-200"
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            className="px-4 py-2 bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors duration-200"
          >
            Submit
          </Button>
        </div>
      </div>
    </Dialog>
  );
};
