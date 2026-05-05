# Overture — Care Transition Orchestrator

Multi-agent A2A system that composes a complete 30-day post-discharge care plan via real-time negotiation across pharmacy, home health, and the patient. Built for **Agents Assemble — The Healthcare AI Endgame** on Prompt Opinion (Devpost deadline 2026-05-11).

See [goal.md](goal.md) for strategy, [architecture.md](architecture.md) for system design.

## What ships

| Service | Type | Port | What it does |
|---------|------|------|--------------|
| `agents/orchestrator` | A2A agent | 8080 | The published headline agent. Reads FHIR via MCP, opens parallel A2A calls, writes validated CarePlan. |
| `agents/pharmacy` | A2A agent | 8082 | Specialty pharmacy — owns inventory, benefits, delivery. Constraint-locked random state. |
| `agents/home_health` | A2A agent | 8083 | Home health agency — owns scheduling, service area, caseload. Constraint-locked random state. |
| `mcp/careplan_composer` | MCP server | 8081 | FHIR reads + US Core CarePlan validation + write-back. |

## Local setup

```bash
# 1. Install agent deps (one venv for all three agents + shared/)
python -m venv .venv
source .venv/Scripts/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Install MCP deps (separate venv, different framework)
cd mcp/careplan_composer
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cd ../..

# 3. Configure .env
cp .env.example .env
# fill in GOOGLE_API_KEY (https://aistudio.google.com/apikey)
# generate API keys for ORCHESTRATOR_API_KEY / PHARMACY_API_KEY / HOME_HEALTH_API_KEY
```

## Run all four services locally

```bash
# In four terminals:
uvicorn agents.orchestrator.app:a2a_app  --host 0.0.0.0 --port 8080
uvicorn agents.pharmacy.app:a2a_app      --host 0.0.0.0 --port 8082
uvicorn agents.home_health.app:a2a_app   --host 0.0.0.0 --port 8083

# Fourth (MCP — different venv):
cd mcp/careplan_composer && uvicorn main:app --host 0.0.0.0 --port 8081
```

Agent cards served at:
- http://localhost:8080/.well-known/agent-card.json
- http://localhost:8082/.well-known/agent-card.json
- http://localhost:8083/.well-known/agent-card.json

## Register in Prompt Opinion

1. Sign up at https://app.promptopinion.ai. Create a workspace. Add a Google AI Studio API key in Settings → Models (Gemini 2.5 Flash).
2. **Import the demo patient.** Workspace → Patients → Upload FHIR Bundle → `scenarios/postpartum_demo_patient.json`.
3. **Expose each service via ngrok** (until Cloud Run deploys land):
   ```bash
   ngrok http 8080  # repeat for 8082, 8083, 8081 in separate terminals
   ```
4. **Add each agent in Workspace Hub → External Agents → Add Connection:**
   - Paste the ngrok URL → Check (it pulls the agent card)
   - Paste the matching API key (from `.env`)
   - Toggle "requires FHIR context" on for the **Orchestrator only** (Pharmacy + Home Health do not get the FHIR token)
5. **Add the MCP server in Workspace Hub → MCP Servers → Add Connection:**
   - URL: `<ngrok-mcp>/mcp`
   - Toggle "pass FHIR token" on
6. **Wire the MCP into the Orchestrator** in PO: configure agent → Tools → add CarePlan Composer tools.
7. **Test in Launchpad:** select the demo patient as context → choose general chat → ask: *"Consult the Discharge Orchestrator: compose the 30-day post-discharge plan."*

## Day-1 verifications (do these first)

Open verifications in [architecture.md §10](architecture.md):

1. Confirm hello-world Orchestrator card renders in PO Workspace Hub.
2. Confirm `skills.examples` render as suggestion chips in Launchpad (or fall back to copy in description).
3. Confirm the FHIR token reaches the MCP server in headers (log `x-fhir-server-url`, `x-fhir-access-token`).
4. Confirm A2A FHIR metadata reaches the Orchestrator (the `fhir_hook` logs `FHIR_TOKEN_FOUND`).
5. Confirm Marketplace publish flow latency by pushing a hello-world agent on Day 1.
6. Confirm the agent-card filename PO actually fetches (`agent-card.json` per the template).

## Layout

```
overture/
├── agents/
│   ├── orchestrator/
│   │   ├── agent.py             ADK agent + tool wrappers (A2A and MCP clients)
│   │   ├── app.py               A2A server entry
│   │   ├── a2a_client.py        HTTP A2A client to Pharmacy + Home Health
│   │   └── mcp_client.py        Streamable-HTTP client to CarePlan Composer
│   ├── pharmacy/
│   │   ├── agent.py
│   │   ├── app.py
│   │   ├── tools/inventory.py
│   │   └── data/pharmacy_state.json     constraint-locked scenarios
│   └── home_health/
│       ├── agent.py
│       ├── app.py
│       ├── tools/scheduling.py
│       └── data/home_health_state.json
├── mcp/careplan_composer/
│   ├── main.py                 FastAPI host
│   ├── mcp_instance.py         FastMCP + 5 tools registered
│   ├── fhir_client.py          httpx FHIR R4 client (read + create)
│   └── tools/                  the 5 tools
├── shared/                     copied from po-adk-python
│   ├── app_factory.py
│   ├── fhir_hook.py
│   ├── middleware.py
│   └── ...
├── scenarios/
│   └── postpartum_demo_patient.json     one-click FHIR Bundle for judges
├── deploy/                     Cloud Run yamls (filled in Day 5)
├── frontend/                   marketing only — not in build budget
└── templates/                  upstream PO templates kept for reference
```

## Tracking

- [goal.md](goal.md) — strategy, judging targets, decision log, competitive landscape
- [architecture.md](architecture.md) — system design, sequence diagrams, auth model
