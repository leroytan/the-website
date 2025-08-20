"use client";

import { useRef, useEffect, useState } from "react";
import TermsAndConditions from "@/components/TermsDialog/TermsAndConditions";
import { Button } from "@/components/button";
import { Dialog } from "@/components/dialog";

interface TermsDialogProps {
  open: boolean;
  onClose: () => void;
  onAgree?: () => void;
  agreed?: boolean;
  requireAgree?: boolean; // If true, show agree button and require scroll
}


const TermsDialog: React.FC<TermsDialogProps> = ({ open, onClose, onAgree, agreed = false, requireAgree = true }) => {
  const [scrolled, setScrolled] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);

  // Handler to check if T&C dialog has been scrolled to bottom
  function handleScroll(e: React.UIEvent<HTMLDivElement>) {
    if (!requireAgree) return;
    const el = e.currentTarget;
    if (!scrolled && el.scrollTop + el.clientHeight >= el.scrollHeight - 2) {
      setScrolled(true);
    }
  }

  // Reset scrolled when dialog opens, but only if not already agreed
  useEffect(() => {
    if (open && requireAgree && !agreed) {
      setScrolled(false);
    }
  }, [open, agreed, requireAgree]);

  if (!open) return null;

  return (
    <Dialog>
      <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Terms and Conditions</h3>
      <div
        ref={dialogRef}
        onScroll={handleScroll}
        className="flex-1 min-h-0 overflow-y-auto border rounded-md p-4 bg-gray-50 w-full mb-4"
        tabIndex={0}
        aria-label="Terms and Conditions Dialog"
        style={{ maxHeight: "60vh" }}
      >
        <TermsAndConditions />
      </div>
      <div className="flex gap-2 w-full justify-end">
        {requireAgree ? (
          !agreed ? (
            <Button
              className={`px-4 py-2 bg-[#fabb84] text-white rounded-full transition-colors duration-200 ${scrolled ? "hover:bg-[#fc6453] cursor-pointer" : "opacity-60 cursor-not-allowed"}`}
              onClick={() => {
                if (onAgree) onAgree();
                onClose();
              }}
              type="button"
              disabled={!scrolled}
            >
              I agree
            </Button>
          ) : (
            <span className="px-4 py-2 text-green-600 font-semibold">You have agreed to the T&amp;C</span>
          )
        ) : null}
        <Button
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors duration-200"
          onClick={onClose}
          type="button"
        >
          Close
        </Button>
      </div>
      {requireAgree && !scrolled && !agreed && (
        <span className="mt-2 text-xs text-gray-400">
          Scroll to bottom to enable 'I agree'
        </span>
      )}
    </Dialog>
  );
};

export default TermsDialog;
