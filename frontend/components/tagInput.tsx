"use client";
import { useState, KeyboardEvent } from "react";
import { X } from "lucide-react";

export default function TagInput({
  tags,
  setTags,
  placeholder = "Add a skill and press Enter",
}: {
  tags: string[];
  setTags: (tags: string[]) => void;
  placeholder?: string;
}) {
  const [input, setInput] = useState("");

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if ((e.key === "Enter" || e.key === ",") && input.trim()) {
      e.preventDefault();
      if (!tags.includes(input.trim())) {
        setTags([...tags, input.trim()]);
      }
      setInput("");
    } else if (e.key === "Backspace" && !input) {
      setTags(tags.slice(0, -1));
    }
  };

  const removeTag = (index: number) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  return (
    <div className="border rounded-md p-2 min-h-[42px] flex flex-wrap items-center gap-2 focus-within:ring-2 focus-within:ring-[#fabb84]">
      {tags.map((tag, i) => (
        <span
          key={i}
          className="bg-[#fabb84] text-white px-2 py-1 rounded-full flex items-center space-x-1 text-sm"
        >
          <span>{tag}</span>
          <button onClick={() => removeTag(i)} type="button">
            <X size={16} />
          </button>
        </span>
      ))}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="flex-1 border-none focus:ring-0 focus:outline-none min-w-[150px]"
      />
    </div>
  );
}
