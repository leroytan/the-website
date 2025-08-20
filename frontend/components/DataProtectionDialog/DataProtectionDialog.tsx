'use client';
import { Dialog } from "@/components/dialog";
import DataProtectionPolicy from "./DataProtectionPolicy";
import { Button } from "@/components/button";

interface DataProtectionDialogProps {
  open: boolean;
  onClose: () => void;
}

const DataProtectionDialog: React.FC<DataProtectionDialogProps> = ({ open, onClose }) => {
  if (!open) return null;
  return (
    <Dialog>
      <h3 className="text-lg font-semibold text-[#4a58b5] mb-2">Data Protection & Privacy Policy</h3>
      <div className="flex-1 min-h-0 overflow-y-auto border rounded-md p-4 bg-gray-50 w-full mb-4" style={{ maxHeight: "60vh" }}>
        <DataProtectionPolicy />
      </div>
      <div className="flex gap-2 w-full justify-end">
        <Button
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors duration-200"
          onClick={onClose}
          type="button"
        >
          Close
        </Button>
      </div>
    </Dialog>
  );
};

export default DataProtectionDialog;
