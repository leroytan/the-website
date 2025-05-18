import React, { useRef, useState, useEffect } from "react";

interface MultiSelectProps {
  options: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  placeholder?: string;
}

const MultiSelectButton: React.FC<MultiSelectProps> = ({
  options,
  selected,
  onChange,
  placeholder = "Select...",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  const toggleOption = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter((item) => item !== option));
    } else {
      onChange([...selected, option]);
    }
  };

  return (
    <div className="relative w-full" ref={ref}>
      <button
        type="button"
        className="w-full px-4 py-2 bg-gray-200 rounded-lg text-left font-medium hover:bg-gray-300 focus:outline-none transition-colors"
        onClick={() => setIsOpen((prev) => !prev)}
      >
        {selected.length > 0 ? selected.join(", ") : <span className="text-gray-400">{placeholder}</span>}
      </button>
      {isOpen && (
        <ul className="absolute w-full mt-2 bg-white shadow-md rounded-lg border border-gray-300 z-10 max-h-60 overflow-y-auto">
          {options.map((option) => (
            <li
              key={option}
              onClick={() => toggleOption(option)}
              className={`px-4 py-2 cursor-pointer transition-colors flex items-center ${
                selected.includes(option)
                  ? "bg-customOrange  text-white font-semibold"
                  : "hover:bg-customYellow hover:text-white"
              }`}
            >
              <input
                type="checkbox"
                checked={selected.includes(option)}
                readOnly
                className="mr-2 accent-customYellow rounded-full"
              />
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MultiSelectButton;