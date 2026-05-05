# Care Transition Orchestrator

**Hackathon:** *Agents Assemble — The Healthcare AI Endgame* (Prompt Opinion / Darena Health, on Devpost).
**Submission deadline:** **2026-05-11, 11:00 PM ET.**
**Build window from today (2026-05-04):** 7 days. *(Earlier draft assumed 15 — wrong. We have one week.)*
**Status:** Committed. One idea, not a menu.
**Target:** Under strong execution, top 3 is plausible. Grand prize: 15–25% (revised down because of the compressed window).
**Last updated:** 2026-05-04 — platform research complete; §6 rewritten for PO Launchpad reality; deadline corrected.

---

## 1. The Concept

A patient is being discharged from the hospital with a complex care plan. A **Discharge Orchestrator** agent — owned by the hospital — reaches out in real time to a constellation of agents owned by *different organizations* (specialty pharmacy, home health agency, OB/PCP practice, DME supplier) to negotiate a complete 30-day post-discharge plan **before the patient leaves the building**.

Each external agent owns its own data, its own constraints (inventory, schedule, insurance acceptance, capacity), and its own decisions. The hospital agent does **not** make point-to-point API calls into other orgs' systems — it has a parallel A2A conversation with each of them. They negotiate, raise blockers, request missing info, and converge on a single coherent CarePlan.

---

## 2. Why This Wins

### A2A is structurally required, not decorative
Prior authorization can honestly be done with one big agent calling MCP tools — payer logic is rules-based, the "negotiation" is performative. Care transitions are different: each receiving organization genuinely owns data and decisions the orchestrator **cannot see** (SNF bed availability, pharmacy stock, home health caseload). A2A is the only way it works. PA fails the multi-agent litmus test. Care transitions pass it.

### It maps cleanly to the three judging criteria
The official Devpost rules name **three equally-weighted criteria**:
1. **AI Factor** — does it leverage generative AI for things rule-based software cannot? *Yes — emergent cross-org negotiation under uncertainty.*
2. **Potential Impact** — pain point + outcome hypothesis. *HRRP penalties, 30-day readmissions, postpartum mortality. Quantified in §11.*
3. **Feasibility** — could this exist in a real healthcare system? *Yes — Da Vinci IGs already define the data flows. Each agent's behavior maps to a real org function.*

Care transitions hit all three. PA hits Impact and Feasibility but is weak on AI Factor (rule-based engines already do it).

### It's not crowded
Marketplace search did not surface a published care-transition or discharge-coordination submission as of 2026-05-04. **Differentiation alone moves a competent submission up before any judge interacts with it.** Re-verify in Marketplace once or twice during build.

### It demos in three minutes
Multiple agents converging on a CarePlan is dense — a 3-minute video can show: chat input → parallel A2A negotiation → validated US Core CarePlan written. PA demos look like form-filling. This looks like an orchestra. See §6 for how to render this *inside PO Launchpad chat*, since that is the demo surface.

### It hits 4 of Prompt Opinion's 5Ts in one workflow
The PO homepage names five deliverable types — Talk, Template, Table, Transaction, Task. Our project hits four:
- **Talk** — the chat consultation with the Orchestrator, grounded in the patient's chart.
- **Template** — the CarePlan IS a document pre-filled with the right data and context.
- **Transaction** — the validated CarePlan is written back to FHIR.
- **Task** — follow-up activities are assigned to Pharmacy and Home Health.

Only Table doesn't apply. Naming this mapping in the Devpost copy and on the agent card signals "we built to your model" — free credibility for Feasibility scoring.

---

## 3. Judging Targets

### Official rubric (Devpost)
| Criterion | Weight | Our move |
|-----------|--------|----------|
| **AI Factor** | 1/3 | Live randomization (§7) proves agents reason over state, not memorize a script. |
| **Potential Impact** | 1/3 | Postpartum-preeclampsia persona + HRRP economics + maternal mortality framing. ICU step-down line as the generality nod. |
| **Feasibility** | 1/3 | Validated US Core CarePlan write-back; Da Vinci IG references; OAuth2 inter-agent auth; SHARP-conformant FHIR token handling. |

The three criteria are equally weighted per Devpost rules. Nothing in the published rules privileges multi-agent over single-agent — but **Feasibility** rewards realistic cross-org architecture, and that's where A2A wins.

