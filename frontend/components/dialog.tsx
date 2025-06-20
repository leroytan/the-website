import { ReactNode } from "react";
import { CheckCircle2 } from "lucide-react";

interface DialogProps {
  children: ReactNode;
  className?: string;
  variant?: "default" | "success";
  icon?: ReactNode;
  title?: string;
  message?: string;
  onClose?: () => void;
  onAction?: () => void;
  actionText?: string;
}

export function Dialog({
  children,
  className,
  variant = "default",
  icon,
  title,
  message,
  onClose,
  onAction,
  actionText
}: DialogProps) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[900]">
      <div className={`bg-white p-6 rounded-lg shadow-lg w-full md:w-1/2 ${className}`}>
        {variant === "success" ? (
          <div className="flex flex-col items-center text-center">
            {icon || <CheckCircle2 className="w-16 h-16 text-green-500 mb-4" />}
            {title && (
              <h3 className="text-xl font-semibold text-customDarkBlue mb-2">
                {title}
              </h3>
            )}
            {message && (
              <p className="text-gray-600 mb-6">
                {message}
              </p>
            )}
            {children}
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
}