import { motion } from "framer-motion";

export function Button({
    children,
    className,
    onClick,
  }: {
    children: React.ReactNode;
    className?: string;
    onClick: () => void;
  }) {
    return (
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`px-4 py-2 rounded-lg shadow-md ${className}`}
        onClick={onClick}
      >
        {children}
      </motion.button>
    );
  }