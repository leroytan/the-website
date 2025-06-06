"use client";
import { useState, useEffect } from "react";

interface HorizontalLoaderProps {
  isLoading: boolean; // Controls when the loader is visible
  completionDelay?: number; // Optional delay before hiding the loader (default: 500ms)
}

export function HorizontalLoader({
  isLoading,
  completionDelay = 500,
}: HorizontalLoaderProps) {
  const [progress, setProgress] = useState(0); // Track progress
  const [showLoader, setShowLoader] = useState(false); // Control loader visibility

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isLoading) {
      setShowLoader(true); // Show the loader
      setProgress(0); // Reset progress
      interval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90)); // Increment progress up to 90%
      }, 200); // Update every 200ms
    } else if (showLoader) {
      setProgress(100); // Complete progress when loading is done
      setTimeout(() => setShowLoader(false), completionDelay); // Wait before hiding the loader
    }

    return () => clearInterval(interval); // Cleanup interval
  }, [isLoading, showLoader, completionDelay]);

  if (!showLoader) return null; // Don't render if the loader is not visible

  return (
    <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-200">
      <div
        className="h-full bg-customYellow transition-all duration-300"
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
}