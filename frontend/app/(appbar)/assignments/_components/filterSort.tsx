"use client";
import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import MultiSelectButton from "@/components/multiSelectButton";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { useTransition, useState } from "react";

interface FilterSortProps {
  subjects: { id: string; name: string }[];
  levels: { id: string; name: string }[];
  sortOptions: { value: string; label: string }[];
}

export function FilterSortBar({
  subjects,
  levels,
  sortOptions,
}: FilterSortProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const [isPending, startTransition] = useTransition();

  // Prepare options
  const subjectOptions = subjects.map((s) => s.name);
  const levelOptions = levels.map((l) => l.name);

  // Local state for filters
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>(searchParams.getAll("subject"));
  const [selectedLevels, setSelectedLevels] = useState<string[]>(searchParams.getAll("level"));
  const [selectedSort, setSelectedSort] = useState<string>(searchParams.get("sort") || "");

  // Handlers update local state only
  const onSubjectsChange = (selected: string[]) => setSelectedSubjects(selected);
  const onLevelsChange = (selected: string[]) => setSelectedLevels(selected);
  const onChangeSort = (value: string) => setSelectedSort(value);

  // Apply filters when button is clicked
  const applyFilters = () => {
    const params = new URLSearchParams();
    selectedSubjects.forEach((s) => params.append("subject", s));
    selectedLevels.forEach((l) => params.append("level", l));
    if (selectedSort) params.set("sort", selectedSort);
    params.set("page", "1");
    router.push(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="sticky z-20 bg-white px-6 pt-4 pb-3 shadow-md w-full">
      <div className="flex flex-wrap gap-4 justify-start items-end">
        {/* MultiSelect for Subjects */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={subjectOptions}
            selected={selectedSubjects}
            onChange={onSubjectsChange}
            placeholder="All Subjects"
          />
        </div>
        {/* MultiSelect for Levels */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={levelOptions}
            selected={selectedLevels}
            onChange={onLevelsChange}
            placeholder="All Levels"
          />
        </div>
        {/* Sort select with dropdown */}
        <div className="min-w-[180px]">
          <DropDown
            stringOnDisplay={
              sortOptions.find((opt) => opt.value === selectedSort)?.label ||
              "Sort by"
            }
            stateController={(option) => onChangeSort(option.value)}
            iterable={sortOptions}
            renderItem={(option) => <span>{option.label}</span>}
          />
        </div>
        {/* Filter Button */}
        <Button
          className="ml-2 px-6 py-2 bg-customYellow text-white rounded-full font-semibold hover:bg-customOrange transition-colors"
          onClick={applyFilters}
          disabled={isPending}
        >
          Filter
        </Button>
      </div>
    </div>
  );
}