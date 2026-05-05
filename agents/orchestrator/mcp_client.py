import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_TIMEOUT = 30.0


def _headers(fhir_url: str, fhir_token: str, patient_id: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if fhir_url:
        headers["x-fhir-server-url"] = fhir_url
    if fhir_token:
        headers["x-fhir-access-token"] = fhir_token
    if patient_id:
        headers["x-patient-id"] = patient_id
    return headers


def _parse_response(response: httpx.Response) -> dict:
    content_type = response.headers.get("content-type", "")
    if "text/event-stream" in content_type:
        for line in response.text.splitlines():
            if line.startswith("data:"):
                payload = line[len("data:"):].strip()
                if payload and payload != "[DONE]":
                    return json.loads(payload)
        raise ValueError(f"No JSON data found in SSE response: {response.text[:300]!r}")
    return response.json()


async def call_tool(tool_name: str, arguments: dict[str, Any], fhir_url: str = "", fhir_token: str = "", patient_id: str = "") -> dict:
    base = os.getenv("CAREPLAN_MCP_URL", "http://localhost:8081").rstrip("/")
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    logger.info("orchestrator_mcp_call tool=%s", tool_name)
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        response = await client.post(
            f"{base}/mcp",
            json=payload,
            headers=_headers(fhir_url, fhir_token, patient_id),
        )
        response.raise_for_status()
        return _parse_response(response)
