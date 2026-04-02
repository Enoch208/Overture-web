"use client";

import { useState } from "react";
import { motion, useMotionValueEvent, useScroll } from "framer-motion";

const navLinks = [
  { label: "How It Works", href: "#how-it-works" },
  { label: "Architecture", href: "#architecture" },
  { label: "Providers", href: "#providers" },
  { label: "Payers", href: "#payers" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const { scrollY } = useScroll();

  useMotionValueEvent(scrollY, "change", (latest: number) => {
    setScrolled(latest > 50);
  });

  return (
    <motion.header
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
      className="fixed top-0 left-0 right-0 z-50 flex justify-center"
    >
      <nav
        className={`
          flex items-center justify-between
          transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]
          will-change-[max-width,border-radius,background-color,box-shadow,padding,margin]
          ${
            scrolled
              ? "mt-3 max-w-5xl w-[94%] h-14 px-4 pl-6 gap-6 rounded-full bg-canvas-elevated/65 backdrop-blur-2xl border border-black/[0.06] shadow-[0_8px_32px_-8px_rgba(0,0,0,0.06)]"
              : "mt-0 max-w-7xl w-full h-16 px-8 gap-8 rounded-none bg-canvas-primary/80 backdrop-blur-xl border-b border-black/5"
          }
        `}
      >
        <a href="/" className="font-display text-xl tracking-tight text-primary shrink-0">
          Overture
        </a>

        <ul className="hidden md:flex items-center gap-6 shrink-0">
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-sm font-body font-medium text-secondary hover:text-primary transition-colors duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] whitespace-nowrap"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-2 shrink-0">
          <button className="hidden sm:inline-flex items-center justify-center rounded-full font-body font-medium text-sm px-6 py-2 text-secondary hover:text-primary transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] cursor-pointer whitespace-nowrap">
            Sign In
          </button>
          <button className="inline-flex items-center justify-center rounded-full font-body font-medium text-sm px-6 py-2 bg-dark-contrast text-white hover:shadow-[0_12px_24px_-6px_rgba(26,47,36,0.25)] transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] cursor-pointer whitespace-nowrap">
            Request Access
          </button>
        </div>
      </nav>
    </motion.header>
  );
}
