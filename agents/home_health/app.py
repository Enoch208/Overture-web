import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="home_health_coordinator_agent",
    description=(
        "Beacon Home Health Services — schedules in-home visits and DME delivery for "
        "post-discharge patients. Reports service-area coverage, caseload status, "
        "and available windows."
    ),
    url=os.getenv("HOME_HEALTH_URL", "http://localhost:8083"),
    port=8083,
    require_api_key=True,
    skills=[
        AgentSkill(
            id="check_capacity",
            name="Check service-area capacity",
            description="Reports whether a ZIP is in the service area and what services + caseload are available.",
            tags=["home-health", "capacity", "service-area", "post-discharge"],
            examples=[
                "Can you cover ZIP 02118 for BP monitoring, a postpartum visit, and lactation support?",
            ],
        ),
        AgentSkill(
            id="propose_window",
            name="Propose visit/delivery window",
            description="Returns the available time windows for a specific service.",
            tags=["home-health", "scheduling"],
            examples=[
                "What delivery window do you have for an automated BP cuff?",
                "Earliest postpartum nurse visit?",
            ],
        ),
        AgentSkill(
            id="confirm_assignment",
            name="Confirm assignment",
            description="Finalizes a visit or delivery on the agency caseload.",
            tags=["home-health", "scheduling"],
            examples=[
                "Confirm BP cuff delivery for 2026-05-05T16:00:00Z.",
            ],
        ),
    ],
)
