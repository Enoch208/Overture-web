import { Navbar } from "@/components/layout/navbar";
import { Hero } from "@/components/blocks/hero";
import { ProblemStats } from "@/components/blocks/problem-stats";
import { HowItWorks } from "@/components/blocks/how-it-works";
import { Architecture } from "@/components/blocks/architecture";
import { CTASection } from "@/components/blocks/cta-section";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <ProblemStats />
      <HowItWorks />
      <Architecture />
      <CTASection />
      <Footer />
    </>
  );
}