### Strategic judge targeting *(unverified panel; treat as targeting overlay, not published assignment)*
Earlier drafts referenced a panel of Mandel, Tripathi, Mathur, Hickey, Zheng, Proctor. **Do not assume these are the assigned judges.** Devpost does not publish per-judge assignments. If we get insider confirmation of the panel via Discord/organizers, the framing below holds; otherwise treat as profile-of-likely-evaluators:

- **FHIR architects** → US Core CarePlan validation visible in chat output. Real SNOMED/RxNorm/LOINC codes. Da Vinci IG citations.
- **Multi-agent / protocol reviewers** → Linux Foundation A2A spec via official `a2a-sdk`. Show one agent card endpoint as JSON during the video.
- **Practicing clinicians** → Scenario reviewed by an OB or hospitalist before lock. Document the reviewer.
- **Operational / EHR reviewers** → Frame as augmenting (not replacing) the care-coordination team. HRRP economics ready.
- **Healthcare investors** → Postpartum-preeclampsia persona. Payer model rehearsed.
- **Platform/innovation reviewers** → One-line generality answer: same pattern handles pediatric discharge, post-ICU, oncology infusion, behavioral health.

---

## 4. Platform Stack & Technical Alignment

### What Prompt Opinion actually is
A healthcare-agent assembly platform built on three open standards (MCP, A2A, FHIR) with two healthcare-specific layers riding on top (SHARP, COIN). The platform IS a FHIR server; agents and MCP servers receive scoped FHIR tokens via SHARP context propagation. The runtime surface is the **Launchpad chat**: User → User Agent → Your Agent. Submissions are published to **Marketplace Studio**.

| Layer | Spec | Owner | Our job |
|-------|------|-------|---------|
| **MCP** | Model Context Protocol | Anthropic | Build a SHARP-conformant MCP server for the CarePlan write-back |
| **A2A** | Agent2Agent Protocol — `a2a-protocol.org` | **Linux Foundation** (since 2025-06-23; co-founders include AWS, Cisco, Google, Microsoft, Salesforce, SAP, ServiceNow) | Use the official `a2a-sdk` (Python). Agent cards at well-known URLs |
| **FHIR** | R4 + US Core | HL7 | US Core CarePlan profile, validated against the HL7 FHIR Validator before write |
| **SHARP** | Standardized Healthcare Agent Remote Protocol — `sharponmcp.com` | Prompt Opinion (open spec) | Receive FHIR tokens via headers (`X-FHIR-Server-URL`, `X-FHIR-Access-Token`) — don't reinvent the auth dance |
| **COIN** | Conversational Interoperability — *industry-emerging concept, not a spec we import* | Industry / HL7 Connectathon work | Reference as architectural framing in the pitch; don't claim it's a library |

**Build to the open standards. Let SHARP do the FHIR-token plumbing. Don't claim COIN as a Prompt Opinion library — it's a conceptual frame.**

