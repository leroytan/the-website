"use client";
import ReviewCarousel from "@/components/ReviewCarousel";
import {
  Clock,
  CheckCircle,
  MessageCircle,
  CreditCard,
} from "lucide-react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import {
  motion,
  useMotionValue,
  useTransform,
} from "framer-motion";
import { useEffect, useState } from "react";
import { Button } from "@/components/button";

const universityLogos = [
  { src: "/images/National_University_of_Singapore_Logo.svg", alt: "NUS" },
  { src: "/images/Nanyang_Technological_University_Logo.svg", alt: "NTU" },
  { src: "/images/Singapore_Management_University_Logo.svg", alt: "SMU" },
  {
    src: "/images/Singapore_University_of_Technology_and_Design_Logo.svg",
    alt: "SUTD",
  },
  {
    src: "/images/Singapore_University_of_Social_Sciences_Logo.svg",
    alt: "SUSS",
  },
  { src: "/images/Singapore_Institute_of_Technology_Logo.svg", alt: "SIT" },
];

function UniversityLogoMarquee() {
  const x = useMotionValue(0);
  const [paused, setPaused] = useState(false);
  const LOGO_WIDTH = 112;
  const GAP = 80;
  const totalWidth = universityLogos.length * (LOGO_WIDTH + GAP);

  useEffect(() => {
    let animationFrame: number;
    const SPEED = 0.75;

    const loop = () => {
      if (!paused) {
        x.set((x.get() - SPEED) % totalWidth); // use modulo to wrap seamlessly
      }
      animationFrame = requestAnimationFrame(loop);
    };

    animationFrame = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animationFrame);
  }, [paused, x, totalWidth]);

  return (
    <div
      className="overflow-hidden w-full py-2"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <motion.div
        className="flex gap-20"
        style={{
          x: useTransform(x, (val) => `${val % totalWidth}px`),
        }}
      >
        {[...universityLogos, ...universityLogos].map((logo, idx) => (
          <div
            key={idx}
            className="relative w-28 h-12 flex-shrink-0 flex items-center justify-center"
            style={{ width: LOGO_WIDTH }}
          >
            <Image
              src={logo.src}
              alt={logo.alt}
              fill
              className="object-contain"
              draggable={false}
            />
          </div>
        ))}
      </motion.div>
    </div>
  );
}

export default function HomeContent() {
  const router = useRouter();

  return (
    <div className="bg-[#fff2de] min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background image with fade + blur mask */}
        <div className="absolute inset-0 z-0 pointer-events-none">
          <Image
            src="/images/hero-illustration.png"
            alt="Hero Illustration"
            fill
            priority
            quality={100}
            className="object-cover object-center"
            style={{
              maskImage:
                "linear-gradient(to bottom, black 70%, transparent 100%)",
              WebkitMaskImage:
                "linear-gradient(to bottom, black 70%, transparent 100%)",
              filter: "blur(0.5px)", // Optional: softens sharp edge
            }}
          />
        </div>

        {/* Main content */}
        <div className="relative z-10 flex justify-center px-4 py-24 sm:py-32">
          <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl p-6 sm:p-10 text-center max-w-2xl">
            <div className="flex justify-center items-center gap-3 mb-4">
              <Image
                src="/images/logo.svg"
                alt="THE Logo"
                width={100}
                height={100}
              />
              <h1 className="text-3xl sm:text-3xl md:text-3xl font-extrabold text-[#4a58b5]">
                Teach. <span className="text-[#fc6453]">Honour</span>. Excel
              </h1>
            </div>
            <p className="text-[#fc6453] uppercase font-medium tracking-wider text-sm mb-2">
              Your path to educational excellence
            </p>
            <p className="text-[#4a58b5] text-base sm:text-lg mb-6 font-medium">
              We connect you with top tutors from leading universities for a
              seamless, flexible, and secure learning experience.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Button
                onClick={() => router.push("/tutors")}
                className="bg-customYellow hover:bg-customOrange text-white text-lg font-semibold py-4 px-6 rounded-full shadow transition"
              >
                Find a Tutor
              </Button>
              <Button
                onClick={() => router.push("/signup")}
                className="bg-customYellow hover:bg-customOrange text-white text-lg font-semibold py-4 px-6 rounded-full shadow transition"
              >
                Become a Tutor
              </Button>
            </div>
          </div>
        </div>
      </section>
      {/* Tutors from Leading Universities */}
      <section className="py-12 bg-[#fff2de]">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <div className=" p-8">
            <h2 className="text-2xl font-bold text-[#4a58b5] mb-3">
              Tutors from Leading Universities
            </h2>
            <p className="text-[#4a58b5] text-sm sm:text-base mb-6">
              Our tutors are top-performing students and graduates from
              Singapore's best universities.
            </p>
            <UniversityLogoMarquee />
          </div>
        </div>
      </section>
      {/* Why Choose Us */}
      {/* Top curved mask */}

      <section className="relative bg-[url('/images/orange-backdrop.png')]">
        <div className="absolute top-0 left-0 w-full overflow-hidden">
          <svg
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
            className="relative block w-full h-[100px]"
            style={{
              transform: "rotateY(180deg)",
            }}
          >
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              fill="#fff2de"
            />
          </svg>
        </div>
        {/* Content */}
        <div className="relative py-20 min-h-screen flex items-center justify-center">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12 text-white">
              Why Choose Us?
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
              {[
                {
                  icon: Clock,
                  title: "Flexible Scheduling",
                  desc: "Learn when you want, how you want.",
                },
                {
                  icon: CheckCircle,
                  title: "Verified Tutors",
                  desc: "Every tutor is carefully screened.",
                },
                {
                  icon: MessageCircle,
                  title: "Chat Before You Book",
                  desc: "Ask questions and clarify upfront.",
                },
                {
                  icon: CreditCard,
                  title: "Secure Payment",
                  desc: "Pay only after your first session.",
                },
              ].map(({ icon: Icon, title, desc }) => (
                <div
                  key={title}
                  className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 flex flex-col items-center text-center transition-transform hover:scale-105 hover:shadow-lg"
                >
                  <div className="bg-[#fabb84]/20 rounded-full p-3 mb-3">
                    <Icon className="text-[#fabb84]" size={32} />
                  </div>
                  <h3 className="font-bold text-lg mb-1 text-[#4a58b5]">
                    {title}
                  </h3>
                  <p className="text-sm text-[#4a58b5]/90">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom curved mask */}
        <div className="absolute bottom-0 left-0 w-full overflow-hidden">
          <svg
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
            className="relative block w-full h-[100px]"
            style={{
              transform: "rotateX(180deg)",
            }}
          >
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              fill="#fff2de"
            />
          </svg>
        </div>
      </section>
      {/* Testimonials / Reviews */}
      <section className="py-20">
        <div className="max-w-3xl mx-auto px-4">
          <div className="flex items-center justify-center mb-6">
            <h2 className="text-2xl font-bold text-[#4a58b5] text-center">
              Testimonials & Reviews
            </h2>
          </div>
          <ReviewCarousel />
        </div>
      </section>
    </div>
  );
}
