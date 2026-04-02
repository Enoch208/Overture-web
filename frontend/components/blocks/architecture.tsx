"use client";

import dynamic from "next/dynamic";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { Badge } from "@/components/ui/badge";

const ArchitectureDiagram = dynamic(
  () => import("@/components/blocks/architecture-diagram").then((m) => ({ default: m.ArchitectureDiagram })),
  { ssr: false }
);

const layers = [
  {
    badge: "MCP Server",
    title: "Clinical Evidence Bundler",
    description:
      "Connects via SMART on FHIR to pull patient summaries, supporting evidence, and compile structured PA submission bundles.",
    tools: ["get_patient_summary", "find_supporting_evidence", "compile_pa_packet"],
  },
  {
    badge: "MCP Server",
    title: "Payer Rules Engine",
    description:
      "Indexes medical policies, coverage rules, and formularies. Evaluates clinical evidence against payer-specific criteria.",
    tools: ["check_pa_required", "get_criteria", "evaluate_evidence"],
  },
  {
    badge: "A2A Agent",
    title: "Provider PA Coordinator",
    description:
      "Detects PA triggers, orchestrates the MCP workflow, compiles submissions, and initiates real-time negotiation with the payer agent.",
    tools: [],
  },
  {
    badge: "A2A Agent",
    title: "Payer Review Agent",
    description:
      "Receives PA requests, applies rules, requests additional documentation through multi-turn conversation, and returns determinations.",
    tools: [],
  },
];

export function Architecture() {
  return (
    <section id="architecture" className="py-32 px-8">
      <div className="max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="text-center max-w-3xl mx-auto">
            <p className="font-mono text-xs uppercase tracking-widest text-secondary">
              Architecture
            </p>
            <h2 className="mt-4 font-display text-5xl md:text-6xl leading-[1.1] tracking-tight text-primary">
              Agents that speak<br />
              <em>each other&apos;s language</em>
            </h2>
            <p className="mt-6 font-body text-lg leading-relaxed text-secondary max-w-2xl mx-auto">
              Built on the A2A protocol and FHIR standard. Provider and payer agents
              communicate via Conversational Interoperability (COIN), exchanging
              structured clinical arguments — not PDFs.
            </p>
          </div>
        </ScrollReveal>

        {/* Animated Architecture Diagram */}
        <ScrollReveal delay={0.1}>
          <div className="mt-16">
            <ArchitectureDiagram />
          </div>
        </ScrollReveal>

        {/* Layer Cards */}
        <div className="mt-24 grid grid-cols-1 md:grid-cols-2 gap-8">
          {layers.map((layer, i) => (
            <ScrollReveal key={layer.title} delay={i * 0.1}>
              <div className="bg-canvas-elevated rounded-3xl p-10 border border-black/5 shadow-soft h-full">
                <Badge
                  label={layer.badge}
                  variant={layer.badge === "A2A Agent" ? "success" : "processing"}
                />
                <h3 className="mt-6 font-display text-2xl tracking-tight text-primary">
                  {layer.title}
                </h3>
                <p className="mt-3 font-body text-sm leading-relaxed text-secondary">
                  {layer.description}
                </p>
                {layer.tools.length > 0 && (
                  <div className="mt-6 flex flex-wrap gap-2">
                    {layer.tools.map((tool) => (
                      <span
                        key={tool}
                        className="inline-block px-3 py-1.5 rounded-full bg-slate-50 font-mono text-xs text-secondary"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
