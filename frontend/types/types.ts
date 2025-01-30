export interface ChatMessageProps {
    avatar: string;
    username: string;
    message: string;
    timestamp: string;
    hasCheckmark?: boolean;
    checkmarkIcon?: string;
  }
  
  export interface ChatSectionProps {
    title: string;
    children: React.ReactNode;
  }
  
  export interface SearchBarProps {
    icon: string;
  }