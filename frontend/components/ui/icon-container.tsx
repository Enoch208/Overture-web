import { ReactNode } from "react";

interface IconContainerProps {
  children: ReactNode;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizes = {
  sm: "w-10 h-10",
  md: "w-12 h-12",
  lg: "w-16 h-16",
};

export function IconContainer({ children, size = "md", className = "" }: IconContainerProps) {
  return (
    <div
      className={`${sizes[size]} rounded-full bg-slate-50 flex items-center justify-center ${className}`}
    >
      {children}
    </div>
  );
}
