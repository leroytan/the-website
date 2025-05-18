"use client";
import "react-image-crop/dist/ReactCrop.css";
import { useRef, useState } from "react";
import ReactCrop, {
  centerCrop,
  convertToPixelCrop,
  makeAspectCrop,
  type PercentCrop,
} from "react-image-crop";
import setCanvasPreview from "./setCanvasPreview";
import Input from "@/components/input";
import { Button } from "@/components/button";

const ASPECT_RATIO = 1;
const MIN_DIMENSION = 150;

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

  const onSelectFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];

    const reader = new FileReader();
    reader.addEventListener("load", () => {
      const imageElement = new Image();
      const imageUrl = reader.result?.toString() || "";
      imageElement.src = imageUrl;

      imageElement.addEventListener("load", (e) => {
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
            />
          </ReactCrop>
          <Button
            className="bg-customYellow text-white mt-2 px-4 py-2 rounded-full text-sm flex items-center gap-2 hover:bg-customOrange transition-colors duration-200"
            onClick={() => {
              if (!crop) return;
              setCanvasPreview(
                imgRef.current!, // HTMLImageElement
                previewCanvasRef.current!, // HTMLCanvasElement
                convertToPixelCrop(
                  crop,
                  imgRef.current!.width,
                  imgRef.current!.height
                )
              );
              const dataUrl = previewCanvasRef.current
                ? previewCanvasRef.current.toDataURL()
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
export default ImageCropper;
