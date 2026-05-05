import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

PO_BASE = os.getenv("PO_PLATFORM_BASE_URL", "https://app.promptopinion.ai")

a2a_app = create_a2a_app(
    agent=root_agent,
    name="discharge_orchestrator",
    description=(
        "Composes a complete 30-day post-discharge care plan via real-time multi-agent "
        "negotiation across pharmacy, home health, and the patient. Writes a validated "
        "US Core CarePlan to FHIR. Hits 4 of Prompt Opinion's 5Ts in one workflow: "
        "Talk, Template, Transaction, Task."
    ),
    url=os.getenv("ORCHESTRATOR_URL", "http://localhost:8080"),
    port=8080,
    fhir_extension_uri=f"{PO_BASE}/schemas/a2a/v1/fhir-context",
    fhir_scopes=[
        {"name": "patient/Patient.rs", "required": False},
        {"name": "patient/Encounter.rs", "required": False},
        {"name": "patient/Condition.rs", "required": False},
        {"name": "patient/MedicationRequest.rs", "required": False},
        {"name": "patient/ServiceRequest.rs", "required": False},
        {"name": "patient/CarePlan.cuds", "required": False},
    ],
    require_api_key=True,
    skills=[
        AgentSkill(
            id="compose_discharge_plan",
            name="Compose 30-day discharge plan",
            description=(
                "Reads the patient's discharge summary from FHIR, opens parallel A2A "
                "negotiations with the specialty pharmacy and home health agents, reconciles "
                "blockers, and writes a validated US Core CarePlan back to FHIR."
            ),
            tags=["patient", "discharge", "care-plan", "transitions-of-care", "us-core", "davinci-pcde", "multi-agent"],
            examples=[
                "Compose the 30-day post-discharge plan for this patient.",
                "What does she need before going home? Negotiate with pharmacy and home health and build the plan.",
                "Build the discharge plan and write it to FHIR.",
            ],
        ),
    ],
)
