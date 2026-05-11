"""
Manual end-to-end test against the local Discharge Orchestrator (A2A).

Runs the full multi-agent flow: orchestrator -> pharmacy + home_health (A2A) +
careplan_composer (MCP) -> validated CarePlan.

Prereqs:
  - All four services running (8080 orchestrator, 8082 pharmacy, 8083 home health, 8081 MCP)
  - .env populated with ORCHESTRATOR_API_KEY (and the agent-to-agent keys)
  - A FHIR-enabled workspace OR pass FHIR metadata inline (see FHIR_METADATA below)

Usage:
    python -m scripts.test_orchestrator
"""

import asyncio
import os
import uuid

import httpx
from dotenv import load_dotenv

load_dotenv()

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8080").rstrip("/")
ORCHESTRATOR_API_KEY = os.getenv("ORCHESTRATOR_API_KEY", "")

PROMPT = (
    "Consult the Discharge Orchestrator. Compose the 30-day post-discharge plan, "
    "but specifically confirm same-day medication delivery and a postpartum nurse "
    "visit within 24 hours. Surface any blockers."
)

# When called from Prompt Opinion these are injected automatically. For local
# testing, point at a FHIR server that has the postpartum demo bundle loaded
# (or leave empty and the orchestrator will skip MCP reads).
FHIR_METADATA = {
    # "fhir_server_url": "https://your-fhir-server/fhir",
    # "fhir_access_token": "your-bearer-token",
    # "patient_id": "a8e3f1c2-9d4b-4f7a-b1e6-3d8c5a2f9e10",
}


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": PROMPT}],
                "messageId": str(uuid.uuid4()),
            }
        },
    }
    if FHIR_METADATA:
        payload["params"]["metadata"] = FHIR_METADATA

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ORCHESTRATOR_API_KEY,
    }

    print(f"POST {ORCHESTRATOR_URL}/")
    print(f"prompt: {PROMPT}\n")

    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(f"{ORCHESTRATOR_URL}/", json=payload, headers=headers)
        response.raise_for_status()
        body = response.json()

    print("--- raw JSON-RPC response ---")
    import json
    print(json.dumps(body, indent=2)[:4000])
    print("\n--- extracted text ---")
    print(_extract_text(body))


def _extract_text(body: dict) -> str:
    result = body.get("result") or {}
    artifacts = (result.get("status") or {}).get("message", {}).get("parts") or result.get("artifacts") or []
    if isinstance(artifacts, list):
        for a in artifacts:
            parts = a.get("parts", [a]) if isinstance(a, dict) else []
            for p in parts:
                if isinstance(p, dict) and p.get("kind") == "text" and p.get("text"):
                    return p["text"]
    parts = (result.get("message") or {}).get("parts", [])
    for p in parts:
        if isinstance(p, dict) and p.get("kind") == "text" and p.get("text"):
            return p["text"]
    if body.get("error"):
        return f"[error from agent: {body['error']}]"
    return str(body)


if __name__ == "__main__":
    asyncio.run(main())
