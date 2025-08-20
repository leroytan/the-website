'use client';
interface ToggleSwitchProps {
  options: [string, string];
  value: string;
  onChange: (value: string) => void;
  label?: string;
  disabled?: boolean;
  className?: string;
}

const ToggleSwitch: React.FC<ToggleSwitchProps> = ({
  options,
  value,
  onChange,
  label,
  disabled = false,
  className = "",
}) => {
  const [left, right] = options;
  const isLeft = value === left;
  return (
    <div className={`inline-flex items-center select-none ${className}`}>
      {label && <span className="mr-2 text-md font-medium text-[#4a58b5]">{label}</span>}
      <div
        className={`relative min-w-max bg-[#f3e7d6] rounded-full flex items-center px-1 border-2 border-[#fabb84] shadow-sm ${disabled ? 'opacity-50' : ''}`}
        style={{ height: '2.5rem', paddingLeft: 4, paddingRight: 4 }}
      >
        {/* Thumb */}
        <div
          
        >
        </div>
        {/* Options */}
        <button
          type="button"
          className={`z-10 h-8 px-4 flex items-center justify-center rounded-full text-base font-semibold transition-colors duration-200 ${isLeft ? 'text-white bg-[#fabb84]' : 'text-[#4a58b5] bg-transparent'} ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
          onClick={() => !disabled && onChange(left)}
          disabled={disabled}
          style={{ borderRadius: '9999px', position: 'relative', zIndex: 2 }}
        >
          {left}
        </button>
        <button
          type="button"
          className={`z-10 h-8 px-4 flex items-center justify-center rounded-full text-base font-semibold transition-colors duration-200 ${!isLeft ? 'text-white bg-[#fabb84]' : 'text-[#4a58b5] bg-transparent'} ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
          onClick={() => !disabled && onChange(right)}
          disabled={disabled}
          style={{ borderRadius: '9999px', position: 'relative', zIndex: 2 }}
        >
          {right}
        </button>
      </div>
    </div>
  );
};

export default ToggleSwitch;
