'use client';

import BurgerMenu from './BurgerMenu';
import UserMenu from './UserMenu';
import { motion } from 'framer-motion';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

const Header = ({ toggleSubpage }: { toggleSubpage: () => void }) => {
  const router = useRouter();

  return (
    <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="container mx-auto px-4 py-2 sm:py-4 flex items-center justify-between">
        <BurgerMenu toggleSidebar={toggleSubpage} />
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => router.push('/')}
          className="cursor-pointer"
        >
          <Image
            src="/images/logo.png"
            alt="THE Logo"
            width={100}
            height={50}
            className="w-16 sm:w-20 md:w-24 lg:w-28"
          />
        </motion.div>
        <UserMenu />
      </div>
    </header>
  );
};

export default Header;
