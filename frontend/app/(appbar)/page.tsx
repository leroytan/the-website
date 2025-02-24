'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import ReviewCarousel from '@/components/ReviewCarousel';


export default function AppPage() {
  const router = useRouter();

  const handleRequestTutor = () => {
    router.push('/tutors');
  };

  const handleJoinUs = () => {
    router.push('/signup');
  };

  return (
    <div>
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="py-12 sm:py-16 md:py-20 bg-cover bg-center"
        style={{
          backgroundImage:
            "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Background%20Programmes%20(1)-uqKeIKQelD3tB85FeakeXgL048p4db.png')",
        }}
      >
        <div className="container mx-auto px-4 text-center">
          <motion.h2
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-3xl sm:text-4xl font-extrabold mb-4 sm:mb-6 text-[#4a58b5]"
          >
            Welcome to THE
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="mb-6 sm:mb-8 text-base sm:text-lg leading-relaxed text-[#4a58b5] font-medium"
          >
            <span className="font-bold">Teach . Honour . Excel</span> - Your
            path to educational excellence!
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-[#fabb84] text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-bold hover:bg-[#fc6453] transition-colors duration-200"
              onClick={handleRequestTutor}
            >
              Request a tutor
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-[#fabb84] text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-bold hover:bg-[#fc6453] transition-colors duration-200"
              onClick={handleJoinUs}
            >
              Join Us
            </motion.button>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
      >
        <div className="container mx-auto px-4">
          <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">
            Our Features
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            {[
              'Personalized Learning',
              'Expert Tutors',
              'Flexible Scheduling',
              'Interactive Sessions',
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                whileHover={{ scale: 1.03 }}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
              >
                <h3 className="text-lg sm:text-xl font-bold mb-3 text-[#4a58b5]">
                  {feature}
                </h3>
                <p className="text-[#4a58b5] text-sm sm:text-base">
                  We offer tailored educational experiences to help you excel
                  in your studies.
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Reviews Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="py-12 sm:py-16 md:py-20 bg-[#fff2de]"
      >
        <div className="container mx-auto px-4">
          <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-[#4a58b5] text-center">
            Student Reviews
          </h2>
          <ReviewCarousel />
        </div>
      </motion.section>
    </div>
  );
}
