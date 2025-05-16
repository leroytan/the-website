import { motion } from "framer-motion";

function Checkbox({
  defaultChecked,
  className,
  children,
  onChange,
}: {
  defaultChecked: boolean;
  className?: string;
  children?: React.ReactNode;
  onChange?: () => void;
}) {
  return (
    <motion.label
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`flex items-center gap-2 cursor-pointer ${className}`}
    >
      <input
        type="checkbox"
        defaultChecked={defaultChecked}
        className={`${className} accent-customYellow w-5 h-5 rounded-full`}
        onChange={onChange}
      />
      <span>{children}</span>
    </motion.label>
  );
}

export default Checkbox;