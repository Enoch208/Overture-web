import json
from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context
from mcp_utilities import create_text_response

US_CORE_CAREPLAN_PROFILE = "http://hl7.org/fhir/us/core/StructureDefinition/us-core-careplan"


async def validate_and_write_care_plan(
    care_plan: Annotated[str, Field(description="JSON-stringified CarePlan resource (US Core profile).")],
    ctx: Context = None,
):
    try:
        plan = json.loads(care_plan)
    except json.JSONDecodeError:
        return create_text_response("care_plan must be valid JSON.", is_error=True)

    issues = []

    if plan.get("resourceType") != "CarePlan":
        issues.append("resourceType must be 'CarePlan'.")

    profile = (plan.get("meta") or {}).get("profile") or []
    if US_CORE_CAREPLAN_PROFILE not in profile:
        issues.append(f"meta.profile must include '{US_CORE_CAREPLAN_PROFILE}'.")

    for required in ("text", "status", "intent", "category", "subject"):
        if required not in plan:
            issues.append(f"missing required element '{required}'.")

    if plan.get("status") not in {"draft", "active", "on-hold", "revoked", "completed", "entered-in-error", "unknown"}:
        issues.append(f"invalid status '{plan.get('status')}'.")

    text = plan.get("text") or {}
    if text.get("status") not in {"generated", "extensions", "additional", "empty"} or not text.get("div"):
        issues.append("text.status and text.div are required for US Core narrative.")

    activities = plan.get("activity") or []
    if not activities:
        issues.append("at least one CarePlan.activity is required to attribute org contributions.")

    for i, act in enumerate(activities):
        ref = act.get("reference") or act.get("plannedActivityReference") or {}
        if not (ref.get("reference") or act.get("detail")):
            issues.append(f"activity[{i}] needs either a reference or a detail block.")

    if issues:
        return create_text_response(json.dumps({
            "valid": False,
            "profile": US_CORE_CAREPLAN_PROFILE,
            "issues": issues,
        }, indent=2), is_error=True)

    fhir = get_fhir_context(ctx)
    if not fhir:
        return create_text_response("Validation passed but FHIR context is missing — cannot write.", is_error=True)

    client = FhirClient(base_url=fhir.url, token=fhir.token)
    created = await client.create("CarePlan", plan)
    return create_text_response(json.dumps({
        "valid": True,
        "profile": US_CORE_CAREPLAN_PROFILE,
        "issues": [],
        "resource_id": created.get("id"),
        "resource_type": created.get("resourceType"),
        "version_id": (created.get("meta") or {}).get("versionId"),
        "last_updated": (created.get("meta") or {}).get("lastUpdated"),
    }, indent=2))
