'use client';

import { motion } from 'framer-motion';
import { Menu } from 'lucide-react';

const BurgerMenu = ({ toggleSidebar }: { toggleSidebar: () => void }) => (
  <motion.button
    initial={false}
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.9 }}
    onClick={toggleSidebar}
    className="text-[#4a58b5]"
  >
    <Menu size={24} />
  </motion.button>
);

export default BurgerMenu;
