import Image from "next/image";

export const UserImage = ({
  user,
  width,
  height,
}: {
  user: { photo_url?: string; name: string; gender?: string | null };
  width?: number;
  height?: number;
}) => {
  const hasSpecificDimensions = width !== undefined || height !== undefined;
  
  // Determine default profile picture based on gender
  const getDefaultProfilePicture = () => {
    if (user.gender === "FEMALE") {
      return "/images/THE-girlprofilephoto.png";
    }
    return "/images/THE-guyprofilephoto.png";
  };
  
  return (
    <Image
      src={user.photo_url || getDefaultProfilePicture()}
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