### Reference repositories (use as starting point)
- **`github.com/prompt-opinion/po-adk-python`** — Google ADK A2A agent template (Python). Ships three sample agents (`healthcare_agent`, `general_agent`, `orchestrator`). **Note:** uses `a2a-sdk` 0.3.x with `AgentCardV1` shims for spec v1 compatibility.
- **`github.com/prompt-opinion/po-adk-typescript`** — TypeScript ADK variant.
- **`github.com/prompt-opinion/po-community-mcp`** — MCP server reference (C#, TypeScript, Python). Conforms to SHARP-on-MCP.
- **`github.com/prompt-opinion/po-community-a2a`** — additional Python A2A samples.

### Non-negotiable technical alignments
1. **Linux Foundation A2A via `a2a-sdk`.** No custom protocols. Standard `Message` / `Task` / `Artifact` / `Part` (TextPart, FilePart, DataPart) lifecycle. **Verify exact agent-card filename on day 1** — A2A spec uses `/.well-known/agent.json`; PO templates may use `agent-card.json`. Lock the working filename, don't argue both.
2. **US Core CarePlan profile, validated** — run the HL7 FHIR Validator (java jar) with `-ig hl7.fhir.us.core` in CI. Each agent's contribution attaches as a `CarePlan.activity` with `author` referencing its own `Organization` resource.
3. **Real terminology codes** — SNOMED CT for conditions, RxNorm for medications, LOINC for observations/labs. No made-up strings.
4. **Da Vinci IG citations in the video and description.** Specifically:
   - **Da Vinci PCDE** (`hl7.org/fhir/us/davinci-pcde`) — Payer Coverage Decision Exchange covers continuity-of-treatment **CarePlan** transfer at coverage transitions. **The headline citation.**
   - **Da Vinci Unsolicited Notifications IG** (`hl7.org/fhir/us/davinci-alerts`) — covers ADT discharge notifications.
   - **Da Vinci CDex** (`hl7.org/fhir/us/davinci-ecdx`) — task-based clinical data request between orgs.
5. **Clinically vetted scenario** — every clinical detail (BP thresholds, medication substitutions, follow-up timing, lactation considerations) reviewed by a practicing OB or hospitalist before lock. Document the reviewer in the submission text.
6. **OAuth2 client-credentials between agents** — service-to-service, audience-scoped tokens. Each org's agent has its own credentials.
7. **Synthetic / de-identified data only.** Devpost rules forbid real PHI.

---

## 5. Architecture

### MCP Server — Patient Care Plan Composer
SHARP-conformant. Receives FHIR token via headers; writes back to PO's FHIR server.

| Tool | Description |
|------|-------------|
| `get_discharge_summary(patient_id)` | Pulls FHIR Encounter, Conditions, MedicationRequests, ServiceRequests |
| `identify_transition_needs(plan)` | Returns structured list (home health, pharmacy, DME, follow-ups) |
| `get_patient_constraints(patient_id)` | Insurance, geography, language, SDoH from FHIR |
| `validate_care_plan(plan)` | Runs HL7 FHIR Validator against US Core CarePlan profile in-process |
| `write_care_plan(plan)` | Writes the validated CarePlan resource back to FHIR |

### A2A Agents — three, separately deployed
Three is the number. Most submissions will be one agent + tools.

1. **Discharge Orchestrator** *(hospital-side, the published headline submission)* — Owns the plan. Drives the negotiation. Parses the discharge summary into discrete needs and opens parallel A2A conversations.
2. **Specialty Pharmacy Agent** — Own state: a JSON inventory store with backorder flags. Own MCP tools for inventory + benefits investigation.
3. **Home Health Coordinator Agent** — Own state: an actual scheduling grid with capacity windows. Own MCP tools for caseload + service area + scheduling.

**The Patient is the User Agent in PO Launchpad.** Don't deploy a fourth external "patient agent" — the platform's User Agent fills that role naturally and the BP-cuff timing scene still works (Orchestrator queries the User Agent for availability).

Each external agent is **separately deployed (own ngrok/host), separately authenticated (own OAuth2 client-credentials), with its own A2A-spec-compliant agent card**. All three should be **published to Marketplace** so judges can probe each independently — single submission rules permitting; otherwise the Orchestrator is the published submission and pharmacy/home-health run privately, called by the Orchestrator.

### FHIR Resources
`Encounter`, `Condition`, `MedicationRequest`, `ServiceRequest`, **`CarePlan`**, `CareTeam`, `Patient`, `Coverage`, `Communication`, `Task`.

`CarePlan` is the central artifact. Each contributing agent appends a `CarePlan.activity` with `author` referencing its own `Organization` resource. The Orchestrator owns the parent CarePlan. Conforms to **US Core CarePlan profile**.

---

## 6. Demo Surface — PO Launchpad Chat + 3-Minute Video

**The judging surface is PO Launchpad chat.** A custom web UI is not a submission. The < 3-minute video must show the project "functioning within the Prompt Opinion platform" (Devpost rules). This forces the storytelling into chat output — and that is fine; do it well.

### What the chat output must do
- **Attribute every message clearly.** Each agent's response renders with its `Organization` name, an `Organization.npi`-style identifier in Geist Mono, and a timestamp. Visually distinct prefixes per org. The chat transcript itself is the orchestra.
- **Show parallel A2A calls in the transcript.** The Orchestrator's response includes a structured "calling: pharmacy_agent, home_health_agent in parallel" preamble (Markdown / fenced code block). Each org's reply lands as its own message with attribution.
- **Render the inter-agent A2A trace inline.** Print a compact, redacted summary of the actual A2A JSON-RPC envelopes between agents — `message/send` request → `task/result` artifact — so the reader can see the protocol working, not just the rendered prose. Fenced JSON in chat output. SyncShift (see §13) does not have anything comparable; this is a free differentiator.
- **Render the CarePlan as a structured artifact.** Final Orchestrator reply includes the validated `CarePlan` JSON in a fenced block. Use A2A `DataPart` / `FilePart` if PO Launchpad renders them inline; fall back to fenced JSON in `TextPart` if not.
- **Show validation passing.** "✓ US Core CarePlan validated against `hl7.fhir.us.core#9.0.0`" — explicit line in the final message. Validator output (or a one-line summary of it) is visible.
- **Surface the agent card.** During the video, flip to a browser tab showing one agent's `/.well-known/agent.json` (or `agent-card.json` — verify and lock). Five seconds; high credibility.

### What the video must do (3 minutes)

| Time | Beat | Surface |
|------|------|---------|
| **0:00–0:20** | Establish patient and stakes (postpartum preeclampsia, day 3, being discharged). | Voiceover + PO Launchpad with patient context loaded |
| **0:20–0:40** | Type one prompt to the Discharge Orchestrator: *"Compose the 30-day post-discharge plan for this patient."* | PO Launchpad chat |
| **0:40–1:30** | **The negotiation.** Orchestrator's response shows parallel A2A calls. Pharmacy reports labetalol on backorder, proposes nifedipine, requests OB confirmation. Home Health reports BP cuff delivery slot after 4pm. Each message attributed, timestamped. | PO Launchpad chat — scrolling transcript |
| **1:30–2:00** | Orchestrator reconciles, asks User Agent (patient) for delivery-window confirmation. User confirms. | PO Launchpad chat |
| **2:00–2:30** | Final Orchestrator message: validated US Core `CarePlan` JSON in a fenced block, "✓ validated" line, `CarePlan` resource ID written to FHIR. | PO Launchpad chat |
| **2:30–2:50** | **Quick browser flip:** show one agent's well-known agent card endpoint. | Browser tab — 5 seconds |
| **2:50–3:00** | The kicker line: "4–6 hours of nurse work → 90 seconds. The same pattern handles post-ICU step-down — the highest-mortality handoff in medicine." | Voiceover over closing PO chat frame |

### Live randomization (the trust move)
Before recording the video, randomize one or two scenario variables in agent state — which medication is on backorder, when the BP cuff window opens, which day OB has availability. Then **record three takes back-to-back with different rolled state** and link all three from the Devpost description. Judges who probe the published Marketplace agent will hit a *different* rolled state again. This proves the negotiation is emergent, not scripted, and is the single highest-leverage move for AI-Factor scoring.

---

## 7. Hard Constraints (Discipline)

These are non-negotiable. Violating any tanks the submission.

- **Three agents. One clinical scenario. One FHIR write. Seven days.** No pediatric *and* adult. No multiple discharge types.
- **No fake multi-agent.** Each external agent is its own deployment, its own auth, its own agent card. A single LLM with three system prompts is disqualifying.
- **No custom A2A protocol.** Use `a2a-sdk` directly.
- **No reinventing SHARP.** Receive FHIR tokens via the standard SHARP headers.
- **Don't claim COIN as a library.** It's an architectural concept; reference it as such.
- **Do not skip the FHIR write-back.** Reading FHIR is table stakes. Writing a *validated* US-Core-conformant `CarePlan` is what makes this look real.
- **No hardcoded conversation.** The negotiation must emerge from real per-agent state. Live randomization (§6) is the proof.
- **No fabricated clinical details.** Every medication name, dose, threshold, and timing reviewed by a clinician.
- **Synthetic / de-identified data only.** No real PHI ever.

---

## 8. Risk & Mitigation

| Risk | Severity | Mitigation |
|------|----------|------------|
| 7-day window vs 3-agent + MCP + validation scope | **Highest** | Cut to 2 agents (Pharmacy + Home Health) if Day 4 is not on track. The orchestra metaphor still holds with 2; the FHIR write-back must not be cut. |
| Negotiation looks scripted in the video | High | Live randomization (§6). Three takes with different rolled state, all linked. |
| FHIR is sloppy → Feasibility score drops | High | Validate against US Core CarePlan profile with HL7 FHIR Validator. Real codes only. References resolve. Show validation passing in the final chat message. |
| Custom protocol or agent-card filename wrong → protocol-savvy reviewer flags it | High | Lock `a2a-sdk` and the working agent-card filename on Day 1. Show the live agent card endpoint in the video. |
| Clinical detail wrong → Feasibility drops | High | Clinician review gate before video record. Document the reviewer in submission text. |
| PO Marketplace publish gate adds latency | Medium | Publish 48+ hours before May 11 11pm ET. Marketplace review/approval flow not publicly documented; assume it exists. |
| The chat transcript looks dense and hard to follow | Medium | Visual attribution per org (§6). Strong typography in chat output. Consider a one-line "what just happened" summary message after each negotiation round. |
| A similar submission already in Marketplace | Low–Medium | Re-check Marketplace twice during build. Adjust framing to differentiate if a similar build appears. |
| Real PHI accidentally used | Catastrophic | Synthetic patients only — use the platform's built-in synthetic patient import. |

---

## 9. The Three Decisive Moves

If we get these right, top 10 (an Honorable Mention prize) is a strong floor. Top 3 is plausible. If we miss any, we drop into the field.

1. **Linux Foundation A2A via `a2a-sdk` on Day 1.** Lock the working agent-card filename. No custom protocols.
2. **Live randomization + real per-agent state.** Three video takes with different rolled state. The single thing most likely to convince a skeptical reviewer that this is genuine multi-agent reasoning.
3. **Clinician-vetted scenario + validated US Core CarePlan.** Validation visible in the final chat message. Reviewer named in the Devpost description.

**Cost note:** all three are cheap relative to the build. Clinician review ≈ 30-minute call. CarePlan validation ≈ one library + a CI step. Live randomization ≈ ~half a day of demo engineering. Together they are <10% of total build effort and represent the difference between honorable-mention floor and grand-prize ceiling.

---

## 10. Reviewer Q&A Prep (asynchronous — they'll read the description, not ask you live)

The submission text on Devpost is the only Q&A surface. Prepare answers as written FAQ-style entries.

**On how this maps to Prompt Opinion's 5Ts.**
Four of the five in one workflow. **Talk** = the chat consultation with the Discharge Orchestrator. **Template** = the CarePlan as a pre-filled, profile-validated document. **Transaction** = the FHIR write-back of the CarePlan to the workspace's FHIR server. **Task** = the follow-up activities assigned to Pharmacy and Home Health, attached as `CarePlan.activity` entries. Only Table does not apply — this workflow doesn't extract from unstructured documents (it composes them).

**On CarePlan authorship across organizations.**
Each contributing agent appends a `CarePlan.activity` with `author` referencing its own `Organization` resource. The Orchestrator owns the parent CarePlan. Conforms to US Core CarePlan profile. Aligns with **Da Vinci PCDE** patterns for continuity-of-treatment CarePlan transfer.

**On agent discovery and auth.**
Each agent publishes a Linux-Foundation-A2A-compliant agent card at its well-known endpoint. Built with the official `a2a-sdk` — standard `Message` / `Task` / `Artifact` / `Part` lifecycle. Inter-agent auth is OAuth2 client-credentials with audience-scoped tokens; FHIR auth uses SHARP-conformant header propagation.

**On patient adherence / non-cooperation.**
The Patient is the User Agent in PO Launchpad — a first-class participant in the negotiation. The BP-cuff timing scene shows this: the Orchestrator queries the User Agent for delivery-window confirmation rather than scheduling unilaterally.

**On EHR fit.**
Single notification at discharge initiation. Background orchestration. The care manager reviews the converged CarePlan in one Epic-embedded SMART app surface (out-of-scope for the hackathon build, in-scope for the production roadmap), then approves. Replaces 4–6 hours of phone/fax with one review.

**On commercial viability.**
Hospitals pay. HRRP readmission penalties total ~$500M+ annually across hospitals. Single readmission cost: $15–20K. Postpartum readmission is a maternal mortality vector under rising payer scrutiny. ROI is immediate and measurable.

**On generality beyond postpartum.**
The MCP server and A2A protocol layer are domain-general. We chose postpartum for the demo because of clinical stakes and specificity. The same pattern handles pediatric discharge, post-ICU step-down, oncology infusion coordination, behavioral health transitions.

---

## 11. Engineering Standard

The frontend in `/frontend` is **marketing only** — it is not the judging surface. Do not invest engineering against it during build week. The judging surface is PO Launchpad chat. All visual storytelling lives there per §6.

If we extend the project post-hackathon, the Overture frontend (per `CLAUDE.md`: Modern Editorial meets Hardworking Tech, Instrument Serif, Geist Mono, soft shadows) becomes the public marketing site and a screen-share demo asset for investor / customer conversations.

---

## 12. Open Verifications (do in Day 1)

Each of these costs <30 minutes and de-risks the build.

- **Marketplace browse.** Log into `app.promptopinion.ai`, search for care-transition / discharge / orchestration agents already published. If a similar build exists, adjust framing.
- **Hosted endpoints, not just ngrok.** Pick one platform (Cloud Run, Render, Railway, Fly) and deploy the three agents + MCP server with stable URLs by Day 2. Stable hosted endpoints are themselves a Feasibility differentiator vs the ngrok-only competition (see §13). ngrok is fine for local iteration; the published agent cards must point at hosted URLs.
- **Agent-card filename.** A2A spec uses `/.well-known/agent.json`; some PO templates use `agent-card.json`. Run the `po-adk-python` template, register it in PO Workspace Hub, and note the working URL. Lock and document.
- **Marketplace publish flow.** Push a hello-world agent through the publish pipeline once on Day 1. Time the latency from publish to discoverable. Plan the real publish accordingly.
- **a2a-sdk version decision.** PO templates ship `a2a-sdk` 0.3.x with `AgentCardV1` shims. Decide: stay on the shimmed template (lower risk) or upgrade to spec v1 (cleaner). Document the choice.
- **SHARP header verification.** Confirm by inspection that an MCP server registered in PO actually receives `X-FHIR-Server-URL` / `X-FHIR-Access-Token` (or whatever the current SHARP header names are at `sharponmcp.com`). One log statement, one test call.
- **Discord questions.** Join `discord.gg/cCBxKpdS7j` (canonical, linked from `promptopinion.ai`). Ask: (a) does Marketplace review/gate publishes, (b) any specific Launchpad chat rendering for `DataPart` / `FilePart`, (c) does PO Launchpad render A2A `skills.examples` as clickable suggestion chips, (d) is there a public list of judges. None of these answers should block the build.

---

## 13. Competitive Landscape (as of 2026-05-04)

Scouted three GitHub repos that public search surfaces as plausible Agents Assemble forks. Findings:

| Repo | Status | Threat |
|------|--------|--------|
| `evantofu/po-adk-python` | Template clone. Three commits by `evantofu`, all minor billing-eval JSON edits. **Not a submission.** | Ignore |
| `iamjai-3/adk-python-poc` | Generic Google ADK + SQLite POC. Not healthcare, not the PO template. **Not a submission.** | Ignore |
| `Roshan-B87/po-adk-python-syncshift` ("SyncShift AI") | "Zero-Click Clinical Handoff Copilot" — generates ICU shift-change SBAR summaries. **Real submission.** | Real but thin |

### SyncShift, honestly
- Single new agent (`handoff_agent/` on port 8004); no second agent, no MCP server, no multi-agent.
- **1 commit total** (Apr 29 2026). One-weekend dump.
- Read-only FHIR — one aggregator (`get_patient_handoff_data` in `shared/tools/fhir.py`) + a hand-rolled risk score. No `CarePlan` write. No US Core validation. No SHARP propagation work beyond template defaults.
- No demo video. No Devpost link. No hosted endpoint (local Uvicorn + ngrok). No screenshots. No Marketplace publish evidence.
- Addresses an *intra-shift* problem (one ICU team handing off to itself). We address a *cross-organization* problem (discharge across pharmacy + home health + OB). Different weight class.

### What this means for our positioning
The strategic case in §2 holds — multi-agent A2A negotiation across orgs, with a validated FHIR write, against a thin field. Concrete differentiators we can claim that SyncShift cannot:

1. **Multi-agent architecture** (3 separately-deployed A2A agents on independent endpoints with discoverable agent cards).
2. **FHIR write-back with US Core validation** (they read FHIR; we write a profiled `CarePlan` and validate it).
3. **Live randomization with three video takes** (their demo is static SBAR text; ours proves emergent reasoning).
4. **Hosted endpoints, stable URLs** (they're on local + ngrok).
5. **Visible inter-agent A2A trace in chat output** (they're a single agent — nothing to trace).

Re-scout once before submission lock.

---

## 14. Decision Log

- **2026-05-03:** Pivoted from Prior Authorization to Care Transition Orchestrator. Rationale: A2A is structurally required here; PA is a single-agent problem masquerading as multi-agent. Trades a crowded, performative space for an open, structurally-honest one.
- **2026-05-03:** Earlier draft attributed A2A to Google. **Corrected:** A2A was transferred to Linux Foundation governance on 2025-06-23. Canonical spec at `a2a-protocol.org`.
- **2026-05-04:** Platform research completed. Material corrections to earlier draft:
  - **Hackathon name** is "Agents Assemble — The Healthcare AI Endgame" (not "Agent Assemble Challenge").
  - **Deadline is 2026-05-11 11pm ET.** Build window is 7 days, not 15. Probability targets revised down accordingly.
  - **Judging is three equally-weighted criteria** (AI Factor / Impact / Feasibility) per Devpost rules — not the per-judge structural mapping the earlier draft assumed. The judge panel cited in earlier drafts is unverified.
  - **No live presentation round.** Judging surface is Marketplace + < 3min video. The earlier §6 "custom UI orchestra" framing is invalid; rewritten to render the orchestra inside PO Launchpad chat.
  - **SHARP** is "Standardized Healthcare Agent Remote Protocol" — open spec at `sharponmcp.com`, headers-based context propagation. Receive FHIR tokens; don't reinvent.
  - **COIN** is industry-emerging conceptual framing, not a Prompt Opinion library. Reference as concept, not as plumbing we import.
  - **Reference repos** are under `github.com/prompt-opinion/*` (not `spoke-community-mcp` — that was a mishearing of `po-community-mcp`).
  - **Da Vinci PCDE** elevated to headline IG citation — it's the IG that explicitly covers continuity-of-treatment CarePlan transfer at coverage transitions, which is exactly our scenario.
  - **No real PHI** — synthetic data only.
- **2026-05-04:** Frontend re-scoped as marketing-only for the hackathon period; engineering effort redirected to agent chat-output design.
- **2026-05-04:** Competitive scout of three known forks. Only one (`Roshan-B87/po-adk-python-syncshift`) is a real submission — single agent, read-only FHIR, no demo, no hosted endpoint, no Marketplace publish evidence. Strategic case strengthened, not weakened. See §13.
- **2026-05-04:** Verified PO homepage at `promptopinion.ai`. Confirmed: assembly platform built on MCP / A2A / FHIR; four agent sources (Platform Templates, Native Custom Agents, External Agents, MCP Tools & Servers); 5T deliverable framework (Talk, Template, Table, Transaction, Task). Our project hits 4 of 5 Ts in one workflow — added to §2 and §10 as the platform-fit credibility move. Discord URL corrected to `discord.gg/cCBxKpdS7j` (the homepage canonical). SHARP and COIN are not on the marketing homepage — keep those terms in the technical plan but use PO's homepage vocabulary in Devpost copy.
- **2026-05-04:** Cloned upstream templates (`prompt-opinion/po-adk-python`, `prompt-opinion/po-community-mcp`) and inspected. Resolved 5 of 8 Day-1 questions before any code:
  - Agent card filename: `/.well-known/agent-card.json` (not `agent.json`).
  - a2a-sdk version: stay on 0.3.x with template shims (`AgentCardV1`, `AgentExtensionV1`).
  - MCP transport: Streamable HTTP via FastAPI mount.
  - MCP-side FHIR transport: lowercase headers `x-fhir-server-url`, `x-fhir-access-token`, `x-patient-id`.
  - **A2A-side FHIR transport: NOT headers — A2A `params.metadata` keyed by `{PO_PLATFORM_BASE_URL}/schemas/a2a/v1/fhir-context`. Two transports total (one per protocol), not the single SHARP-headers model implied by `sharponmcp.com`.**
- **2026-05-04:** Day 1 build kicked off. Project layout: `agents/{orchestrator,pharmacy,home_health}/` + `mcp/careplan_composer/` + `shared/` (from po-adk-python) + `scenarios/postpartum_demo_patient.json` + top-level `Dockerfile`/`requirements.txt`/`.env.example`/`README.md`. Pharmacy and Home Health each ship 3 constraint-locked random scenarios. Orchestrator's tools call Pharmacy and Home Health over real HTTP A2A (`agents/orchestrator/a2a_client.py`) and CarePlan Composer over MCP Streamable HTTP (`agents/orchestrator/mcp_client.py`) — no in-process AgentTool delegation. The template's `orchestrator/` pattern (in-process AgentTool) is explicitly rejected as it would fail the multi-agent litmus test in §8.
