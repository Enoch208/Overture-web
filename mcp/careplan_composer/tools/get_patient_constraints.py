import json

from mcp.server.fastmcp import Context

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context, get_patient_id
from mcp_utilities import create_text_response


async def get_patient_constraints(ctx: Context = None):
    fhir = get_fhir_context(ctx)
    patient_id = get_patient_id(ctx)
    if not fhir or not patient_id:
        return create_text_response("Missing FHIR context or patient id.", is_error=True)

    client = FhirClient(base_url=fhir.url, token=fhir.token)
    patient = await client.read(f"Patient/{patient_id}") or {}
    coverage = await client.search("Coverage", {"patient": patient_id, "_count": "5"}) or {}

    address = (patient.get("address") or [{}])[0]
    constraints = {
        "patient_id": patient_id,
        "language": _primary_language(patient),
        "zip_code": address.get("postalCode"),
        "city": address.get("city"),
        "state": address.get("state"),
        "marital_status": (patient.get("maritalStatus") or {}).get("text"),
        "coverage": [
            {
                "payor": (e.get("resource") or {}).get("payor", [{}])[0].get("display"),
                "plan": ((e.get("resource") or {}).get("class") or [{}])[0].get("name"),
                "status": (e.get("resource") or {}).get("status"),
            }
            for e in (coverage.get("entry") or [])
        ],
    }
    return create_text_response(json.dumps(constraints, indent=2))


def _primary_language(patient: dict) -> str | None:
    for c in patient.get("communication", []):
        if c.get("preferred"):
            lang = (c.get("language") or {})
            return lang.get("text") or _first_display(lang.get("coding", []))
    return None


def _first_display(codings: list) -> str | None:
    for c in codings:
        if c.get("display"):
            return c["display"]
    return None
