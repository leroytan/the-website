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

  // Close dropdown on outside click or Escape key
  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [isOpen]);

  const toggleOption = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter((item) => item !== option));
    } else {
      onChange([...selected, option]);
    }
  };

  // Keyboard navigation for options
  const handleKeyDown = (e: React.KeyboardEvent<HTMLUListElement>) => {
    if (!isOpen) return;
    const items = Array.from(
      ref.current?.querySelectorAll("li[role=option]") ?? []
    ) as HTMLLIElement[];
    const currentIndex = items.findIndex(
      (item) => item === document.activeElement
    );
    if (e.key === "ArrowDown") {
      e.preventDefault();
      const next = items[(currentIndex + 1) % items.length];
      next?.focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      const prev = items[(currentIndex - 1 + items.length) % items.length];
      prev?.focus();
    }
  };

  return (
    <div className="relative w-full" ref={ref}>
      <button
        type="button"
        className="px-4 py-2 border rounded-full bg-white text-customDarkBlue font-medium flex items-center justify-between w-full"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((prev) => !prev)}
      >
        <span>
  {selected.length > 0 ? (
    <>
      {[...selected]
        .sort((a, b) => options.indexOf(a) - options.indexOf(b))
        .slice(0, 3)
        .join(", ")}
      {selected.length > 3 && (
        <>, +{selected.length - 3} more</>
      )}
    </>
  ) : (
    <span className="text-gray-400">{placeholder}</span>
  )}
</span>
        {/* Dropdown arrow */}
        <svg
          className={`ml-2 h-4 w-4 transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      {isOpen && (
        <ul
          className="absolute left-0 mt-2 w-full bg-white shadow-md rounded-lg border border-gray-300 z-50 max-h-60 overflow-y-auto animate-fade-in"
          role="listbox"
          tabIndex={-1}
          onKeyDown={handleKeyDown}
        >
          {options.map((option) => (
            <li
              key={option}
              role="option"
              aria-selected={selected.includes(option)}
              tabIndex={0}
              onClick={() => toggleOption(option)}
              onKeyDown={(e) => {
                if (e.key === " " || e.key === "Enter") {
                  e.preventDefault();
                  toggleOption(option);
                }
              }}
              className={`px-4 py-2 cursor-pointer transition-colors flex items-center ${
                selected.includes(option)
                  ? "bg-customYellow text-white font-semibold"
                  : "hover:bg-gray-100 hover:text-customDarkBlue"
              }`}
            >
              {option}
              {selected.includes(option) && (
                <span className="ml-auto text-white font-bold">✔</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MultiSelectButton;
