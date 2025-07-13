import { useRef, useState, useEffect } from "react";
import { Dialog } from "../../../../components/dialog";
import { Button } from "../../../../components/button";
import {
  X,
  ChevronLeft,
  ChevronRight,
  Plus,
  Clock,
  Hourglass,
} from "lucide-react";
import DropDown from "../../../../components/dropdown";
import { motion, AnimatePresence } from "framer-motion";
import Checkbox from "../../../../components/checkbox";

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
  onSubmit: (data: {
    requested_rate_hourly: number;
    available_slots: { day: string; start_time: string; end_time: string }[];
  }) => void;
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
const DURATIONS = [
  "1 hour",
  "1.5 hours",
  "2 hours",
  "2.5 hours",
  "3 hours",
  "3.5 hours",
  "4 hours",
  "4.5 hours",
  "5 hours",
];

export const TutorRequestDialog = ({
  isOpen,
  onClose,
  onSubmit,
  clientSlots = [],
}: AvailableSlotsDialogProps) => {
  const [slots, setSlots] = useState<TimeSlot[]>([]);
  const [currentSlot, setCurrentSlot] = useState(0);
  const [requestedRate, setRequestedRate] = useState("");
  const prevSlotRef = useRef(0);
  const directionRef = useRef<Direction>("right");
  const [copiedMappings, setCopiedMappings] = useState<Record<number, number>>(
    {}
  );

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
    const removedSlotIdx = currentSlot;
    const newSlotIndex =
      currentSlot === slots.length - 1 ? currentSlot - 1 : currentSlot;
    const newSlots = slots.filter((_, idx) => idx !== removedSlotIdx);
    // Remove any mapping in copiedMappings that points to the removed slot
    const newMappings: Record<number, number> = {};
    Object.entries(copiedMappings).forEach(([cIdx, tIdx]) => {
      const t = tIdx as number;
      if (t < removedSlotIdx) {
        newMappings[Number(cIdx)] = t;
      } else if (t > removedSlotIdx) {
        newMappings[Number(cIdx)] = t - 1;
      }
      // If t === removedSlotIdx, do not copy (removes the mapping)
    });
    setSlots(newSlots);
    setCopiedMappings(newMappings);
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
    if (!requestedRate) {
      alert("Please select a requested hourly rate.");
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

    onSubmit({
      requested_rate_hourly: parseInt(requestedRate, 10),
      available_slots: formattedSlots,
    });
    onClose();
  };

  useEffect(() => {
    if (slots.length === 0) {
      setSlots([{ day: "", hours: "", minutes: "", duration: "" }]);
      setCurrentSlot(0);
    }
  }, [slots]);

  if (!isOpen) return null;

  return (
    <Dialog className="relative">
      <Button
            onClick={onClose}
            className="absolute top-4 right-4 text-customOrange hover:text-red-700 transition-colors duration-200 z-10"
            aria-label="Close"
          >
            <X size={24} />
          </Button>
      <div>
        <h2 className="text-xl font-semibold mb-4 text-center sm:text-left text-customDarkBlue">
          Select Your Rate & Available Slots
        </h2>
      </div>
      <div className="overflow-y-auto max-h-[80vh] p-4 space-y-4">

        {/* Requested Rate Dropdown */}
        <div>
          <h3 className="text-base font-medium text-customDarkBlue mb-2">
            Requested Hourly Rate <span className="text-red-500">*</span>
          </h3>
          <DropDown
            placeholder="Select Rate"
            stringOnDisplay={requestedRate ? `$${requestedRate}/hour` : ""}
            iterable={[
              25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
            ].map((r) => `${r}`)}
            renderItem={(option) => <span>${option}/hour</span>}
            stateController={setRequestedRate}
            className="w-full rounded-md text-sm"
          />
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
                const durationMinutes = eh * 60 + em - (sh * 60 + sm);
                const durationOptions = [60, 90, 120, 150, 180];
                const closestDuration = durationOptions.reduce(
                  (prev, curr) =>
                    Math.abs(curr - durationMinutes) <
                    Math.abs(prev - durationMinutes)
                      ? curr
                      : prev,
                  durationOptions[0]
                );
                const hours = Math.floor(closestDuration / 60);
                const mins = closestDuration % 60;
                const durationLabel =
                  mins === 0 ? `${hours} hour` : `${hours}.5 hour`;

                return (
                  <div
                    key={`client-slot-${index}-${slot.day}-${start}-${end}`}
                    className="flex justify-between items-center bg-customLightYellow px-4 py-2 rounded-xl"
                  >
                    <Checkbox
                      checked={!!copiedMappings.hasOwnProperty(index)}
                      onChange={() => {
                        if (copiedMappings.hasOwnProperty(index)) {
                          // Uncheck: remove the mapped tutor slot
                          const slotIdx = copiedMappings[index];
                          const newSlots = slots.filter(
                            (_, i) => i !== slotIdx
                          );
                          // Remove mapping and update all mappings after the removed slot
                          const newMappings: Record<number, number> = {};
                          Object.entries(copiedMappings).forEach(
                            ([cIdx, tIdx]) => {
                              const cIdxNum = Number(cIdx);
                              const t = tIdx as number;
                              if (cIdxNum !== index) {
                                newMappings[cIdxNum] = t > slotIdx ? t - 1 : t;
                              }
                            }
                          );
                          if (newSlots.length === 0) {
                            setSlots([
                              { day: "", hours: "", minutes: "", duration: "" },
                            ]);
                            setCurrentSlot(0);
                          } else {
                            setSlots(newSlots);
                            setCurrentSlot(Math.max(0, slotIdx - 1));
                          }
                          setCopiedMappings(newMappings);
                        } else {
                          // Check: add new slot or fill current if empty
                          let slotToUse = currentSlot;
                          let newSlots = [...slots];
                          const isCurrentEmpty =
                            !slots[currentSlot].day &&
                            !slots[currentSlot].hours &&
                            !slots[currentSlot].minutes &&
                            !slots[currentSlot].duration;
                          if (isCurrentEmpty) {
                            newSlots[currentSlot] = {
                              day: slot.day,
                              hours: sh.toString().padStart(2, "0"),
                              minutes: sm.toString().padStart(2, "0"),
                              duration: durationLabel,
                            };
                          } else {
                            newSlots = [
                              ...slots,
                              {
                                day: slot.day,
                                hours: sh.toString().padStart(2, "0"),
                                minutes: sm.toString().padStart(2, "0"),
                                duration: durationLabel,
                              },
                            ];
                            slotToUse = newSlots.length - 1;
                            setCurrentSlot(slotToUse);
                          }
                          setSlots(newSlots);
                          setCopiedMappings({
                            ...copiedMappings,
                            [index]: slotToUse,
                          });
                        }
                      }}
                      className="mr-2"
                    />
                    <span className="font-bold text-customDarkBlue">
                      {slot.day}
                    </span>
                    <div className="flex flex-col items-end text-customDarkBlue text-sm">
                      <div className="flex items-center gap-1">
                        <Clock size={14} /> {start} - {end}
                      </div>
                      <div className="flex items-center gap-1">
                        <Hourglass size={14} />{" "}
                        {(durationMinutes / 60).toFixed(1)} hours
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
                          <div
                            className={
                              Object.values(copiedMappings).includes(
                                currentSlot
                              )
                                ? "pointer-events-none opacity-60"
                                : ""
                            }
                          >
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
                              disabled={Object.values(copiedMappings).includes(
                                currentSlot
                              )}
                            />
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Start Time <span className="text-red-500">*</span>
                          </label>
                          <div
                            className={
                              Object.values(copiedMappings).includes(
                                currentSlot
                              )
                                ? "pointer-events-none opacity-60"
                                : ""
                            }
                          >
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
                                disabled={Object.values(
                                  copiedMappings
                                ).includes(currentSlot)}
                              />
                              <span className="text-customDarkBlue font-medium">
                                :
                              </span>
                              <DropDown
                                placeholder="Minute"
                                stringOnDisplay={slots[currentSlot].minutes}
                                iterable={["00", "30"]}
                                stateController={(value) => {
                                  const newSlots = [...slots];
                                  newSlots[currentSlot].minutes = value;
                                  setSlots(newSlots);
                                }}
                                className="w-full rounded-md text-sm"
                                disabled={Object.values(
                                  copiedMappings
                                ).includes(currentSlot)}
                              />
                            </div>
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-customDarkBlue mb-1">
                            Duration <span className="text-red-500">*</span>
                          </label>
                          <div
                            className={
                              Object.values(copiedMappings).includes(
                                currentSlot
                              )
                                ? "pointer-events-none opacity-60"
                                : ""
                            }
                          >
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
                              disabled={Object.values(copiedMappings).includes(
                                currentSlot
                              )}
                            />
                          </div>
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
