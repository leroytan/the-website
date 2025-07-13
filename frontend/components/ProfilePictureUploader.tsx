"use client";

import { Button } from "@/components/button";
import { CloudUpload } from "lucide-react";
import { useRef, useState } from "react";
import Image from "next/image";
import { useError } from "@/context/errorContext";
import { useParams } from "next/navigation";
import { Dialog } from "@/components/dialog";
import { Button as DialogButton } from "@/components/button";
import Input from "@/components/input";
import "react-image-crop/dist/ReactCrop.css";
import ReactCrop, {
  centerCrop,
  convertToPixelCrop,
  makeAspectCrop,
  type PercentCrop,
} from "react-image-crop";
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatchClient";
import { useAuth } from "@/context/authContext";

const ASPECT_RATIO = 1;
const MIN_DIMENSION = 150;

interface ProfilePictureUploaderProps {
  photoUrl?: string;
}

const ProfilePictureUploader = ({ photoUrl }: ProfilePictureUploaderProps) => {
  const { setError } = useError();
  const { refetch } = useAuth();
  const [avatarUrl, setAvatarUrl] = useState<string>(photoUrl || "");
  const [modalOpen, setModalOpen] = useState(false);
  const oldAvatarUrl = useRef<string>("");
  const params = useParams();
  const tutorId = params.id;

  const updateAvatar = async (avatarDataUrl: string | null) => {
    if (!avatarDataUrl) return;

    // Store the current avatar before changing
    oldAvatarUrl.current = avatarUrl;
    setAvatarUrl(avatarDataUrl); // Show the new avatar immediately

    // Convert Data URL to Blob
    const res = await fetch(avatarDataUrl);
    const blob = await res.blob();
    console.log("Blob type: %s", blob.type); // Debugging line to check blob type
    // Prepare form data
    const formData = new FormData();
    formData.append("file", blob, "avatar." + blob.type.split("/")[1]); // Use the correct file extension

    // Upload to your API
    try {
      const response = await fetchWithTokenCheck(
        `/api/me/upload-profile-photo/`,
        {
          method: "POST",
          body: formData,
          credentials: "include",
        }
      );
      if (!response.ok) throw new Error("Upload failed");
      refetch(); // Refetch user data to update avatar URL
    } catch (err) {
      setError("Failed to upload avatar. Please try again later.");
      setAvatarUrl(oldAvatarUrl.current); // Revert to original on error
    }
  };

  return (
      <div className="flex flex-col items-center gap-2">
        <Image
          src={avatarUrl || "/images/THE-guyprofilephoto.png"}
          alt="Avatar"
          width={140}
          height={140}
          className="rounded-full border-4 border-customYellow"
        />
        <Button
          className="bg-customYellow text-white px-4 py-2 rounded-full text-sm flex items-center gap-2 hover:bg-customOrange transition-colors duration-200"
          onClick={() => {
            setModalOpen(true);
          }}
        >
          <CloudUpload className="w-6 h-auto mr-1" />
          Upload Profile Pic
        </Button>
        {modalOpen && (
          <Modal
            updateAvatar={updateAvatar}
            closeModal={() => setModalOpen(false)}
          />
        )}
      </div>
  );
};

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
        <DialogButton
          onClick={closeModal}
          className="px-4 py-2 bg-gray-200 text-[#4a58b5] rounded-md hover:bg-gray-300 transition-colors duration-200"
        >
          Cancel
        </DialogButton>
      </div>
    </Dialog>
  );
};

interface ImageCropperProps {
  closeModal: () => void;
  updateAvatar: (dataUrl: string) => void;
}

