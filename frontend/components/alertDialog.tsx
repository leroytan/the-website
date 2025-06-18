// components/AlertDialog.tsx
"use client";

import { useAlert } from "@/context/alertContext";
import { Dialog } from "@/components/dialog";
import { Button } from "@/components/button";

const AlertDialog = () => {
  const { alert, setAlert } = useAlert();

  if (!alert) return null;

  return (
    <Dialog>
      <div className="p-4">
        <h2 className="text-lg font-bold text-customGreen">Alert!</h2>
        <p className="mt-2 text-sm text-gray-700">{alert}</p>
        <div className="flex justify-end mt-4">
          <Button onClick={() => setAlert(null)} className="px-4 py-2 bg-[#a7f3d0] text-white rounded-md hover:bg-[#34d399] transition-colors duration-200">
            Close
          </Button>
        </div>
      </div>
    </Dialog>
  );
};

export default AlertDialog;