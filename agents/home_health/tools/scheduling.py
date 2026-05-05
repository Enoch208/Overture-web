import json
import logging
import random
from pathlib import Path

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

_STATE_PATH = Path(__file__).resolve().parents[1] / "data" / "home_health_state.json"
_STATE = json.loads(_STATE_PATH.read_text())


def _default_scenario_id() -> str:
    for s in _STATE["scenarios"]:
        if s.get("is_default"):
            return s["id"]
    return _STATE["scenarios"][-1]["id"]


def _match_scenario_id(hint: str) -> str:
    h = hint.lower()
    for s in _STATE["scenarios"]:
        for kw in s.get("match_keywords", []):
            if kw.lower() in h:
                return s["id"]
    return _default_scenario_id()


def _scenario(tool_context: ToolContext, hint: str = "") -> dict:
    sid = tool_context.state.get("home_health_scenario_id")
    if not sid:
        sid = _match_scenario_id(hint) if hint else _default_scenario_id()
        tool_context.state["home_health_scenario_id"] = sid
        logger.info("home_health_scenario_locked id=%s hint=%r", sid, hint[:80])
    return next(s for s in _STATE["scenarios"] if s["id"] == sid)


def check_capacity(zip_code: str, services_needed: list[str], tool_context: ToolContext) -> dict:
    """
    Check service-area coverage and same-week capacity for a list of services.

    Args:
        zip_code: Patient's ZIP code.
        services_needed: e.g. ["bp_monitoring", "postpartum_visit", "lactation_support"].
    """
    org = _STATE["organization"]
    zip_clean = (zip_code or "").strip()
    if not zip_clean:
        in_area = True
    else:
        in_area = zip_clean in org["service_area_zips"]
    hint = " ".join(services_needed) if in_area else "out of area"
    scenario = _scenario(tool_context, hint=hint)

    supported = [s for s in services_needed if s in org["services_offered"]]
    unsupported = [s for s in services_needed if s not in org["services_offered"]]

    return {
        "organization": org,
        "scenario": scenario["id"],
        "narrative": scenario["narrative"],
        "in_service_area": in_area,
        "caseload_status": scenario["caseload_status"],
        "partner_agency": scenario.get("partner_agency"),
        "supported_services": supported,
        "unsupported_services": unsupported,
    }


def propose_window(service: str, tool_context: ToolContext) -> dict:
    """
    Propose an available delivery / visit window for a specific service.

    Args:
        service: One of the agency's offered services, e.g. "dme_delivery", "postpartum_visit", "lactation_support".
    """
    scenario = _scenario(tool_context, hint=service)
    matches = [w for w in scenario["windows"] if w["service"] == service]
    if not matches:
        matches = [{
            "service": service,
            "earliest": "2026-05-06T09:00:00Z",
            "latest": "2026-05-06T17:00:00Z",
            "note": "Generic next-day window — confirm with caseload coordinator.",
        }]
    return {
        "organization": _STATE["organization"],
        "service": service,
        "windows": matches,
        "requires_patient_confirmation": True,
    }


def confirm_assignment(service: str, window_start: str, tool_context: ToolContext) -> dict:
    """
    Confirm a service assignment to the agency caseload.

    Args:
        service: Service being scheduled.
        window_start: ISO 8601 start time the patient agreed to.
    """
    return {
        "organization": _STATE["organization"],
        "assignment_id": f"HH-{random.randint(100000, 999999)}",
        "service": service,
        "window_start": window_start,
        "status": "confirmed",
        "assigned_clinician": "Beacon RN floater pool",
    }
