# Care Transition Orchestrator — System Architecture

Companion to [goal.md](goal.md). This doc covers the **how**: services, ports, URLs, data flow, auth, state, repo layout.

## 1. The Five Boxes

Two layers: what we own, what Prompt Opinion provides.

```
╔═══════════════════════════════════════════════════════════════╗
║  PROMPT OPINION (THEIRS — we do not deploy this)              ║
║  ───────────────────────────────────────────────              ║
║                                                                ║
║   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐     ║
║   │  Launchpad   │   │  User Agent  │   │ FHIR Server  │     ║
║   │   (chat UI)  │──►│ (general     │──►│  (workspace) │     ║
║   │              │   │  chat / pt.) │   │              │     ║
║   └──────────────┘   └──────┬───────┘   └──────▲───────┘     ║
║                             │                   │             ║
║                             │ A2A + SHARP       │             ║
║                             │ (FHIR token       │             ║
║                             │  in headers)      │             ║
║                             ▼                   │             ║
║   ┌─────────────────────────────────────────────│──────┐     ║
║   │  Marketplace Studio (publish target)        │      │     ║
║   └─────────────────────────────────────────────┼──────┘     ║
║                                                 │             ║
╚═════════════════════════════════════════════════│═════════════╝
                                                  │
                            ╔═════════════════════│════════════════════╗
                            ║  OUR BUILD          │                    ║
                            ║  ───────            │                    ║
                            ║                     ▼                    ║
                            ║   ┌────────────────────────────────┐    ║
                            ║   │  DISCHARGE ORCHESTRATOR        │    ║
                            ║   │  Cloud Run · port 8080          │    ║
                            ║   │  GET /.well-known/agent-card.json    │    ║
                            ║   │  POST /a2a (message/send)       │    ║
                            ║   │                                 │    ║
                            ║   │  - Receives FHIR token (SHARP)  │    ║
                            ║   │  - Calls MCP for chart reads    │    ║
                            ║   │  - Opens parallel A2A calls     │    ║
                            ║   │  - Calls MCP for write          │    ║
                            ║   │  - Returns final chat response  │    ║
                            ║   └─┬────────────┬────────────┬─────┘    ║
                            ║     │            │            │          ║
                            ║     │ MCP-HTTP   │ A2A        │ A2A      ║
                            ║     │ (with      │ (no FHIR   │ (no FHIR ║
                            ║     │  FHIR      │  token)    │  token)  ║
                            ║     │  token)    │            │          ║
                            ║     ▼            ▼            ▼          ║
                            ║  ┌─────────┐ ┌─────────┐ ┌──────────┐  ║
                            ║  │ CAREPLAN│ │PHARMACY │ │ HOME     │  ║
                            ║  │ COMPOSER│ │ AGENT   │ │ HEALTH   │  ║
                            ║  │ (MCP)   │ │         │ │ AGENT    │  ║
                            ║  │ port    │ │ port    │ │ port     │  ║
                            ║  │ 8081    │ │ 8082    │ │ 8083     │  ║
                            ║  └────┬────┘ └─────────┘ └──────────┘  ║
                            ║       │                                 ║
                            ║       │ FHIR R4 REST                    ║
                            ║       │ (read + write)                  ║
                            ╚═══════│═════════════════════════════════╝
                                    │
                    back into PO FHIR server (above)
```

**Five boxes total:** Discharge Orchestrator, Pharmacy Agent, Home Health Agent, CarePlan Composer MCP — and the Frontend, which is hackathon-irrelevant (marketing only).

## 2. Service Contract Per Box

| Service | Type | Port (local) | Endpoint | Speaks |
|---------|------|--------------|----------|--------|
| Discharge Orchestrator | A2A agent | 8080 | `/a2a` + `/.well-known/agent-card.json` | A2A in (from PO), MCP-HTTP out, A2A out |
| Pharmacy Agent | A2A agent | 8082 | same | A2A in (from Orchestrator only) |
| Home Health Agent | A2A agent | 8083 | same | A2A in (from Orchestrator only) |
| CarePlan Composer | MCP server | 8081 | `/MCP` (Streamable HTTP) | MCP-HTTP in, FHIR REST out |

Each runs as its own Cloud Run service. Stable URL per service. Each agent's `agent.json` points at its own URL — that's how PO's User Agent finds it.

