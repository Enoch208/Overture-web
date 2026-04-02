"use client";

import { ScrollReveal } from "@/components/ui/scroll-reveal";
import {
  MoneyReceiveCircleIcon,
  TimeManagementIcon,
  CancelCircleIcon,
  PolicyIcon,
} from "hugeicons-react";
import { ElementType } from "react";

const stats: { icon: ElementType; value: string; label: string; description: string }[] = [
  {
    icon: MoneyReceiveCircleIcon,
    value: "$35B",
    label: "Annual PA cost to US healthcare",
    description: "Administrative burden that could be redirected to patient care.",
  },
  {
    icon: TimeManagementIcon,
    value: "3 days",
    label: "Average PA turnaround",
    description: "Phone trees, fax machines, and manual review queues.",
  },
  {
    icon: CancelCircleIcon,
    value: "34%",
    label: "Of PAs initially denied",
    description: "Most overturned on appeal — wasted effort on both sides.",
  },
  {
    icon: PolicyIcon,
    value: "Jan 2026",
    label: "CMS mandate deadline",
    description: "7-day electronic PA turnaround now required by federal rule.",
  },
];

export function ProblemStats() {
  return (
    <section className="py-32 px-8">
      <div className="max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="text-center max-w-3xl mx-auto">
            <p className="font-mono text-xs uppercase tracking-widest text-secondary">
              The Problem
            </p>
            <h2 className="mt-4 font-display text-5xl md:text-6xl leading-[1.1] tracking-tight text-primary">
              A $35 billion<br />
              <em>administrative tax</em>
            </h2>
            <p className="mt-6 font-body text-lg leading-relaxed text-secondary max-w-2xl mx-auto">
              Prior authorization was designed to control costs. Instead, it became
              the most expensive, time-consuming process in healthcare administration.
            </p>
          </div>
        </ScrollReveal>

        <div className="mt-24 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, i) => (
            <ScrollReveal key={stat.label} delay={i * 0.1}>
              <div className="bg-canvas-elevated rounded-3xl p-8 border border-black/5 shadow-soft h-full">
                <div className="w-12 h-12 rounded-full bg-slate-50 flex items-center justify-center mb-6">
                  <stat.icon size={22} strokeWidth={1.5} className="text-secondary" />
                </div>
                <span className="font-display text-4xl tracking-tight text-primary">
                  {stat.value}
                </span>
                <p className="mt-4 font-body font-medium text-sm text-primary">
                  {stat.label}
                </p>
                <p className="mt-2 font-body text-sm leading-relaxed text-secondary">
                  {stat.description}
                </p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
