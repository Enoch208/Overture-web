"use client";

import { motion } from "framer-motion";

export function AgentBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-white border border-black/5 shadow-[0_8px_16px_-6px_rgba(0,0,0,0.02)]"
    >
      <div className="relative flex items-center justify-center w-2 h-2">
        <motion.span
          animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: [0.22, 1, 0.36, 1] }}
          className="absolute w-full h-full bg-emerald-500 rounded-full"
        />
        <span className="relative w-1.5 h-1.5 bg-emerald-500 rounded-full" />
      </div>
      <span className="font-mono text-xs uppercase tracking-[0.2em] text-primary font-medium">
        COIN Protocol Active
      </span>
    </motion.div>
  );
}
