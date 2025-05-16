import { motion } from "framer-motion";

export function Button({
    children,
    className,
    disabled,
    onClick,
  }: {
    children: React.ReactNode;
    className?: string;
    disabled?: boolean;
    onClick: () => void;
  }) {
    return (
      <motion.button
        type="button"
        whileHover={!disabled ? { scale: 1.05 } : undefined}
        whileTap={!disabled ? { scale: 0.95 } : undefined}
        className={`${className}`}
        onClick={onClick}
        disabled={disabled}
      >
        {children}
      </motion.button>
    );
  }