const ImageCropper = ({ closeModal, updateAvatar }: ImageCropperProps) => {
  const imgRef = useRef<HTMLImageElement>(null);
  const previewCanvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [imgSrc, setImgSrc] = useState("");
  const [crop, setCrop] = useState<PercentCrop>();
  const [error, setError] = useState("");
  const [imgType, setImgType] = useState<"image/png" | "image/jpeg">(
    "image/png"
  );

  const onSelectFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    setImgType(file.type === "image/jpeg" ? "image/jpeg" : "image/png");

    const reader = new FileReader();
    reader.addEventListener("load", () => {
      const imageElement = new window.Image();
      const imageUrl = reader.result?.toString() || "";
      imageElement.src = imageUrl;

      imageElement.addEventListener("load", (e: Event) => {
        if (error) setError("");
        const { naturalWidth, naturalHeight } =
          e.currentTarget as HTMLImageElement;
        if (naturalWidth < MIN_DIMENSION || naturalHeight < MIN_DIMENSION) {
          setError("Image must be at least 150 x 150 pixels.");
          return setImgSrc("");
        }
      });
      setImgSrc(imageUrl);
    });
    reader.readAsDataURL(file);
  };

  const onImageLoad = (e: { currentTarget: { width: any; height: any } }) => {
    const { width, height } = e.currentTarget;
    const cropWidthInPercent = (MIN_DIMENSION / width) * 100;

    const crop = makeAspectCrop(
      {
        unit: "%",
        width: cropWidthInPercent,
      },
      ASPECT_RATIO,
      width,
      height
    );
    const centeredCrop = centerCrop(crop, width, height);
    setCrop(centeredCrop);
  };

  return (
    <>
      <div className="mb-3 w-fit">
        <Button
          className="bg-customYellow text-white px-4 py-2 rounded-full text-sm flex items-center gap-2 hover:bg-customOrange duration-200"
          onClick={() => fileInputRef.current?.click()}
        >
          From Computer
        </Button>
        <Input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={onSelectFile}
          className="hidden"
          name="profilePhoto"
          placeholder={""}
          value={""}
        />
      </div>
      {error && <p className="text-red-400 text-xs">{error}</p>}
      {imgSrc && (
        <div className="flex flex-col items-center">
          <ReactCrop
            crop={crop}
            onChange={(pixelCrop, percentCrop) => setCrop(percentCrop)}
            circularCrop
            keepSelection
            aspect={ASPECT_RATIO}
            minWidth={MIN_DIMENSION}
          >
            <img
              ref={imgRef}
              src={imgSrc}
              alt="Upload"
              style={{ maxHeight: "70vh" }}
              onLoad={onImageLoad}
              fetchPriority="low"
              loading="lazy"
              decoding="async"
            />
          </ReactCrop>
          <Button
            className="bg-customYellow text-white mt-2 px-4 py-2 rounded-full text-sm flex items-center gap-2 hover:bg-customOrange transition-colors duration-200"
            onClick={() => {
              if (!crop) return;
              setCanvasPreview(
                imgRef.current!,
                previewCanvasRef.current!,
                convertToPixelCrop(
                  crop,
                  imgRef.current!.width,
                  imgRef.current!.height
                )
              );
              const dataUrl = previewCanvasRef.current
                ? previewCanvasRef.current.toDataURL(imgType, 0.92)
                : "";
              updateAvatar(dataUrl);
              closeModal();
            }}
          >
            <span>Upload Profile Pic</span>
          </Button>
        </div>
      )}
      {crop && (
        <canvas
          ref={previewCanvasRef}
          className="mt-4"
          style={{
            display: "none",
            border: "1px solid black",
            objectFit: "contain",
            width: 150,
            height: 150,
          }}
        />
      )}
    </>
  );
};
const setCanvasPreview = (
  image: { naturalWidth: number; width: number; naturalHeight: number; height: number; }, // HTMLImageElement
  canvas: { getContext: (arg0: string) => any; width: number; height: number; }, // HTMLCanvasElement
  crop: { width: number; height: number; x: number; y: number; } // PixelCrop
) => {
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("No 2d context");
  }

  // devicePixelRatio slightly increases sharpness on retina devices
  // at the expense of slightly slower render times and needing to
  // size the image back down if you want to download/upload and be
  // true to the images natural size.
  const pixelRatio = window.devicePixelRatio;
  const scaleX = image.naturalWidth / image.width;
  const scaleY = image.naturalHeight / image.height;

  canvas.width = Math.floor(crop.width * scaleX * pixelRatio);
  canvas.height = Math.floor(crop.height * scaleY * pixelRatio);

  ctx.scale(pixelRatio, pixelRatio);
  ctx.imageSmoothingQuality = "high";
  ctx.save();

  const cropX = crop.x * scaleX;
  const cropY = crop.y * scaleY;

  // Move the crop origin to the canvas origin (0,0)
  ctx.translate(-cropX, -cropY);
  ctx.drawImage(
    image,
    0,
    0,
    image.naturalWidth,
    image.naturalHeight,
    0,
    0,
    image.naturalWidth,
    image.naturalHeight
  );

  ctx.restore();
};
export default ProfilePictureUploader;
