interface BadgeProps {
  label: string;
  variant?: "default" | "success" | "processing";
}

const variants = {
  default: "bg-slate-100 text-slate-800",
  success: "bg-emerald-50 text-emerald-800",
  processing: "bg-slate-100 text-slate-800",
};

export function Badge({ label, variant = "default" }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full font-mono text-xs uppercase tracking-widest ${variants[variant]}`}
    >
      {label}
    </span>
  );
}
