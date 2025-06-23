'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Quote } from 'lucide-react';

const reviews = [
  { id: 1, text: "T.H.E. tutors have been instrumental in my academic growth. Their patience and expertise are unmatched.", author: "Emily S.", grade: "11th Grade" },
  { id: 2, text: "The personalized approach to learning has boosted my confidence in subjects I once struggled with.", author: "Michael L.", grade: "9th Grade" },
  { id: 3, text: "Flexible scheduling and top-notch instructors make T.H.E. the perfect choice for busy students.", author: "Sarah K.", grade: "12th Grade" },
  { id: 4, text: "I've seen a significant improvement in my grades since starting with T.H.E. Highly recommended!", author: "David W.", grade: "10th Grade" },
];

const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 1000 : -1000,
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 1000 : -1000,
    opacity: 0,
  }),
};

const ReviewCarousel = () => {
  const [currentReview, setCurrentReview] = useState(0);
  const [direction, setDirection] = useState(0);

  const nextReview = useCallback(() => {
    setDirection(1);
    setCurrentReview((prev) => (prev + 1) % reviews.length);
  }, []);

  const prevReview = useCallback(() => {
    setDirection(-1);
    setCurrentReview((prev) => (prev - 1 + reviews.length) % reviews.length);
  }, []);

  useEffect(() => {
    const interval = setInterval(nextReview, 5000);
    return () => clearInterval(interval);
  }, [nextReview]);

  return (
    <div className="relative w-full max-w-4xl mx-auto px-4 py-12" aria-live="polite">
      <div className="bg-white rounded-lg shadow-md overflow-visible relative">
        {/* Quote icon hanging outside */}
        <Quote 
          className="absolute -top-8 -left-8 text-[#fabb84] opacity-60 z-0"
          aria-hidden="true"
          color="#fabb84"
          fill="#fabb84"
          style={{ transform: 'rotate(180deg)' }}
          size={70}
        />
        {/* Review content clipped to card */}
        <div className="relative overflow-hidden h-[200px] sm:h-[180px] z-10">
          <AnimatePresence initial={false} custom={direction} mode="wait">
            <motion.div
              key={currentReview}
              custom={direction}
              variants={variants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="absolute inset-0 flex flex-col justify-center p-6 sm:p-8 z-10"
              aria-live="assertive"
            >
              <p className="text-[#4a58b5] mb-4 text-base sm:text-lg italic">{reviews[currentReview].text}</p>
              <div className="flex justify-between items-center">
                <p className="font-semibold text-[#fc6453] text-sm sm:text-base">- {reviews[currentReview].author}</p>
                <p className="text-[#fabb84] text-xs sm:text-sm">{reviews[currentReview].grade}</p>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {reviews.map((_, index) => (
          <button
            key={index}
            onClick={() => {
              setDirection(index > currentReview ? 1 : -1);
              setCurrentReview(index);
            }}
            className={`w-2 h-2 rounded-full transition-colors duration-200 ${
              index === currentReview ? 'bg-[#fc6453]' : 'bg-[#fabb84] hover:bg-[#fc6453]'
            }`}
            aria-label={`Go to review ${index + 1}`}
          />
        ))}
      </div>
      <button
        onClick={prevReview}
        className="absolute top-1/2 left-0 transform -translate-y-1/2 bg-white text-[#4a58b5] p-2 rounded-full shadow-md hover:bg-[#fabb84] hover:text-white transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[#fc6453] focus:ring-opacity-50"
        aria-label="Previous review"
      >
        <ChevronLeft size={20} />
      </button>
      <button
        onClick={nextReview}
        className="absolute top-1/2 right-0 transform -translate-y-1/2 bg-white text-[#4a58b5] p-2 rounded-full shadow-md hover:bg-[#fabb84] hover:text-white transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[#fc6453] focus:ring-opacity-50"
        aria-label="Next review"
      >
        <ChevronRight size={20} />
      </button>
    </div>
  );
};

export default ReviewCarousel;
