from mcp.server.fastmcp import FastMCP

from tools import (
    get_discharge_summary,
    identify_transition_needs,
    get_patient_constraints,
    validate_care_plan,
    write_care_plan,
)

mcp = FastMCP("CarePlan Composer", stateless_http=True, host="0.0.0.0")

_original_get_capabilities = mcp._mcp_server.get_capabilities


def _patched_get_capabilities(notification_options, experimental_capabilities):
    caps = _original_get_capabilities(notification_options, experimental_capabilities)
    caps.model_extra["extensions"] = {
        "ai.promptopinion/fhir-context": {
            "scopes": [
                {"name": "patient/Patient.rs", "required": True},
                {"name": "patient/Encounter.rs", "required": True},
                {"name": "patient/Condition.rs", "required": True},
                {"name": "patient/MedicationRequest.rs", "required": True},
                {"name": "patient/ServiceRequest.rs", "required": True},
                {"name": "patient/CarePlan.cuds", "required": True},
                {"name": "patient/Coverage.rs"},
            ]
        }
    }
    return caps


mcp._mcp_server.get_capabilities = _patched_get_capabilities

mcp.tool(name="GetDischargeSummary", description="Reads the patient's discharge summary (encounter, conditions, meds, service requests) from FHIR.")(get_discharge_summary)
mcp.tool(name="IdentifyTransitionNeeds", description="Converts a discharge summary JSON into a structured list of post-discharge needs (medications, home services, follow-ups, monitoring).")(identify_transition_needs)
mcp.tool(name="GetPatientConstraints", description="Returns patient constraints (language, zip, coverage) used to scope cross-org negotiation.")(get_patient_constraints)
mcp.tool(name="ValidateCarePlan", description="Validates a CarePlan against the US Core CarePlan profile and returns a structured issue list.")(validate_care_plan)
mcp.tool(name="WriteCarePlan", description="Writes a validated US Core CarePlan resource to the workspace's FHIR server. Returns the new resource id.")(write_care_plan)
