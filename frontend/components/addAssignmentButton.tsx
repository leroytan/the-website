import { useState } from "react";
import { Button } from "./button";
import DropDown from "./dropdown";
import Image from "next/image";
const convertTo12HourFormat = (hours: string, minutes: string) => {
    let hour = parseInt(hours, 10);
    const minute = minutes.padStart(2, "0");
    const ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12 || 12; // Convert 0 to 12 for 12 AM
    return `${hour.toString().padStart(2, "0")}:${minute} ${ampm}`;
  };
function Input({
  type,
  name,
  placeholder,
  value,
  onChange,
  required,
}: {
  type: string;
  name: string;
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
}) {
  return (
    <input
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      required={required}
      className="w-full p-2 border rounded"
    />
  );
}

function Dialog({
  open,
  children,
}: {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
}) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-10">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">{children}</div>
    </div>
  );
}

const levelFeesMapping: { [key: string]: string[] } = {
  "Primary 1": ["$25", "$30", "$35"],
  "Primary 2": ["$25", "$30", "$35"],
  "Primary 3": ["$30", "$35", "$40"],
  "Primary 4": ["$30", "$35", "$40"],
  "Primary 5": ["$35", "$40", "$45"],
  "Primary 6": ["$35", "$40", "$45"],
};

export default function AddAssignmentButton({
  addListingController,
}: {
  addListingController: (listing: {
    id: number;
    time: string;
    title: string;
    location: string;
    duration: string;
    price: string;
    averagePrice: number;
    status: string;
    level: string;
    subject: string;
  }) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    level: "Select Level",
    subject: "Select Subject",
    location: "",
    day: "Select Day",
    hours: "Hour",
    minutes: "Minute",
    duration: "1 hour",
    fees: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted Data:", formData);
    setIsOpen(false);
  };

  const handleLevelChange = (value: string) => {
    setFormData({ ...formData, level: value, fees: "" });
  };

  return (
    <div className="flex justify-center items-center">
      <Button
        onClick={() => setIsOpen(true)}
        className="bg-customDarkBlue text-white"
      >
        Add Assignment
      </Button>

      <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
        <h2 className="text-xl font-semibold mb-4">Add Assignment</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <DropDown
            stringOnDisplay={formData.level}
            stateController={handleLevelChange}
            iterable={[
              "Primary 1",
              "Primary 2",
              "Primary 3",
              "Primary 4",
              "Primary 5",
              "Primary 6",
            ]}
          />
          <DropDown
            stringOnDisplay={formData.subject}
            stateController={(value) =>
              setFormData({ ...formData, subject: value })
            }
            iterable={["English", "Mathematics", "Science", "Chinese"]}
          />

          <Input
            type="text"
            name="location"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
            required
          />
          <DropDown
            stringOnDisplay={formData.day}
            stateController={(value) =>
              setFormData({ ...formData, day: value })
            }
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
              stringOnDisplay={formData.hours}
              iterable={Array.from({ length: 24 }, (_, i) =>
                i.toString().padStart(2, "0")
              )}
              stateController={(value) =>
                setFormData({ ...formData, hours: value })
              }
            />
            <p>:</p>
            <DropDown
              stringOnDisplay={formData.minutes}
              iterable={Array.from({ length: 60 }, (_, i) =>
                i.toString().padStart(2, "0")
              )}
              stateController={(value) =>
                setFormData({ ...formData, minutes: value })
              }
            />
          </div>

          <DropDown
            stringOnDisplay={formData.duration}
            iterable={[
              "1 hour",
              "1.5 hours",
              "2 hours",
              "2.5 hours",
              "3 hours",
            ]}
            stateController={(value) =>
              setFormData({ ...formData, duration: value })
            }
          />
          <DropDown
            stringOnDisplay={
              formData.fees || "Select Fees (Must select level first)"
            }
            iterable={levelFeesMapping[formData.level] || []}
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
            <Button
              onClick={() => setIsOpen(false)}
              className="bg-customYellow text-white"
            >
              Cancel
            </Button>
            <Button
              onClick={() => {
                setIsOpen(false);
                addListingController({
                  ...formData,
                  level: "Primary",
                  id: Date.now(),
                  time: `${formData.day.slice(0,3).toLocaleUpperCase()+ " "} ${convertTo12HourFormat(formData.hours, formData.minutes)}`,
                  title: `P5 Math`,
                  price: formData.fees,
                  averagePrice: parseFloat(formData.fees.replace('$', '')),
                  status: "apply",
                });
              }}
              className="bg-customDarkBlue text-white"
            >
              Submit
            </Button>
          </div>
        </form>
      </Dialog>
    </div>
  );
}
