import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="specialty_pharmacy_agent",
    description=(
        "Meridian Specialty Pharmacy — fulfills post-discharge prescriptions. "
        "Reports inventory, prior-auth status, and delivery windows. Proposes "
        "clinically appropriate substitutes when first-line therapy is blocked."
    ),
    url=os.getenv("PHARMACY_URL", "http://localhost:8082"),
    port=8082,
    require_api_key=True,
    skills=[
        AgentSkill(
            id="check_availability",
            name="Check medication availability",
            description="Reports inventory, prior-auth status, and copay for a list of prescribed medications.",
            tags=["pharmacy", "inventory", "benefits", "post-discharge"],
            examples=[
                "Are labetalol 200mg and nifedipine ER 30mg available for this patient?",
                "Check stock and PA status for the postpartum hypertension regimen.",
            ],
        ),
        AgentSkill(
            id="propose_substitution",
            name="Propose substitution",
            description="Proposes clinically appropriate substitutes when first-line therapy is on backorder or PA-blocked.",
            tags=["pharmacy", "substitution", "post-discharge"],
            examples=[
                "Labetalol is on backorder — propose a substitute for postpartum hypertension.",
            ],
        ),
        AgentSkill(
            id="confirm_dispense",
            name="Confirm dispense",
            description="Finalizes a dispense and returns a dispense id and delivery window.",
            tags=["pharmacy", "dispense", "post-discharge"],
            examples=[
                "Dispense nifedipine ER 30mg, 1 tab PO BID for this patient.",
            ],
        ),
    ],
)
