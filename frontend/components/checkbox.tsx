import { motion } from "framer-motion";

function Checkbox({
  defaultChecked,
  checked,
  className,
  children,
  onChange,
  readonly
}: {
  defaultChecked?: boolean;
  checked?: boolean;
  className?: string;
  children?: React.ReactNode;
  onChange?: () => void;
  readonly?: boolean;
}) {
  return (
    <motion.label
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`flex items-center gap-2 cursor-pointer ${className}`}
    >
      <input
        type="checkbox"
        checked={checked}
        defaultChecked={checked === undefined ? defaultChecked : undefined}
        className={`${className} accent-customYellow w-5 h-5 rounded-full`}
        onChange={onChange}
        readOnly={readonly}
      />
      <span>{children}</span>
    </motion.label>
  );
}

export default Checkbox;