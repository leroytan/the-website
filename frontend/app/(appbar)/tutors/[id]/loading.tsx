"use client";

import { motion } from "framer-motion";

export default function Loading() {
  return (
    <motion.div className="min-h-screen bg-customLightYellow px-4 sm:px-8 md:px-16 lg:px-20 py-6 sm:py-8">
      {/* Top Profile Info Skeleton */}
      <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 md:p-10 flex flex-col sm:flex-row justify-center gap-6 relative animate-pulse">
        <div className="w-36 h-36 bg-gray-200 rounded-full border-4 border-[#fabb84]" />
        <div className="flex flex-col justify-center space-y-4">
          <div className="h-6 bg-gray-200 rounded w-48" />
          <div className="h-4 bg-gray-200 rounded w-32" />
          <div className="flex flex-wrap items-center space-x-3 mt-2">
            <div className="h-4 bg-gray-200 rounded w-20" />
            <div className="h-4 bg-gray-200 rounded w-16" />
          </div>
        </div>
      </div>

      {/* Bottom Section Skeleton */}
      <div className="mt-6 flex flex-col sm:flex-row gap-6 sm:gap-8">
        {/* About Me Skeleton */}
        <div className="w-full sm:w-1/4 bg-white shadow-lg rounded-xl p-4 sm:p-6 animate-pulse">
          <div className="h-5 bg-gray-200 rounded w-24 mb-4" />
          <div className="h-4 bg-gray-200 rounded w-full mb-2" />
          <div className="h-4 bg-gray-200 rounded w-5/6 mb-2" />
          <div className="h-4 bg-gray-200 rounded w-4/6" />
        </div>

        {/* Tabs and Content Skeleton */}
        <div className="w-full sm:w-3/4 bg-white shadow-lg rounded-xl p-4 sm:p-6 max-w-full break-words animate-pulse">
          {/* Tabs Skeleton */}
          <div className="flex flex-wrap justify-center sm:justify-start space-x-3 sm:space-x-6 border-b border-gray-200 pb-2 mb-4">
            <div className="h-6 bg-gray-200 rounded w-32" />
            <div className="h-6 bg-gray-200 rounded w-24" />
          </div>

          {/* Content Skeleton */}
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <div className="h-5 bg-gray-200 rounded w-36 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-full" />
              </div>
              <div>
                <div className="h-5 bg-gray-200 rounded w-36 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-full" />
              </div>
              <div>
                <div className="h-5 bg-gray-200 rounded w-36 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-full" />
              </div>
              <div>
                <div className="h-5 bg-gray-200 rounded w-36 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-full" />
              </div>
              <div>
                <div className="h-5 bg-gray-200 rounded w-36 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-full" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}