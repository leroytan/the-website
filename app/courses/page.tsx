'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { CheckCircle, ArrowRight } from 'lucide-react';
import { Inter } from 'next/font/google';
import Header from '../components/Header';

const inter = Inter({ subsets: ['latin'] });

type Course = {
  id: number;
  title: string;
  description: string;
  progress: number;
  completed: boolean;
  totalModules: number;
  completedModules: number;
};

const course: Course = {
  id: 1,
  title: 'PSLE English',
  description: 'Master English language skills and prepare effectively for PSLE examination.',
  progress: 0,
  completed: false,
  totalModules: 8,
  completedModules: 0,
};

const CourseCard = ({ course }: { course: Course }) => {
  const router = useRouter();

  const handleContinueCourse = () => {
    router.push(`/courses/psle-english/module`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
    >
      <h3 className="text-xl font-bold mb-2 text-[#4a58b5]">{course.title}</h3>
      <p className="text-[#4a58b5] mb-4">{course.description}</p>
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-[#4a58b5]">Progress</span>
          <span className="text-sm font-medium text-[#4a58b5]">{course.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-[#fabb84] h-2.5 rounded-full"
            style={{ width: `${course.progress}%` }}
          ></div>
        </div>
      </div>
      {course.completed ? (
        <div className="flex justify-between items-center">
          <span className="text-green-500 font-medium flex items-center">
            <CheckCircle size={20} className="mr-2" />
            Completed
          </span>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-[#4a58b5] text-white px-4 py-2 rounded-md hover:bg-[#3a4795] transition-colors duration-200 text-sm font-medium"
          >
            Get Certificate
          </motion.button>
        </div>
      ) : (
        <div className="flex justify-end">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleContinueCourse}
            className="bg-[#fabb84] text-white px-4 py-2 rounded-full hover:bg-[#fc6453] transition-colors duration-200 text-sm font-medium flex items-center"
          >
            Continue
            <ArrowRight size={16} className="ml-2" />
          </motion.button>
        </div>
      )}
    </motion.div>
  );
};

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  return (
    <div className={`min-h-screen bg-[#fff2de] ${inter.className}`}>
      <main className="pt-16 sm:pt-20 md:pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <CourseCard course={course} />
          </div>
        </div>
      </main>
    </div>
  );
}
