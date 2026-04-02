"use client";

import { motion } from "framer-motion";

const customEase: [number, number, number, number] = [0.22, 1, 0.36, 1];

function TerminalChrome({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="relative bg-dark-contrast/95 rounded-2xl border border-white/[0.08] overflow-hidden shadow-[0_24px_48px_-12px_rgba(0,0,0,0.2)] h-full">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[50%] h-px bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="flex items-center gap-2 px-6 py-3 border-b border-white/[0.06]">
        <div className="w-2.5 h-2.5 rounded-full bg-[#FF5F57]" />
        <div className="w-2.5 h-2.5 rounded-full bg-[#FEBC2E]" />
        <div className="w-2.5 h-2.5 rounded-full bg-[#28C840]" />
        <span className="ml-2 font-mono text-[10px] text-white/25 uppercase tracking-widest">{title}</span>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

function Line({ label, value, accent, delay }: { label: string; value: string; accent?: boolean; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.5, ease: customEase }}
      className="flex items-center justify-between font-mono text-xs"
    >
      <span className="text-white/40">{label}</span>
      <span className={accent ? "text-emerald-400" : "text-white/60"}>{value}</span>
    </motion.div>
  );
}

/* ── Step 1: Order Triggers PA ── */
export function StepTrigger() {
  return (
    <TerminalChrome title="ehr / clinical-order">
      <div className="space-y-4">
        <Line delay={0.1} label="patient" value="Sarah Chen, 42F" />
        <Line delay={0.2} label="order" value="MRI Shoulder (73221)" />
        <Line delay={0.3} label="icd-10" value="M75.110" />
        <Line delay={0.4} label="payer" value="Anthem Blue Cross" />
        <div className="border-t border-white/[0.06]" />
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6, duration: 0.5, ease: customEase }}
          className="flex items-center gap-2"
        >
          <motion.div
            animate={{ scale: [1, 1.4, 1], opacity: [0.5, 0, 0.5] }}
            transition={{ duration: 2, repeat: Infinity, ease: [0.22, 1, 0.36, 1] }}
            className="w-2 h-2 bg-emerald-400 rounded-full"
          />
          <span className="font-mono text-xs text-emerald-400">PA REQUIRED — agent triggered</span>
        </motion.div>
      </div>
    </TerminalChrome>
  );
}

/* ── Step 2: Evidence Assembly ── */
export function StepEvidence() {
  const resources = [
    { type: "Condition", desc: "Rotator cuff tear", status: "pulled" },
    { type: "Observation", desc: "MRI prior imaging", status: "pulled" },
    { type: "Procedure", desc: "8wk PT completed", status: "pulled" },
    { type: "DocumentRef", desc: "Ortho consult note", status: "pulled" },
  ];

  return (
    <TerminalChrome title="mcp / evidence-bundler">
      <div className="space-y-4">
        {resources.map((r, i) => (
          <motion.div
            key={r.type}
            initial={{ opacity: 0, x: -8 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15 + 0.1, duration: 0.5, ease: customEase }}
            className="flex items-center gap-4 font-mono text-xs"
          >
            <span className="px-2 py-1 rounded bg-white/[0.06] text-white/30 text-[10px]">{r.type}</span>
            <span className="text-white/50 flex-1">{r.desc}</span>
            <span className="text-emerald-400">✓</span>
          </motion.div>
        ))}
        <div className="border-t border-white/[0.06]" />
        <Line delay={0.8} label="bundle" value="4 resources compiled" accent />
      </div>
    </TerminalChrome>
  );
}

/* ── Step 3: Criteria Matching ── */
export function StepCriteria() {
  const criteria = [
    { rule: "Conservative tx ≥ 6 weeks", evidence: "8 weeks PT", match: true },
    { rule: "Imaging supports diagnosis", evidence: "MRI confirmed", match: true },
    { rule: "Specialist referral", evidence: "Ortho consult", match: true },
  ];

  return (
    <TerminalChrome title="mcp / rules-engine">
      <div className="space-y-4">
        {criteria.map((c, i) => (
          <motion.div
            key={c.rule}
            initial={{ opacity: 0, x: -8 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.2 + 0.1, duration: 0.5, ease: customEase }}
            className="space-y-2"
          >
            <div className="flex items-center justify-between font-mono text-[11px]">
              <span className="text-white/35">{c.rule}</span>
              <span className="text-emerald-400">
                {c.match ? "MET" : "UNMET"}
              </span>
            </div>
            <div className="h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: "100%" }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2 + 0.3, duration: 0.8, ease: customEase }}
                className="h-full rounded-full bg-emerald-500/40"
              />
            </div>
          </motion.div>
        ))}
        <div className="border-t border-white/[0.06]" />
        <Line delay={0.9} label="score" value="3/3 criteria met" accent />
      </div>
    </TerminalChrome>
  );
}

/* ── Step 4: Agent Negotiation ── */
export function StepNegotiation() {
  const messages = [
    { from: "provider", text: "Submitting PA for MRI 73221", delay: 0.1 },
    { from: "provider", text: "Evidence bundle: 4 FHIR resources attached", delay: 0.3 },
    { from: "payer", text: "Reviewing against policy ANC-2024-MRI", delay: 0.6 },
    { from: "payer", text: "Additional doc needed: PT discharge summary", delay: 0.9 },
    { from: "provider", text: "Retrieved. Attaching DocumentReference/pt-dc", delay: 1.2 },
    { from: "payer", text: "All criteria satisfied.", delay: 1.5 },
  ];

  return (
    <TerminalChrome title="a2a / coin-negotiation">
      <div className="space-y-4">
        {messages.map((m, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: m.delay, duration: 0.5, ease: customEase }}
            className={`flex gap-2 font-mono text-[11px] ${
              m.from === "provider" ? "" : "justify-end"
            }`}
          >
            <span className={`px-2 py-1 rounded text-[9px] uppercase tracking-wider ${
              m.from === "provider"
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-white/[0.06] text-white/30"
            }`}>
              {m.from}
            </span>
            <span className="text-white/50">{m.text}</span>
          </motion.div>
        ))}
      </div>
    </TerminalChrome>
  );
}

/* ── Step 5: Determination Returned ── */
export function StepApproved() {
  return (
    <TerminalChrome title="overture / determination">
      <div className="space-y-4">
        <Line delay={0.1} label="status" value="" />
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3, duration: 0.6, ease: customEase }}
          className="flex items-center justify-center py-8"
        >
          <div className="flex flex-col items-center gap-4">
            <div className="w-14 h-14 rounded-full bg-emerald-500/15 flex items-center justify-center">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1.5" strokeLinecap="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <span className="font-mono text-emerald-400 text-sm uppercase tracking-widest">PA Approved</span>
          </div>
        </motion.div>
        <div className="border-t border-white/[0.06] pt-4 space-y-4">
          <Line delay={0.5} label="auth_number" value="ATH-2026-0847291" />
          <Line delay={0.6} label="latency" value="47.2 seconds" accent />
          <Line delay={0.7} label="written_to" value="EHR/ClaimResponse" />
        </div>
      </div>
    </TerminalChrome>
  );
}
