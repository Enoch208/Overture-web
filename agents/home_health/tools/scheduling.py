import json
import logging
import random
from pathlib import Path

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

_STATE_PATH = Path(__file__).resolve().parents[1] / "data" / "home_health_state.json"
_STATE = json.loads(_STATE_PATH.read_text())


def _scenario(tool_context: ToolContext) -> dict:
    sid = tool_context.state.get("home_health_scenario_id")
    if not sid:
        sid = random.choice(_STATE["scenarios"])["id"]
        tool_context.state["home_health_scenario_id"] = sid
        logger.info("home_health_scenario_locked id=%s", sid)
    return next(s for s in _STATE["scenarios"] if s["id"] == sid)


def check_capacity(zip_code: str, services_needed: list[str], tool_context: ToolContext) -> dict:
    """
    Check service-area coverage and same-week capacity for a list of services.

    Args:
        zip_code: Patient's ZIP code.
        services_needed: e.g. ["bp_monitoring", "postpartum_visit", "lactation_support"].
    """
    scenario = _scenario(tool_context)
    org = _STATE["organization"]

    in_area = zip_code in org["service_area_zips"]
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
    scenario = _scenario(tool_context)
    matches = [w for w in scenario["windows"] if w["service"] == service]
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
