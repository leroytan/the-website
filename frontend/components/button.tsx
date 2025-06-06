import { motion } from "framer-motion";

export function Button({
    children,
    className,
    disabled,
    onClick,
    type
  }: {
    children: React.ReactNode;
    className?: string;
    disabled?: boolean;
    onClick?: () => void;
    type?: "button" | "submit" | "reset";
    
  }) {
    return (
      <motion.button
        type={type? type : "button"}
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