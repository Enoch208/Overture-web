"use client";

import { motion } from "framer-motion";
import { AgentBadge } from "@/components/ui/agent-badge";
import { MagneticButton } from "@/components/ui/magnetic-button";

const customEase: [number, number, number, number] = [0.22, 1, 0.36, 1];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, ease: customEase },
  },
};

export function Hero() {
  return (
    <section className="relative w-full min-h-screen bg-canvas-primary flex flex-col items-center justify-center px-6 pt-32 pb-0 overflow-hidden">
      {/* ── Ambient Background Glow ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {/* Sage/emerald glow — echoes the "Headache." italic color */}
        <div className="absolute top-[15%] left-[30%] w-[700px] h-[500px] rounded-full bg-emerald-200/15 blur-[150px]" />
        {/* White volumetric light — focal center */}
        <div className="absolute top-[10%] left-1/2 -translate-x-1/2 w-[900px] h-[600px] rounded-full bg-white/50 blur-[150px]" />
        {/* Subtle warm accent — right side */}
        <div className="absolute top-[25%] right-[20%] w-[400px] h-[400px] rounded-full bg-emerald-100/10 blur-[120px]" />
      </div>

      {/* ── Hero Text ── */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 max-w-4xl mx-auto flex flex-col items-center text-center"
      >
        <motion.div variants={itemVariants} className="mb-10">
          <AgentBadge />
        </motion.div>

        <motion.h1
          variants={itemVariants}
          className="font-display text-[4rem] leading-[1.05] tracking-tight text-primary md:text-[6rem] lg:text-[7rem] max-w-5xl"
        >
          Automating the $35B <br />
          <span className="italic text-dark-contrast pr-4">Headache.</span>
        </motion.h1>

        <motion.p
          variants={itemVariants}
          className="mt-8 max-w-2xl font-body text-lg md:text-xl text-secondary leading-relaxed"
        >
          Meet Overture. A multi-agent system that handles the cross-organizational
          negotiation of prior authorizations in seconds, not days.
        </motion.p>

        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center gap-4 mt-12"
        >
          <MagneticButton variant="primary">Watch the Demo</MagneticButton>
          <MagneticButton variant="secondary">Read the Architecture</MagneticButton>
        </motion.div>
      </motion.div>

      {/* ── Hero Anchor — Glassmorphic Protocol Card ── */}
      <motion.div
        initial={{ opacity: 0, y: 80 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.2, delay: 0.8, ease: customEase }}
        className="relative z-10 mt-24 w-full max-w-4xl mx-auto"
      >
        {/* Glow behind the card */}
        <div className="absolute -inset-8 bg-dark-contrast/5 rounded-[40px] blur-[60px] pointer-events-none" />

        <div className="relative bg-dark-contrast/95 backdrop-blur-xl rounded-3xl border border-white/[0.08] overflow-hidden shadow-[0_40px_80px_-20px_rgba(0,0,0,0.25)]">
          {/* Subtle top highlight */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[60%] h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />

          <div className="p-8 md:p-10">
            {/* Terminal header dots */}
            <div className="flex items-center gap-2 mb-6">
              <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
              <div className="w-3 h-3 rounded-full bg-[#FEBC2E]" />
              <div className="w-3 h-3 rounded-full bg-[#28C840]" />
              <span className="ml-3 font-mono text-[11px] text-white/30 uppercase tracking-widest">
                overture / agent-orchestrator
              </span>
            </div>

            {/* Animated protocol lines */}
            <div className="space-y-3">
              <ProtocolLine delay={1.0} label="provider_agent" status="connected" />
              <ProtocolLine delay={1.2} label="fhir_bundler" status="assembling" detail="12 resources" />
              <ProtocolLine delay={1.4} label="payer_rules_engine" status="evaluating" detail="criteria: met" />
              <ProtocolLine delay={1.6} label="a2a_negotiation" status="active" detail="COIN protocol" />
              <ProtocolLine delay={1.8} label="determination" status="approved" detail="47.2s" />
            </div>

            {/* Bottom status bar */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 2.2, duration: 0.6, ease: customEase }}
              className="mt-8 pt-6 border-t border-white/[0.06] flex items-center justify-between"
            >
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400" />
                <span className="font-mono text-[11px] text-emerald-400/80 uppercase tracking-widest">
                  PA Approved
                </span>
              </div>
              <span className="font-mono text-[11px] text-white/20">
                latency: 47.2s &middot; confidence: 0.97
              </span>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Bottom fade — blends card into next section */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-canvas-primary to-transparent pointer-events-none z-20" />
    </section>
  );
}

/* ─── Protocol Line Sub-component ─── */

function ProtocolLine({
  delay,
  label,
  status,
  detail,
}: {
  delay: number;
  label: string;
  status: string;
  detail?: string;
}) {
  const statusColor =
    status === "approved"
      ? "text-emerald-400"
      : status === "active"
        ? "text-emerald-400/70"
        : status === "connected"
          ? "text-white/40"
          : "text-white/30";

  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className="flex items-center gap-4 font-mono text-sm"
    >
      <span className="text-white/20 select-none">→</span>
      <span className="text-white/50">{label}</span>
      <span className={`${statusColor}`}>{status}</span>
      {detail && (
        <span className="text-white/15 ml-auto">{detail}</span>
      )}
    </motion.div>
  );
}
