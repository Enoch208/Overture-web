# OVERTURE: Frontend Architecture & UI/UX Standard
**Document Version:** 1.0 (Strict Enforcement)
**Project Context:** Overture is a VC-backed, high-end healthcare infrastructure product. It automates prior authorization using a multi-agent system (Conversational Interoperability / COIN). 
**Design Philosophy:** "Modern Editorial meets Hardworking Tech." It must look like a trusted, century-old institution, powered by cutting-edge AI. **DO NOT design a generic, colorful B2B SaaS dashboard.**

---

## 1. ENGINEERING DIRECTIVES (STRICT)
You are the Lead Frontend Engineer. You will not write monolithic code. 
* **Zero Monoliths:** A page file (e.g., `page.tsx`) must contain NO hardcoded layout HTML. It must only render a stack of semantic sections (e.g., `<Hero />`, `<WorkflowCards />`).
* **Component Modularity:** Every visual element must be broken down into Atoms (`/ui`), Molecules (`/blocks`), and Organisms (`/layout`).
* **Prop-Driven:** Never hardcode text inside a reusable component. Use props (`title`, `description`, `icon`, `children`).
* **No Default Tailwind Colors:** You are forbidden from using default tailwind colors (e.g., `blue-500`, `purple-600`) unless explicitly instructed. Use the Semantic Color Tokens below.

---

## 2. DESIGN TOKENS

### A. Typography (The 3-Tier System)
You must import and apply these three distinct fonts. Do not mix their purposes.
1. **Display / Editorial (Trust):** `Instrument Serif` (or `Playfair Display`)
   * *Usage:* Exclusively for `<h1>`, `<h2>`, and massive statistics.
   * *Styling:* Always `leading-[1.1]` or `leading-none`, `tracking-tight`. Use italics selectively for emphasis.
2. **Interface / Body (Clarity):** `Satoshi` (or `Plus Jakarta Sans`, `Inter`)
   * *Usage:* Paragraphs, button text, navbar links, UI labels.
   * *Styling:* `leading-relaxed` for paragraphs, `font-medium` for buttons/labels.
3. **Agent / Utility (The Machine):** `Geist Mono` (or `JetBrains Mono`)
   * *Usage:* Only for FHIR codes, timestamps, agent status indicators, and JSON snippets.
   * *Styling:* Always `text-xs` or `text-sm`, `uppercase tracking-widest` when used in badges.

### B. Color Palette
Define these in `tailwind.config.js` or as CSS variables.
* **Canvas Primary:** `#F9F9F6` (Warm, premium off-white. Used for main page backgrounds).
* **Canvas Elevated:** `#FFFFFF` (Pure white. Used for cards and modals).
* **Dark Contrast:** `#1A2F24` (Deep forest slate. Used for primary buttons and dark CTA sections).
* **Text Primary:** `#2D2D2D` (Dark charcoal. Never use `#000000`).
* **Text Secondary:** `#6B7280` (Muted gray for subtext).
* **Agent Status (Muted):**
  * Success: `bg-emerald-50 text-emerald-800`
  * Processing: `bg-slate-100 text-slate-800`

### C. Geometry & Shadows
* **Interactive Elements:** Fully rounded (`rounded-full`).
* **Structural Containers:** Soft, uniform curves (`rounded-2xl` or `rounded-3xl`).
* **Borders:** No harsh solid borders. Use `border border-black/5` or `border-white/20`.
* **The "Soft Glow" Shadow:** Do not use default `shadow-md`. Use:
  * `box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.04)`

---

## 3. ICONOGRAPHY ARCHITECTURE
* **Library:** `Hugeicons`. 
* **Rule 1: Stroke Width:** All icons MUST have a `stroke-width` of exactly `1.5px`. 
* **Rule 2: Fill:** Outline only. `fill-none`.
* **Rule 3: Containers:** Icons should rarely float on their own. Wrap them in a soft circular container (e.g., `w-12 h-12 rounded-full bg-slate-50 flex items-center justify-center`).

---

## 4. MOTION & PHYSICS
Animations must feel heavy, deliberate, and expensive. No bouncy, fast defaults.
* **Global Easing:** Use custom cubic-bezier: `transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]`.
* **Hover States:** Scale interactives infinitesimally (`scale-105` or `-translate-y-1`) and increase shadow opacity slightly. Do not dramatically change background colors.
* **Scroll Entrances:** Elements entering the viewport must fade in and slide up:
  * *From:* `opacity-0 translate-y-8`
  * *To:* `opacity-100 translate-y-0`
  * *Duration:* `700ms`
  * *Stagger:* If rendering a list or grid of cards, stagger the children by `100ms` or `150ms`.

---

## 5. SPATIAL RHYTHM (8pt Grid)
Every margin, padding, and gap must be a multiple of 8px. 
* **Macro (Sections):** `py-24` or `py-32`. Let the layout breathe.
* **Micro (Cards):** `p-8` or `p-10`.
* **Gaps:** `gap-4` or `gap-8` for flex/grid containers.
* **Strict Ban:** Do not use arbitrary Tailwind values (e.g., `mt-[17px]`).

---

## 6. COMPONENT LIBRARY & TECH STACK DIRECTIVE
You are forbidden from using default Shadcn/UI styling. It is too generic. To achieve the bespoke Overture aesthetic, you must use the following stack:

* **Base UI Logic:** Use **Radix UI Primitives**. You must style them strictly using the Overture Tailwind tokens (no default Radix styles). 
* **Animations:** Use **Framer Motion**. All complex entrances, stagger effects, and layout changes must use Framer Motion with the global custom easing: `ease: [0.22, 1, 0.36, 1]`.
* **Complex Visuals:** For diagrams, connecting lines, or bento grids, you may pull from **Magic UI**, but you MUST override their default styles to match the Overture Light/Cream palette. No neon glowing effects.
* **Forms & Inputs:** If a pre-built library is absolutely necessary for speed, use **NextUI v2**, but strip all default borders and apply the Overture soft-shadow system.
