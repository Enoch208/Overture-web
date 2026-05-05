import json
from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from mcp_utilities import create_text_response


async def identify_transition_needs(
    discharge_summary: Annotated[str, Field(description="JSON-stringified discharge summary returned by GetDischargeSummary.")],
    ctx: Context = None,
):
    try:
        summary = json.loads(discharge_summary)
    except json.JSONDecodeError:
        return create_text_response("discharge_summary must be valid JSON.", is_error=True)

    needs = {
        "medications_to_dispense": [],
        "home_services": [],
        "follow_ups": [],
        "monitoring": [],
    }

    for med in summary.get("medications", []):
        concept = med.get("medicationCodeableConcept", {})
        name = concept.get("text") or _first_display(concept.get("coding", []))
        dose_text = (med.get("dosageInstruction") or [{}])[0].get("text")
        needs["medications_to_dispense"].append({
            "name": name,
            "dose": dose_text,
            "rxnorm": _first_code(concept.get("coding", []), "http://www.nlm.nih.gov/research/umls/rxnorm"),
        })

    for svc in summary.get("service_requests", []):
        code = svc.get("code", {})
        category = (svc.get("category") or [{}])[0]
        item = {
            "name": code.get("text") or _first_display(code.get("coding", [])),
            "snomed": _first_code(code.get("coding", []), "http://snomed.info/sct"),
            "category": (category.get("text") or _first_display(category.get("coding", []))),
        }
        bucket = needs["home_services"] if "home" in (item["category"] or "").lower() else needs["follow_ups"]
        bucket.append(item)

    for cond in summary.get("conditions", []):
        code = cond.get("code", {})
        cond_name = code.get("text") or _first_display(code.get("coding", []))
        if cond_name and any(k in cond_name.lower() for k in ["preeclampsia", "hypertension", "gestational"]):
            needs["monitoring"].append({"name": cond_name, "frequency": "BP twice daily for 7 days"})

    return create_text_response(json.dumps(needs, indent=2))


def _first_display(codings: list) -> str | None:
    for c in codings:
        if c.get("display"):
            return c["display"]
    return None


def _first_code(codings: list, system: str) -> str | None:
    for c in codings:
        if c.get("system") == system:
            return c.get("code")
    return None
