import asyncio
import logging
import os
import uuid
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_TIMEOUT = 30.0


async def _call(url: str, api_key: str, message: str, fhir_metadata: dict | None = None) -> str:
    payload: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": message}],
                "messageId": str(uuid.uuid4()),
            }
        },
    }
    if fhir_metadata:
        payload["params"]["metadata"] = fhir_metadata

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        body = response.json()

    return _extract_text(body)


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


async def call_pharmacy(message: str) -> str:
    url = os.getenv("PHARMACY_URL", "http://localhost:8082").rstrip("/")
    api_key = os.getenv("PHARMACY_API_KEY", "")
    logger.info("orchestrator_a2a_call target=pharmacy url=%s", url)
    return await _call(f"{url}/", api_key, message)


async def call_home_health(message: str) -> str:
    url = os.getenv("HOME_HEALTH_URL", "http://localhost:8083").rstrip("/")
    api_key = os.getenv("HOME_HEALTH_API_KEY", "")
    logger.info("orchestrator_a2a_call target=home_health url=%s", url)
    return await _call(f"{url}/", api_key, message)


def call_pharmacy_sync(message: str) -> str:
    return asyncio.run(call_pharmacy(message))


def call_home_health_sync(message: str) -> str:
    return asyncio.run(call_home_health(message))


async def call_both(pharmacy_msg: str, home_health_msg: str) -> dict[str, str]:
    pharmacy_task = asyncio.create_task(call_pharmacy(pharmacy_msg))
    home_health_task = asyncio.create_task(call_home_health(home_health_msg))
    pharmacy_reply, home_health_reply = await asyncio.gather(
        pharmacy_task, home_health_task, return_exceptions=True
    )
    return {
        "pharmacy": str(pharmacy_reply) if not isinstance(pharmacy_reply, str) else pharmacy_reply,
        "home_health": str(home_health_reply) if not isinstance(home_health_reply, str) else home_health_reply,
    }


def call_both_sync(pharmacy_msg: str, home_health_msg: str) -> dict[str, str]:
    return asyncio.run(call_both(pharmacy_msg, home_health_msg))
