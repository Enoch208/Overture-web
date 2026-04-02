"use client";

import { useState } from "react";
import Image from "next/image";
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
      className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-6 pointer-events-none"
    >
      <nav
        className={`
          pointer-events-auto flex items-center justify-between rounded-full
          transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]
          ${
            scrolled
              ? "w-[90%] max-w-4xl h-14 px-4 pl-6 gap-6 bg-canvas-elevated/70 backdrop-blur-2xl border border-black/[0.06] shadow-[0_8px_32px_-8px_rgba(0,0,0,0.06)]"
              : "w-[90%] max-w-5xl h-14 px-6 pl-8 gap-8 bg-canvas-elevated/40 backdrop-blur-xl border border-black/[0.04]"
          }
        `}
      >
        <a href="/" className="shrink-0 flex items-center">
          <Image
            src="/overture-logo.png"
            alt="Overture"
            width={120}
            height={36}
            className="h-7 w-auto"
            priority
          />
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
