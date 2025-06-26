'use client';
import { useEffect, useRef, useState } from "react";
import { Button } from "./button";

interface DropDownProps<T> {
  stringOnDisplay: string;
  stateController?: (value: T) => void;
  iterable: T[];
  renderItem?: (item: T) => React.ReactNode;
  placeholder?: string;
  className?: string;
  onApply?: (value: T) => void;
  disabled?: boolean;
}

function DropDown<T>({
  stringOnDisplay,
  stateController,
  iterable,
  renderItem,
  placeholder = "Select...",
  className = "",
  onApply,
  disabled
}: DropDownProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
  const [tempSelected, setTempSelected] = useState<T | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
        setTempSelected(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  // Keyboard navigation
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!listRef.current) return;
      const items = Array.from(
        listRef.current.querySelectorAll("li[role=option]")
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
      } else if (e.key === "Escape") {
        setIsOpen(false);
        setTempSelected(null);
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  // Determine if nothing is selected (show placeholder)
  const showPlaceholder =
    stringOnDisplay === "" ||
    stringOnDisplay === "Select..." ||
    stringOnDisplay === "Select" ||
    stringOnDisplay === placeholder;

  return (
    <div className={`relative w-full ${className}`} ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className={`px-4 py-2 border rounded-full bg-white text-customDarkBlue font-medium flex items-center justify-between w-full ${disabled ? "bg-gray-200 cursor-not-allowed" : ""}`}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        disabled={disabled}
      >
        <span className={showPlaceholder ? "text-gray-400" : ""}>
          {showPlaceholder ? placeholder : stringOnDisplay}
        </span>
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
              ref={listRef}
              className="overflow-y-auto overflow-x-hidden"
              role="listbox"
              tabIndex={-1}
            >
              {iterable.length === 0 ? (
                <li className="px-4 py-2 text-gray-400">No options</li>
              ) : (
                iterable.map((item, index) => (
                  <li
                    key={index}
                    role="option"
                    tabIndex={0}
                    aria-selected={tempSelected === item}
                    onClick={(e) => {
                      e.preventDefault();
                      setTempSelected(item);
                      if (!onApply) {
                        stateController && stateController(item);
                        setIsOpen(false);
                      }
                    }}
                    onKeyDown={(e) => {
                      const items = Array.from(
                        e.currentTarget.parentElement?.querySelectorAll(
                          "li[role=option]"
                        ) ?? []
                      ) as HTMLLIElement[];
                      const currentIndex = items.findIndex(
                        (el) => el === e.currentTarget
                      );

                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        setTempSelected(item);
                        if (!onApply) {
                          stateController && stateController(item);
                          setIsOpen(false);
                        }
                      } else if (e.key === "Tab") {
                        e.preventDefault();
                        const next = items[(currentIndex + 1) % items.length];
                        next?.focus();
                      } else if (e.key === "ArrowUp") {
                        e.preventDefault();
                        const prev =
                          items[(currentIndex - 1 + items.length) % items.length];
                        prev?.focus();
                      } else if (e.key === "ArrowDown") {
                        e.preventDefault();
                        const next = items[(currentIndex + 1) % items.length];
                        next?.focus();
                      }
                    }}
                    className={`px-4 py-2 cursor-pointer transition-colors flex items-center ${
                      tempSelected === item
                        ? "bg-customYellow text-white"
                        : "hover:bg-gray-100 hover:text-customDarkBlue"
                    }`}
                  >
                    {renderItem ? renderItem(item) : String(item)}
                  </li>
                ))
              )}
            </ul>
            {onApply && (
              <div className="sticky bottom-0 p-2 bg-white border-t border-gray-200 flex justify-between items-center">
                <Button
                  onClick={() => {
                    setTempSelected(null);
                  }}
                  className="px-3 py-1 text-sm font-medium text-gray-600 hover:text-customDarkBlue transition-colors"
                >
                  Clear
                </Button>
                <Button
                  onClick={() => {
                    if (tempSelected !== null) {
                      stateController && stateController(tempSelected);
                      onApply(tempSelected);
                    }
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
}

export default DropDown;