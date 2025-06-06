"use client";
import React, { useRef, useState, useEffect } from "react";

interface MultiSelectProps {
  options: string[] | { value: string; label: string }[];
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

  // Normalize options to always be objects with value and label
  const normalizedOptions: { value: string; label: string }[] = Array.isArray(
    options
  )
    ? typeof options[0] === "string"
      ? (options as string[]).map((opt) => ({ value: opt, label: opt }))
      : (options as { value: string; label: string }[])
    : [];

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
                .sort(
                  (a, b) =>
                    normalizedOptions.findIndex((opt) => opt.value === a) -
                    normalizedOptions.findIndex((opt) => opt.value === b)
                )
                .slice(0, 3)
                .map(
                  (val) =>
                    normalizedOptions.find((opt) => opt.value === val)?.label ??
                    val
                )
                .join(", ")}
              {selected.length > 3 && <>, +{selected.length - 3} more</>}
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
          {normalizedOptions.length === 0 ? (
            <li className="px-4 py-2 text-gray-400">No options</li>
          ) : (
            normalizedOptions.map((option) => (
              <li
                key={option.value}
                role="option"
                aria-selected={selected.includes(option.value)}
                tabIndex={0}
                onClick={() => toggleOption(option.value)}
                onKeyDown={(e) => {
                  if (e.key === " " || e.key === "Enter") {
                    e.preventDefault();
                    toggleOption(option.value);
                  }
                }}
                className={`px-4 py-2 cursor-pointer transition-colors flex items-center ${
                  selected.includes(option.value)
                    ? "bg-customYellow text-white font-semibold"
                    : "hover:bg-gray-100 hover:text-customDarkBlue"
                }`}
              >
                {option.label}
                {selected.includes(option.value) && (
                  <span className="ml-auto text-white font-bold">✔</span>
                )}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
};

export default MultiSelectButton;
