import json
import logging
import random
from pathlib import Path

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

_STATE_PATH = Path(__file__).resolve().parents[1] / "data" / "pharmacy_state.json"
_STATE = json.loads(_STATE_PATH.read_text())


def _scenario(tool_context: ToolContext) -> dict:
    sid = tool_context.state.get("pharmacy_scenario_id")
    if not sid:
        sid = random.choice(_STATE["scenarios"])["id"]
        tool_context.state["pharmacy_scenario_id"] = sid
        logger.info("pharmacy_scenario_locked id=%s", sid)
    return next(s for s in _STATE["scenarios"] if s["id"] == sid)


def check_availability(medications: list[str], tool_context: ToolContext) -> dict:
    """
    Check inventory and benefits for a list of medications.

    Args:
        medications: A list of medication names with strength, e.g. ["labetalol 200mg", "nifedipine ER 30mg"].
    """
    scenario = _scenario(tool_context)
    inventory = scenario["inventory"]

    findings = []
    for med in medications:
        match = next((k for k in inventory if k.lower() in med.lower() or med.lower() in k.lower()), None)
        if not match:
            findings.append({"medication": med, "stocked": False, "reason": "not in formulary"})
            continue
        item = inventory[match]
        findings.append({
            "medication": match,
            "stocked": item.get("in_stock", False),
            "backorder_until": item.get("backorder_until"),
            "prior_auth_required": item.get("pa_required", False),
            "prior_auth_reason": item.get("pa_reason"),
            "copay_usd": item.get("copay_estimate_usd"),
        })

    return {
        "organization": _STATE["organization"],
        "scenario": scenario["id"],
        "narrative": scenario["narrative"],
        "delivery_window": scenario.get("delivery_window"),
        "findings": findings,
    }


def propose_substitution(blocked_medication: str, indication: str, tool_context: ToolContext) -> dict:
    """
    Propose a clinically appropriate substitute for a blocked medication.

    Args:
        blocked_medication: The medication that cannot be dispensed (backorder, PA required, etc.).
        indication: The clinical indication, e.g. "postpartum hypertension".
    """
    scenario = _scenario(tool_context)
    inventory = scenario["inventory"]

    candidates = [
        {"medication": k, "copay_usd": v.get("copay_estimate_usd")}
        for k, v in inventory.items()
        if v.get("in_stock") and not v.get("pa_required") and k.lower() not in blocked_medication.lower()
    ]

    return {
        "organization": _STATE["organization"],
        "blocked": blocked_medication,
        "indication": indication,
        "proposals": candidates,
        "requires_prescriber_confirmation": True,
        "rationale": "All proposals are first-line per ACOG for the indication. Prescriber must confirm before substitution dispensed.",
    }


def confirm_dispense(medication: str, dose: str, tool_context: ToolContext) -> dict:
    """
    Confirm dispense of an approved medication.

    Args:
        medication: Medication name with strength.
        dose: Dosing instruction, e.g. "1 tab PO BID".
    """
    scenario = _scenario(tool_context)
    delivery = scenario.get("delivery_window") or {
        "earliest": "2026-05-05T10:00:00Z",
        "latest": "2026-05-05T18:00:00Z",
    }
    return {
        "organization": _STATE["organization"],
        "dispense_id": f"RX-{random.randint(100000, 999999)}",
        "medication": medication,
        "dose": dose,
        "delivery_window": delivery,
        "status": "confirmed",
    }
