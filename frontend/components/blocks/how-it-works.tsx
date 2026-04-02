"use client";

import { ScrollReveal } from "@/components/ui/scroll-reveal";
import {
  AiScanIcon,
  FileSearchIcon,
  DocumentValidationIcon,
  ChatBotIcon,
  SecurityCheckIcon,
} from "hugeicons-react";
import { ElementType, ReactNode } from "react";
import {
  StepTrigger,
  StepEvidence,
  StepCriteria,
  StepNegotiation,
  StepApproved,
} from "@/components/blocks/step-illustrations";

const steps: {
  number: string;
  icon: ElementType;
  title: string;
  description: string;
  illustration: ReactNode;
}[] = [
  {
    number: "01",
    icon: AiScanIcon,
    title: "Order Triggers PA",
    description:
      "A physician places a clinical order. Our agent detects the PA requirement instantly from the CPT code and payer rules.",
    illustration: <StepTrigger />,
  },
  {
    number: "02",
    icon: FileSearchIcon,
    title: "Evidence Assembly",
    description:
      "The Clinical Evidence Bundler connects to the patient's FHIR record via SMART on FHIR, pulling diagnoses, labs, imaging, and treatment history.",
    illustration: <StepEvidence />,
  },
  {
    number: "03",
    icon: DocumentValidationIcon,
    title: "Criteria Matching",
    description:
      "The Payer Rules Engine evaluates gathered evidence against medical necessity criteria specific to the procedure and payer.",
    illustration: <StepCriteria />,
  },
  {
    number: "04",
    icon: ChatBotIcon,
    title: "Agent Negotiation",
    description:
      "Provider and Payer agents begin an A2A conversation — exchanging structured clinical arguments via the COIN protocol in real time.",
    illustration: <StepNegotiation />,
  },
  {
    number: "05",
    icon: SecurityCheckIcon,
    title: "Determination Returned",
    description:
      "The PA determination is written back to the EHR. What took 3 days of phone and fax now takes 47 seconds.",
    illustration: <StepApproved />,
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-32 px-8 bg-canvas-elevated">
      <div className="max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="text-center max-w-3xl mx-auto">
            <p className="font-mono text-xs uppercase tracking-widest text-secondary">
              How It Works
            </p>
            <h2 className="mt-4 font-display text-5xl md:text-6xl leading-[1.1] tracking-tight text-primary">
              Five steps.<br />
              <em>Forty-seven seconds.</em>
            </h2>
          </div>
        </ScrollReveal>

        <div className="mt-24 space-y-32">
          {steps.map((step, i) => {
            const isReversed = i % 2 !== 0;
            return (
              <ScrollReveal key={step.number} delay={0.05}>
                <div
                  className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center"
                  style={isReversed ? { direction: "rtl" } : undefined}
                >
                  <div style={isReversed ? { direction: "ltr" } : undefined}>
                    <div className="flex items-center gap-4 mb-6">
                      <div className="w-12 h-12 rounded-full bg-slate-50 flex items-center justify-center">
                        <step.icon size={22} strokeWidth={1.5} className="text-dark-contrast" />
                      </div>
                      <span className="font-mono text-xs uppercase tracking-widest text-secondary">
                        Step {step.number}
                      </span>
                    </div>
                    <h3 className="font-display text-4xl leading-[1.1] tracking-tight text-primary">
                      {step.title}
                    </h3>
                    <p className="mt-4 font-body text-lg leading-relaxed text-secondary max-w-md">
                      {step.description}
                    </p>
                  </div>

                  <div style={isReversed ? { direction: "ltr" } : undefined}>
                    {step.illustration}
                  </div>
                </div>
              </ScrollReveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
