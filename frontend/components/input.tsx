function Input({
  type,
  name,
  placeholder,
  value,
  onChange,
  required,
  ref,
  className,
}: {
  type: string;
  name: string;
  placeholder: string;
  value: any;
  accept?: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
  ref?: React.RefObject<HTMLInputElement>;
  className?: string;
}) {
  return (
    <input
      ref={ref}
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      required={required}
      className={`w-full border px-3 py-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#fabb84] ${className}`}
    />
  );
}

export default Input;