"use client";
import { Button } from "@/components/button";
import DropDown from "@/components/dropdown";
import MultiSelectButton from "@/components/multiSelectButton";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { useTransition, useState } from "react";
import { HorizontalLoader } from "./horizontalLoader";

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
  const subjectOptions = subjects.map(({ id, name }) => ({
    value: id,
    label: name,
  }));
  const levelOptions = levels.map(({ id, name }) => ({
    value: id,
    label: name,
  }));

  // Parse filters from URL
  const filtersParam = searchParams.get("filter_by") || "";
  const filterIds = filtersParam.split(",").filter(Boolean); // Split by comma and remove empty values

  // Separate filters into levels and subjects
  const initialSelectedLevels = filterIds.filter((id) =>
    levels.some((level) => level.id === id)
  );
  const initialSelectedSubjects = filterIds.filter((id) =>
    subjects.some((subject) => subject.id === id)
  );

  // Local state for filters
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>(
    initialSelectedSubjects
  );
  const [selectedLevels, setSelectedLevels] = useState<string[]>(
    initialSelectedLevels
  );
  const [selectedSort, setSelectedSort] = useState<string>(
    searchParams.get("sort") || ""
  );

  // Handlers update local state only
  const onSubjectsChange = (selected: string[]) =>
    setSelectedSubjects(selected);
  const onLevelsChange = (selected: string[]) => setSelectedLevels(selected);
  const onChangeSort = (value: string) => setSelectedSort(value);

  // Apply filters when button is clicked
  const applyFilters = () => {
    const params = new URLSearchParams();

    // Remove filters params if they are empty
    if (selectedSubjects.length + selectedLevels.length === 0) {
      params.delete("filter_by");
    } else {
      params.set(
        "filter_by",
        [...selectedSubjects, ...selectedLevels].join(",")
      );
    }
    if (selectedSort) params.set("sort_by", selectedSort);

    // Use startTransition to defer the navigation
    startTransition(() => {
      router.push(`${pathname}?${params.toString()}`);
    });
  };

  return (
    <div className="sticky top-14 z-10 bg-white px-6 pt-4 pb-3 shadow-md w-full">
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
            placeholder="Sort by"
            stringOnDisplay={
              sortOptions.find((opt) => opt.value === selectedSort)?.label || ""
            }
            stateController={(option) => onChangeSort(option.value)}
            iterable={sortOptions}
            renderItem={(option) => <span>{option.label}</span>}
          />
        </div>
        {/* Filter Button */}
        <Button
          className="ml-2 px-6 py-2 bg-customYellow text-white rounded-full font-semibold hover:bg-customOrange transition-colors flex items-center"
          onClick={applyFilters}
          disabled={isPending} // Disable button while pending
        >
          Filter
        </Button>
      </div>

      {/* Horizontal Loading Indicator */}
      <HorizontalLoader isLoading={isPending} />
    </div>
  );
}