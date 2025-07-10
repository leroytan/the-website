"use client";
import React, { useRef, useState, useEffect } from "react";
import { Button } from "./button";

interface MultiSelectProps {
  options: string[] | { value: string; label: string }[];
  applied?: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  placeholder?: string;
  className?: string;
  onApply?: () => void;
}

const MultiSelectButton: React.FC<MultiSelectProps> = ({
  options,
  applied,
  selected,
  onChange,
  placeholder = "Select...",
  className = "",
  onApply,
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

  // Normalize options to always be objects with value and label
  const normalizedOptions: { value: string; label: string }[] = Array.isArray(
    options
  )
    ? typeof options[0] === "string"
      ? (options as string[]).map((opt) => ({ value: opt, label: opt }))
      : (options as { value: string; label: string }[])
    : [];

  return (
    <div className={`relative w-full ${className}`} ref={ref}>
      <button
        type="button"
        className="px-4 py-2 border rounded-full bg-white text-customDarkBlue font-medium flex items-center justify-between w-full"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((prev) => !prev)}
      >
        <span>
          {applied ? (
            applied.length > 0 ? (
              <>
                {[...applied]
                  .sort(
                    (a, b) =>
                      normalizedOptions.findIndex((opt) => opt.value === a) -
                      normalizedOptions.findIndex((opt) => opt.value === b)
                  )
                  .slice(0, 3)
                  .map(
                    (val) =>
                      normalizedOptions.find((opt) => opt.value === val)
                        ?.label ?? val
                  )
                  .join(", ")}
                {selected.length > 3 && <>, +{selected.length - 3} more</>}
              </>
            ) : (
              <span className="text-gray-400">{placeholder}</span>
            )
          ) : selected.length > 0 ? (
            <>
              {selected
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
        <div className="absolute left-0 mt-2 w-full bg-white shadow-md rounded-lg border border-gray-300 z-50">
          <div className="flex flex-col max-h-60">
            <ul
              className="overflow-y-auto overflow-x-hidden"
              role="listbox"
              tabIndex={-1}
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
            {onApply && (
              <div className="sticky bottom-0 p-2 bg-white border-t border-gray-200 flex justify-between items-center">
                <Button
                  onClick={() => {
                    onChange([]);
                  }}
                  className="px-3 py-1 text-sm font-medium text-gray-600 hover:text-customDarkBlue transition-colors"
                >
                  Clear
                </Button>
                <Button
                  onClick={() => {
                    onApply();
                    setIsOpen(false);
                  }}
                  className="px-3 py-1 text-sm font-medium bg-customYellow text-white rounded-full hover:bg-customOrange transition-colors"
                >
                  Apply
                </Button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MultiSelectButton;
