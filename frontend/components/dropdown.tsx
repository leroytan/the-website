import { ReactElement, useState } from "react";

const DropDown = ({
  stringOnDisplay,
  stateController,
  iterable,
}: {
  stringOnDisplay: string;
  stateController: (value: any) => void;
  iterable: React.ReactNode[];
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const toggleDropdown = (e: React.FormEvent) => {
    e.preventDefault();
    setIsOpen((prev) => !prev);
  };

  return (
    <div className="relative w-full">
      <button
        onClick={toggleDropdown}
        className="w-full px-4 py-2 bg-gray-200 rounded-lg text-left font-medium 
                        hover:bg-gray-300 focus:outline-none transition-colors"
      >
        {stringOnDisplay}
      </button>

      {isOpen && (
        <ul
          className="absolute w-full mt-2 bg-white shadow-md rounded-lg border border-gray-300 z-10 
        max-h-[30vh] overflow-y-auto"
        >
          {iterable.map((item, index) => (
            <li
              key={index}
              onClick={(e) => {
                e.preventDefault();
                stateController(item);
                setIsOpen(false);
              }}
              className="px-4 py-2 hover:bg-blue-500 hover:text-white cursor-pointer transition-colors"
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropDown;
