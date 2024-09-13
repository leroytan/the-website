'use client'

import { Splide, SplideSlide } from "@splidejs/react-splide";
import { AutoScroll } from "@splidejs/splide-extension-auto-scroll";
import "@splidejs/splide/dist/css/splide.min.css";

import Brooklyn from '/PosterBrooklyn.png';
import Macao from '/PosterMacao.png';
import Navada from '/PosterNavada.png';

// Define the style for the images in the carousel
const imageStyle = {
  width: '447px',
  height: '664px',
  borderRadius: '20px',
  border: '1px solid #FFFFFF33',
};

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

function ReviewCarouselCard({ review }: { review: Review }) {
  return (
    <SplideSlide
      key={review.id}
      className="w-1/3 px-4"
    >
      <div className="bg-gray-100 rounded-lg shadow-md p-6 h-full">
        <p className="mb-4 text-lg">&ldquo;{review.text}&rdquo;</p>
        <p className="font-semibold">- {review.author}</p>
      </div>
    </SplideSlide>
  )
}

function CarouselGames() {
  return (
    <div className="relative flex h-full bg-white">
      <div className="container max-w-screen-xl mx-auto relative z-20 overflow-x-hidden">
        <Splide
          options={{
            type: "loop", // Loop back to the beginning when reaching the end
            reducedMotion: {
              interval: 4000,
              speed: 800,
              autoplay: "play"
            },
            rewindByDrag: true, // Allow rewinding by dragging
            arrows: false, // Hide navigation arrows
            pagination: false, // Hide pagination dots
            fixedWidth: '32%', // Fixed width for each slide
            gap: '3%', // Gap between slides
          }}
          // extensions={{ AutoScroll }} // Use the AutoScroll extension
        >
          {reviews.map((review, index) => (
            <ReviewCarouselCard review={review} key={index}/>
          ))}
        </Splide>
      </div>
    </div>
  );
}

export default CarouselGames;