"use client";

import { motion } from "framer-motion";
import { ArrowRight01Icon } from "hugeicons-react";

interface MagneticButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}

export function MagneticButton({ children, variant = "primary" }: MagneticButtonProps) {
  const isPrimary = variant === "primary";

  return (
    <motion.button
      whileHover={{ y: -2 }}
      whileTap={{ y: 0, scale: 0.98 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className={`
        group relative inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full font-body font-medium text-sm cursor-pointer
        transition-shadow duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]
        ${
          isPrimary
            ? "bg-dark-contrast text-white shadow-lg hover:shadow-[0_24px_48px_-12px_rgba(26,47,36,0.3)]"
            : "bg-white text-primary border border-black/5 shadow-sm hover:shadow-[0_24px_48px_-12px_rgba(0,0,0,0.06)]"
        }
      `}
    >
      {children}
      {isPrimary && (
        <ArrowRight01Icon
          size={16}
          strokeWidth={1.5}
          className="transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:translate-x-1"
        />
      )}
    </motion.button>
  );
}