## 3. The Happy Path (one full request)

```
Judge                    User Agent          Orchestrator       MCP        Pharmacy    HomeHealth    PO FHIR
  │                          │                    │              │            │             │           │
  │ click "compose plan"     │                    │              │            │             │           │
  ├─────────────────────────►│                    │              │            │             │           │
  │                          │ A2A message/send   │              │            │             │           │
  │                          │ + SHARP headers    │              │            │             │           │
  │                          │ (FHIR token)       │              │            │             │           │
  │                          ├───────────────────►│              │            │             │           │
  │                          │                    │ get_discharge_summary    │             │           │
  │                          │                    ├─────────────►│            │             │           │
  │                          │                    │              │ GET Encounter, Cond, Med            │
  │                          │                    │              ├──────────────────────────────────────►
  │                          │                    │              │◄──────────────────────────────────────
  │                          │                    │◄─────────────┤            │             │           │
  │                          │                    │ identify_transition_needs │             │           │
  │                          │                    ├─────────────►│            │             │           │
  │                          │                    │◄─────────────┤            │             │           │
  │                          │                    │                                                      │
  │                          │                    │ A2A: drug list                                       │
  │                          │                    ├─────────────────────────►│             │           │
  │                          │                    │ A2A: address + services  │             │           │
  │                          │                    ├──────────────────────────────────────►│             │
  │                          │                    │                          │ ▲ parallel ▲│           │
  │                          │                    │◄─────────────────────────┤             │           │
  │                          │                    │   "labetalol on backorder, propose nifedipine"      │
  │                          │                    │◄──────────────────────────────────────┤             │
  │                          │                    │   "BP cuff slot 4–6pm only"                          │
  │                          │                    │                                                      │
  │                          │                    │ ask user: "delivery 4–6pm OK?"                       │
  │                          │◄───────────────────┤              │            │             │           │
  │ "yes"                    │                    │              │            │             │           │
  ├─────────────────────────►├───────────────────►│              │            │             │           │
  │                          │                    │ validate_care_plan       │             │           │
  │                          │                    ├─────────────►│            │             │           │
  │                          │                    │◄─────────────┤ ✓ US Core │             │           │
  │                          │                    │ write_care_plan          │             │           │
  │                          │                    ├─────────────►│            │             │           │
  │                          │                    │              │ POST CarePlan                        │
  │                          │                    │              ├──────────────────────────────────────►
  │                          │                    │              │◄──────────────────────────────────────
  │                          │                    │◄─────────────┤ resource id              │           │
  │                          │ final chat msg     │              │            │             │           │
  │                          │ (per-org transcript│              │            │             │           │
  │                          │  + CarePlan JSON   │              │            │             │           │
  │                          │  + ✓ validated     │              │            │             │           │
  │                          │  + FHIR id)        │              │            │             │           │
  │◄─────────────────────────┤                    │              │            │             │           │
```

That's the demo, end-to-end, in one diagram.

## 4. Authentication — Three Separate Concerns

Easy to confuse. Keep them separate.

