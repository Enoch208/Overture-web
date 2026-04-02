export function Footer() {
  return (
    <footer className="bg-dark-contrast text-white">
      <div className="max-w-7xl mx-auto px-8 py-24">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-16">
          <div className="md:col-span-1">
            <span className="font-display text-3xl tracking-tight">Overture</span>
            <p className="mt-4 text-white/60 font-body text-sm leading-relaxed">
              Automating prior authorization through agent-to-agent orchestration.
            </p>
          </div>

          <div>
            <h4 className="font-body font-medium text-sm uppercase tracking-widest text-white/40 mb-6">
              Product
            </h4>
            <ul className="space-y-4">
              {["How It Works", "Architecture", "Security", "Pricing"].map((item) => (
                <li key={item}>
                  <a href="#" className="font-body text-sm text-white/70 hover:text-white transition-colors duration-500">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-body font-medium text-sm uppercase tracking-widest text-white/40 mb-6">
              Resources
            </h4>
            <ul className="space-y-4">
              {["Documentation", "API Reference", "FHIR Guide", "Changelog"].map((item) => (
                <li key={item}>
                  <a href="#" className="font-body text-sm text-white/70 hover:text-white transition-colors duration-500">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-body font-medium text-sm uppercase tracking-widest text-white/40 mb-6">
              Company
            </h4>
            <ul className="space-y-4">
              {["About", "Blog", "Careers", "Contact"].map((item) => (
                <li key={item}>
                  <a href="#" className="font-body text-sm text-white/70 hover:text-white transition-colors duration-500">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-24 pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="font-body text-xs text-white/40">
            &copy; 2026 Overture Health, Inc. All rights reserved.
          </p>
          <div className="flex gap-8">
            {["Privacy", "Terms", "HIPAA"].map((item) => (
              <a key={item} href="#" className="font-body text-xs text-white/40 hover:text-white/70 transition-colors duration-500">
                {item}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
