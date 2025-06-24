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
  locations: { id: string; name: string }[];
  sortOptions: { value: string; label: string }[];
}

export function FilterSortBar({
  subjects,
  levels,
  locations,
  sortOptions,
}: FilterSortProps) {
  const params = useSearchParams();
  const searchParams = new URLSearchParams(params?.toString() || "");
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
  const locationOptions = locations.map(({ id, name }) => ({
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
  const initialSelectedLocations = filterIds.filter((id) =>
    locations.some((location) => location.id === id)
  );

  // Local state for filters
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>(
    initialSelectedSubjects
  );
  const [selectedLevels, setSelectedLevels] = useState<string[]>(
    initialSelectedLevels
  );
  const [selectedLocations, setSelectedLocations] = useState<string[]>(
    initialSelectedLocations
  );
  const [selectedSort, setSelectedSort] = useState<string>(
    searchParams.get("sort_by") || ""
  );

  // Handlers update local state only
  const onSubjectsChange = (selected: string[]) =>
    setSelectedSubjects(selected);
  const onLevelsChange = (selected: string[]) => 
    setSelectedLevels(selected);
  const onLocationsChange = (selected: string[]) =>
    setSelectedLocations(selected);

  const onSortChange = (option: { value: string; label: string }) => {
    setSelectedSort(option.value);
    const params = new URLSearchParams(searchParams.toString());
    if (option.value) {
      params.set("sort_by", option.value);
    }
    else {
      params.delete("sort_by");
    }
    params.delete("page_number"); // Clear page number on sort change
    startTransition(() => {
      router.push(`${pathname}?${params.toString()}`);
    });
  }
  // Apply individual filter for a specific type
  const applyIndividualFilter = (type: 'subjects' | 'levels' | 'locations') => {
    const params = new URLSearchParams(searchParams.toString());
    const currentFilters = params.get("filter_by")?.split(",").filter(Boolean) || [];

    // Remove existing filters of the same type
    const otherFilters = currentFilters.filter(id => {
      if (type === 'subjects') {
        return !subjects.some(subject => subject.id === id);
      } else if (type === 'levels') {
        return !levels.some(level => level.id === id);
      } else {
        return !locations.some(location => location.id === id);
      }
    });

    // Add new filters
    const newFilters = type === 'subjects' ? selectedSubjects : type === 'levels' ? selectedLevels : selectedLocations;
    const allFilters = [...otherFilters, ...newFilters];

    if (allFilters.length === 0) {
      params.delete("filter_by");
    } else {
      params.set("filter_by", allFilters.join(","));
    }
    //remove page_number
    params.delete("page_number");

    startTransition(() => {
      router.push(`${pathname}?${params.toString()}`);
    });
  };

  // Clear all filters
  const clearAllFilters = () => {
    const params = new URLSearchParams(searchParams.toString());
    params.delete("filter_by");
    params.delete("sort_by");
    params.delete("page_number"); // Clear page number on filter reset
    setSelectedSort("");
    setSelectedSubjects([]);
    setSelectedLevels([]);
    setSelectedLocations([]);
    
    startTransition(() => {
      router.push(`${pathname}?${params.toString()}`);
    });
  };


  return (
    <div className="sticky top-0 z-10 bg-white px-6 pt-4 pb-3 shadow-md w-full">
      <div className="flex flex-wrap gap-4 justify-start items-end">
        {/* MultiSelect for Subjects */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={subjectOptions}
            selected={selectedSubjects}
            onChange={onSubjectsChange}
            placeholder="All Subjects"
            onApply={() => applyIndividualFilter('subjects')}
          />
        </div>
        {/* MultiSelect for Levels */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={levelOptions}
            selected={selectedLevels}
            onChange={onLevelsChange}
            placeholder="All Levels"
            onApply={() => applyIndividualFilter('levels')}
          />
        </div>
        {/* MultiSelect for Locations */}
        <div className="min-w-[180px]">
          <MultiSelectButton
            options={locationOptions}
            selected={selectedLocations}
            onChange={onLocationsChange}
            placeholder="All Locations"
            onApply={() => applyIndividualFilter('locations')}
          />
        </div>
        {/* Sort select with dropdown */}
        <div className="min-w-[180px]">
          <DropDown
            placeholder="Sort by"
            stringOnDisplay={
              sortOptions.find((opt) => opt.value === selectedSort)?.label || ""
            }
            iterable={sortOptions}
            renderItem={(option) => <span>{option.label}</span>}
            onApply={onSortChange}
          />
        </div>
        {/* Clear All Filters Button */}
        <Button
          className="ml-2 px-6 py-2 bg-customYellow text-white rounded-full font-semibold hover:bg-customOrange transition-colors flex items-center"
          onClick={clearAllFilters}
          disabled={isPending}
        >
          Clear All Filters
        </Button>
      </div>

      {/* Horizontal Loading Indicator */}
      <HorizontalLoader isLoading={isPending} />
    </div>
  );
}