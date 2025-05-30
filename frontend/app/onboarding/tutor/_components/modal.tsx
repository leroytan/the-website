import { Dialog } from "@/components/dialog";
import { Button } from "@/components/button";
import ImageCropper from "./imageCropper";
type ModalProps = {
  updateAvatar: (avatar: string | null) => void;
  closeModal: () => void;
};

const Modal = ({ updateAvatar, closeModal }: ModalProps) => {
  return (
    <Dialog>
      <h1 className="mb-4 text-lg font-bold text-customDarkBlue">
        Upload your profile picture
      </h1>
      <ImageCropper updateAvatar={updateAvatar} closeModal={closeModal} />

      <div className="flex justify-end space-x-2">
        <Button
          onClick={closeModal}
          className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
        >
          Cancel
        </Button>
      </div>
    </Dialog>
  );
};

export default Modal;
