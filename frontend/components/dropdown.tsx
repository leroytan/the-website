'use client';
import { useEffect, useRef, useState } from "react";

interface DropDownProps<T> {
  stringOnDisplay: string;
  stateController: (value: T) => void;
  iterable: T[];
  renderItem?: (item: T) => React.ReactNode;
  placeholder?: string;
}

function DropDown<T>({
  stringOnDisplay,
  stateController,
  iterable,
  renderItem,
  placeholder = "Select...",
}: DropDownProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
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
    <div className="relative w-full" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="px-4 py-2 border rounded-full bg-white text-customDarkBlue font-medium flex items-center justify-between w-full"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
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
        <ul
          ref={listRef}
          className="absolute left-0 mt-2 w-full bg-white shadow-md rounded-lg border border-gray-300 z-50 max-h-60 overflow-y-auto animate-fade-in"
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
                onClick={(e) => {
                  e.preventDefault();
                  stateController(item);
                  setIsOpen(false);
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
                    stateController(item);
                    setIsOpen(false);
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
                className="px-4 py-2 hover:bg-customYellow hover:text-white cursor-pointer transition-colors flex items-center"
              >
                {renderItem ? renderItem(item) : String(item)}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}

export default DropDown;