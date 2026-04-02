import { ReactNode } from "react";

interface OvertureButtonProps {
  children: ReactNode;
  variant?: "primary" | "secondary";
  href?: string;
  className?: string;
}

export function OvertureButton({ children, variant = "primary", href, className = "" }: OvertureButtonProps) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full font-body font-medium transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] cursor-pointer";

  const variants = {
    primary:
      "bg-dark-contrast text-white px-8 py-4 hover:scale-105 hover:shadow-[0_24px_48px_-12px_rgba(0,0,0,0.12)]",
    secondary:
      "bg-transparent text-primary border border-black/10 px-8 py-4 hover:bg-black/[0.03] hover:scale-105",
  };

  const classes = `${base} ${variants[variant]} ${className}`;

  if (href) {
    return (
      <a href={href} className={classes}>
        {children}
      </a>
    );
  }

  return <button className={classes}>{children}</button>;
}
