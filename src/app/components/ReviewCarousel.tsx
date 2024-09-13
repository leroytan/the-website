// app/components/ReviewCarousel.tsx
'use client'

import { useState, useRef, useEffect } from 'react'

interface Review {
  id: number
  text: string
  author: string
}

const reviews: Review[] = [
  { id: 1, text: "Great service!", author: "Happy Customer 1" },
  { id: 2, text: "Awesome product!", author: "Happy Customer 2" },
  { id: 3, text: "Highly recommended!", author: "Happy Customer 3" },
  { id: 4, text: "Will use again!", author: "Happy Customer 4" },
  { id: 5, text: "Excellent experience!", author: "Happy Customer 5" },
  { id: 6, text: "Top-notch quality!", author: "Happy Customer 6" },
  { id: 7, text: "Exceeded expectations!", author: "Happy Customer 7" },
]

function ReviewCarouselCard({review} : {review: Review}) {
  return (
    <div
      key={review.id}
      className="w-1/3 px-4"
    >
      <div className="bg-gray-100 rounded-lg shadow-md p-6 h-full">
        <p className="mb-4 text-lg">&ldquo;{review.text}&rdquo;</p>
        <p className="font-semibold">- {review.author}</p>
      </div>
    </div>
  )
}

export default function ReviewCarousel() {
  const VIEW_SIZE = 3
  const TIMES_REPEAT = 10
  const TOTAL_LENGTH = TIMES_REPEAT * reviews.length
  const VIEW_LENGTH = TOTAL_LENGTH - VIEW_SIZE + 1

  const [currentIndex, setCurrentIndex] = useState(reviews.length * TIMES_REPEAT / 2)
  const carouselRef = useRef<HTMLDivElement>(null)

  function calcTransform(currentIndex: number)  {
    return `translateX(-${currentIndex * (100 / TOTAL_LENGTH
    )}%)`
  }

  function calcTotalWidth() {
    return `${(TOTAL_LENGTH / VIEW_SIZE) * 100}%`
  }

  useEffect(() => {
    const interval = setInterval(() => {
      nextReview()
    }, 3000) // Rotate every 3 seconds

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (carouselRef.current) {
      carouselRef.current.style.transform = calcTransform(currentIndex)
    }
  }, [currentIndex])

  const nextReview = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % VIEW_LENGTH)
  }

  const prevReview = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + VIEW_LENGTH) % VIEW_LENGTH)
  }

  return (
    <div className="relative overflow-hidden">
      <div
        ref={carouselRef}
        className="flex transition-trnansform duration-500 ease-in-out"
        style={{ width: calcTotalWidth(), transform: calcTransform(currentIndex) }}
      >
       {[...Array(TIMES_REPEAT)].map((_, i) => 
        reviews.map((currentReview) => (
          <ReviewCarouselCard review={currentReview}/>
        )))}
      </div>
      <button
        onClick={prevReview}
        className="absolute top-1/2 left-0 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-md"
      >
        <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button
        onClick={nextReview}
        className="absolute top-1/2 right-0 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-md"
      >
        <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  )
}