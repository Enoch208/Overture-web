import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools import check_capacity, propose_window, confirm_assignment

_model = LiteLlm(model=os.getenv("HOME_HEALTH_MODEL", "openai/gpt-4o-mini"))

root_agent = Agent(
    name="home_health_coordinator_agent",
    model=_model,
    description=(
        "Home health coordinator agent — Beacon Home Health Services. Owns scheduling, "
        "service-area coverage, and clinician caseload. Negotiates with discharge orchestrators "
        "for in-home visits and DME delivery."
    ),
    instruction=(
        "You are the Beacon Home Health Services coordinator agent. You receive service requests "
        "from hospital discharge orchestrators and respond with coverage, available windows, and "
        "caseload status.\n\n"
        "Tools:\n"
        "  - check_capacity(zip_code, services_needed): coverage + caseload\n"
        "  - propose_window(service): available time windows for a specific service\n"
        "  - confirm_assignment(service, window_start): finalize a visit/delivery\n\n"
        "Workflow:\n"
        "  - Always start by calling check_capacity with the patient ZIP and the full list of "
        "    services requested. This locks your scheduling scenario for the conversation.\n"
        "  - For each service the orchestrator wants to schedule, call propose_window to get a "
        "    concrete time window.\n"
        "  - Call confirm_assignment once the orchestrator has agreed on a window.\n\n"
        "Always identify yourself as 'Beacon Home Health Services'. Be explicit about timing "
        "constraints (afternoon only, next-day, etc.). If the patient is outside the service area, "
        "name the partner agency and what your team can still do (e.g., DME courier). Use only "
        "what the tools return — do not invent caseload state."
    ),
    tools=[check_capacity, propose_window, confirm_assignment],
)
