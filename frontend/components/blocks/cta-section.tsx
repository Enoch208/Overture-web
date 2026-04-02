"use client";

import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { OvertureButton } from "@/components/ui/overture-button";

export function CTASection() {
  return (
    <section className="py-32 px-8">
      <div className="max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="bg-dark-contrast rounded-3xl p-16 md:p-24 text-center">
            <p className="font-mono text-xs uppercase tracking-widest text-white/40">
              Early Access
            </p>
            <h2 className="mt-6 font-display text-5xl md:text-6xl leading-[1.1] tracking-tight text-white">
              3 days → 47 seconds.
              <br />
              <em className="text-white/70">See it live.</em>
            </h2>
            <p className="mt-8 font-body text-lg leading-relaxed text-white/60 max-w-xl mx-auto">
              Join the providers and payers already transforming prior authorization.
              CMS compliance deadline is here — Overture gets you there.
            </p>
            <div className="mt-10 flex flex-wrap justify-center gap-4">
              <OvertureButton
                variant="primary"
                className="!bg-white !text-dark-contrast hover:!bg-white/90"
              >
                Request Early Access
              </OvertureButton>
              <OvertureButton
                variant="secondary"
                className="!border-white/20 !text-white hover:!bg-white/10"
              >
                Schedule a Demo
              </OvertureButton>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
