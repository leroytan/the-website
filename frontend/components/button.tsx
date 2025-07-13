import { motion } from "framer-motion";

export function Button({
    children,
    className,
    disabled,
    onClick,
    type,
    loading = false
  }: {
    children: React.ReactNode;
    className?: string;
    disabled?: boolean;
    onClick?: () => void;
    type?: "button" | "submit" | "reset";
    loading?: boolean;
    
  }) {
    const isDisabled = disabled || loading;
    
    return (
      <motion.button
        type={type? type : "button"}
        whileHover={!isDisabled ? { scale: 1.05 } : undefined}
        whileTap={!isDisabled ? { scale: 0.95 } : undefined}
        className={`${isDisabled ? 'opacity-50 cursor-not-allowed' : ''} ${loading ? `${className}  bg-gray-400` : className}`}
        onClick={onClick}
        disabled={isDisabled}
        style={loading ? { backgroundColor: '#9ca3af', cursor: 'not-allowed'  }  : {}}
      >
        <div className={`relative flex items-center justify-center ${loading ? 'opacity-60 cursor-not-allowed' : ''}`}>
          {children}
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            </div>
          )}
        </div>
      </motion.button>
    );
  }