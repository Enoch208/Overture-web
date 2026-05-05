import json

from mcp.server.fastmcp import Context

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context, get_patient_id
from mcp_utilities import create_text_response


async def get_discharge_summary(ctx: Context = None):
    fhir = get_fhir_context(ctx)
    patient_id = get_patient_id(ctx)
    if not fhir or not patient_id:
        return create_text_response("Missing FHIR context or patient id.", is_error=True)

    client = FhirClient(base_url=fhir.url, token=fhir.token)
    patient = await client.read(f"Patient/{patient_id}")
    encounters = await client.search("Encounter", {"patient": patient_id, "_sort": "-date", "_count": "1"})
    conditions = await client.search("Condition", {"patient": patient_id, "clinical-status": "active", "_count": "20"})
    meds = await client.search("MedicationRequest", {"patient": patient_id, "status": "active", "_count": "20"})
    services = await client.search("ServiceRequest", {"patient": patient_id, "status": "active", "_count": "20"})

    summary = {
        "patient": {
            "id": patient_id,
            "name": (patient or {}).get("name"),
            "birth_date": (patient or {}).get("birthDate"),
            "gender": (patient or {}).get("gender"),
        },
        "encounter": _first_resource(encounters),
        "conditions": _resources(conditions),
        "medications": _resources(meds),
        "service_requests": _resources(services),
    }
    return create_text_response(json.dumps(summary, indent=2))


def _first_resource(bundle: dict | None) -> dict | None:
    entries = (bundle or {}).get("entry", [])
    if not entries:
        return None
    return entries[0].get("resource")


def _resources(bundle: dict | None) -> list[dict]:
    return [e.get("resource") for e in (bundle or {}).get("entry", []) if e.get("resource")]
