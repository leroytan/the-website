import Image from "next/image";
export const UserImage = ({
  user,
  width,
  height,
}: {
  user: { photo_url?: string; name: string };
  width?: number;
  height?: number;
}) => {
  const hasSpecificDimensions = width !== undefined || height !== undefined;
  
  return (
    <Image
      src={user.photo_url || "/images/THE-guyprofilephoto.png"}
      alt={user.name}
      width={width || 80}
      height={height || 80}
      className={`rounded-full mr-4 border-2 border-[#fabb84] object-cover ${
        hasSpecificDimensions ? '' : 'w-full h-full'
      }`}
      style={hasSpecificDimensions ? { width: `${width}px`, height: `${height}px` } : {}}
    />
  );
};