### A. FHIR auth (read/write the patient's chart)
- PO captures the SMART-on-FHIR access token at user login.
- PO injects it into A2A messages as **SHARP headers** (`X-FHIR-Server-URL`, `X-FHIR-Access-Token`).
- Orchestrator receives the token and **forwards to MCP only**.
- Orchestrator does **NOT** forward to Pharmacy/Home Health (cross-org realism: external orgs don't see the chart).

### B. Inter-agent auth (Orchestrator → Pharmacy / Home Health)
- OAuth2 client-credentials, audience-scoped.
- Each agent has its own `client_id` / `client_secret`.
- For the hackathon: simple JWT signed with a per-agent secret is fine. Don't overbuild.
- Each agent verifies the JWT before processing the A2A request.

### C. PO calling our agents (entrypoint auth)
- Agent card at `/.well-known/agent-card.json` is **public** (so PO can discover it).
- The actual `/a2a` endpoint requires an API key — judges paste this when registering the agent in PO Workspace Hub (per the quick-start video: *"this agent requires a key... I can just copy that key and paste it here"*).
- One static API key per agent, set as Cloud Run env var. Document each in the Devpost description.

## 5. State & Data Ownership

| Service | Persistent state | Per-request state | Data source |
|---------|------------------|-------------------|-------------|
| Discharge Orchestrator | None | In-memory negotiation transcript | FHIR (via MCP) |
| Pharmacy Agent | `pharmacy_state.json` (inventory + backorder + benefits) — **randomized at startup, constraint-locked** | In-memory request log | Own state file |
| Home Health Agent | `home_health_state.json` (scheduling grid, capacity by zip) — **randomized at startup, constraint-locked** | In-memory request log | Own state file |
| CarePlan Composer | None | In-memory plan being built | PO's FHIR server |

**Constraint-locked randomization:** the state always has *some* interesting failure mode (a backorder OR a PA blocker; a timing constraint OR a service-area gap). The variable is *which* of N pre-defined "interesting" states this run hits, not whether anything is interesting at all. Guarantees the demo works every time a judge probes.

## 6. Repo Layout

```
overture/
├── goal.md
├── architecture.md          ← this file
├── CLAUDE.md
├── frontend/                ← marketing only (out of scope for hackathon)
│
├── agents/
│   ├── orchestrator/
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── agent_card.json
│   │   └── src/
│   │       ├── main.py              ← FastAPI + a2a-sdk server
│   │       ├── orchestrator.py      ← Google ADK agent definition
│   │       ├── negotiation.py       ← parallel A2A call orchestration
│   │       ├── mcp_client.py        ← Streamable-HTTP client for Composer
│   │       └── a2a_clients.py       ← clients for Pharmacy + HomeHealth
│   │
│   ├── pharmacy/
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── agent_card.json
│   │   ├── data/pharmacy_state.json
│   │   └── src/
│   │       ├── main.py
│   │       ├── agent.py
│   │       ├── inventory.py         ← state loader + constraint-locked randomizer
│   │       └── tools/
│   │           ├── check_availability.py
│   │           └── propose_substitution.py
│   │
│   └── home_health/
│       ├── Dockerfile
│       ├── pyproject.toml
│       ├── agent_card.json
│       ├── data/home_health_state.json
│       └── src/
│           ├── main.py
│           ├── agent.py
│           ├── scheduling.py        ← state loader + randomizer
│           └── tools/
│               ├── check_capacity.py
│               └── propose_window.py
│
├── mcp/
│   └── careplan_composer/
│       ├── Dockerfile
│       ├── pyproject.toml
│       ├── resources/validator.jar  ← HL7 FHIR Validator
│       └── src/
│           ├── main.py              ← MCP HTTP server (Streamable HTTP)
│           ├── tools.py             ← @tool decorators
│           ├── fhir_client.py       ← reads/writes via SHARP token
│           └── validator.py         ← invokes validator.jar with US Core IG
│
├── shared/
│   ├── fhir_models.py               ← Pydantic CarePlan model
│   └── scenarios/
│       └── postpartum_demo_patient.json   ← FHIR Bundle for one-click import
│
└── deploy/
    ├── orchestrator.yaml            ← Cloud Run service config
    ├── pharmacy.yaml
    ├── home_health.yaml
    └── careplan_composer.yaml
```

## 7. Tech Stack Per Service

| Layer | Choice | Why |
|-------|--------|-----|
| Language | Python 3.11+ | PO templates are Python; team familiarity; richest A2A/MCP support |
| Agent framework | Google ADK | What `po-adk-python` ships with; ADK has built-in A2A |
| A2A SDK | `a2a-sdk` (PyPI, Linux Foundation) | The official SDK; `po-adk-python` already bundles 0.3.x with v1 shims |
| MCP SDK | `mcp` Python SDK | Streamable HTTP transport; what PO recognizes |
| FHIR library | `fhir.resources` | Pydantic models for FHIR R4 + US Core profiles |
| Validation | HL7 FHIR Validator (java jar) | Canonical CI tool with `-ig hl7.fhir.us.core` flag |
| LLM | Gemini 2.0 Flash via Google AI Studio | What the PO quick-start video uses; free tier sufficient |
| Web framework | FastAPI | A2A SDK examples use it; async native |
| Container | Docker | One image per service |
| Hosting | Google Cloud Run | Stable URLs, easy deploys, Gemini-region affinity |
| Secrets | Cloud Run env vars | API keys, OAuth secrets |

## 8. Agent Card Shape (Discharge Orchestrator)

The most important agent card — the one judges click in PO Marketplace.

```json
{
  "name": "Discharge Orchestrator",
  "description": "Composes a complete 30-day post-discharge care plan via real-time multi-agent negotiation across pharmacy, home health, and patient. Writes a validated US Core CarePlan to FHIR.",
  "url": "https://overture-orchestrator-xxxx.run.app",
  "version": "0.1.0",
  "provider": {
    "organization": "Overture Health",
    "url": "https://overture.health"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "compose_discharge_plan",
      "name": "Compose 30-day discharge plan",
      "description": "Negotiates with pharmacy and home health to build a validated US Core CarePlan for the patient's first 30 days post-discharge.",
      "tags": ["discharge", "care-plan", "transitions-of-care", "us-core", "davinci-pcde"],
      "examples": [
        "Compose the 30-day post-discharge plan for this patient.",
        "What does she need before going home?",
        "Build the discharge plan and write it to FHIR."
      ]
    }
  ]
}
```

The Pharmacy and Home Health agent cards mirror this shape with their own `skills.examples`.

## 9. Mapping to the 7-Day Plan

| Day | Architecture milestone |
|-----|------------------------|
| **Day 1** | Empty Cloud Run services up for all 4 boxes. Hello-world A2A agent registered in PO Workspace Hub end-to-end. Agent-card filename locked. SHARP header receipt verified in MCP. |
| **Day 2** | All 3 agents deployed with real agent cards + auth. Orchestrator opens parallel A2A calls (Pharmacy/HomeHealth return mock JSON). |
| **Day 3** | CarePlan Composer MCP deployed. FHIR reads working through SHARP. Synthetic patient bundle imported into PO. |
| **Day 4** | Pharmacy + Home Health implemented with real state files + constraint-locked randomization. Orchestrator writes a CarePlan (unvalidated) to FHIR. **Cut decision: drop to 2 agents if not on track.** |
| **Day 5** | US Core validation working in `validate_care_plan`. Validation passes on the demo scenario. Clinician sanity-call. |
| **Day 6** | Chat-output design: per-org attribution, A2A trace render, CarePlan JSON artifact. Three video takes recorded. |
| **Day 7** | Devpost copy. Marketplace publish confirmed live. Submit by 11pm ET 2026-05-11. |

## 10. Open Architecture Questions (resolve Day 1)

Resolved by reading the upstream templates on 2026-05-04:

1. ~~**Agent-card filename.**~~ ✅ Confirmed: `/.well-known/agent-card.json` (per `po-adk-python/healthcare_agent/app.py` — `to_a2a()` mounts it there).
2. ~~**`a2a-sdk` version.**~~ ✅ Decided: stay on 0.3.x with `AgentCardV1` + `AgentExtensionV1` shims (already implemented in `shared/app_factory.py`). Don't fight it.
3. ~~**MCP transport.**~~ ✅ Confirmed: Streamable HTTP (`mcp.streamable_http_app()` mounted on FastAPI).
4. ~~**SHARP header names** (MCP side).~~ ✅ Confirmed lowercase: `x-fhir-server-url`, `x-fhir-access-token`, `x-patient-id`. Source: `po-community-mcp/python/mcp_constants.py`.
5. ~~**FHIR transport on the A2A side.**~~ ✅ Confirmed: NOT headers — FHIR creds ride inside A2A `params.metadata` keyed by `{PO_PLATFORM_BASE_URL}/schemas/a2a/v1/fhir-context` with `{fhirUrl, fhirToken, patientId}`. The `extract_fhir_context` ADK callback in `shared/fhir_hook.py` handles extraction. Two transports total: A2A → metadata; MCP → headers.

Still open (verify in Day 1 with PO):

6. **Suggestion-chip rendering.** Does PO Launchpad render `skills.examples` as clickable chips? Verify Day 1; if not, fall back to Devpost "Quick Test" copy.
7. **Whether Pharmacy/Home Health need to be published in Marketplace** for the multi-agent story to count, or whether private endpoints called by the published Orchestrator is acceptable. Ask in Discord. Default plan: publish all three.
8. **Marketplace publish latency.** Push a hello-world agent on Day 1, time the publish-to-discoverable interval.
