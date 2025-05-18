// components/ErrorDialog.tsx
"use client";

import { useError } from "@/context/errorContext";
import { Dialog } from "@/components/dialog";
import { Button } from "@/components/button";

const ErrorDialog = () => {
  const { error, setError } = useError();

  if (!error) return null;

  return (
    <Dialog>
      <div className="p-4">
        <h2 className="text-lg font-bold text-customOrange">Oops!</h2>
        <p className="mt-2 text-sm text-gray-700">{error}</p>
        <div className="flex justify-end mt-4">
          <Button onClick={() => setError(null)} className="px-4 py-2 bg-[#fabb84] text-white rounded-md hover:bg-[#fc6453] transition-colors duration-200">
            Close
          </Button>
        </div>
      </div>
    </Dialog>
  );
};

export default ErrorDialog;
