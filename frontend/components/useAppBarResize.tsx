import { useEffect, useState } from "react";

const useAppBarResize = () => {
    const [availableHeight, setAvailableHeight] = useState<number>();
    useEffect(() => {
        const handleResize = () => {
          // Subtract the height of the app bar dynamically
          const appBarHeight = document.getElementById("appbar")?.offsetHeight || 0;
          setAvailableHeight(window.innerHeight - appBarHeight);
        };
    
        // Initial calculation and add event listener
        handleResize();
        window.addEventListener("resize", handleResize);
    
        return () => window.removeEventListener("resize", handleResize);
      }, []);
    return ( availableHeight );
    
}
 
export default useAppBarResize;