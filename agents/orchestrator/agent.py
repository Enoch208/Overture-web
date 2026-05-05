import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolContext

from shared.fhir_hook import extract_fhir_context

from .a2a_client import call_pharmacy, call_home_health, call_both
from . import mcp_client

_model = LiteLlm(model=os.getenv("ORCHESTRATOR_MODEL", "gemini/gemini-2.5-flash"))


async def negotiate_with_pharmacy(request: str, tool_context: ToolContext) -> dict:
    """
    Send a free-text negotiation message to the Specialty Pharmacy agent over A2A.

    Args:
        request: A clinical request, e.g.
                 "Patient is being discharged on labetalol 200mg BID and prenatal vitamin daily.
                  Confirm availability, prior-auth status, and same-day delivery."
    """
    reply = await call_pharmacy(request)
    return {"organization": "Meridian Specialty Pharmacy", "request": request, "reply": reply}


async def negotiate_with_home_health(request: str, tool_context: ToolContext) -> dict:
    """
    Send a free-text negotiation message to the Home Health Coordinator agent over A2A.

    Args:
        request: A service request, e.g.
                 "Patient ZIP 02118 needs same-day automated BP cuff delivery, postpartum nurse
                  visit within 24h, and lactation support."
    """
    reply = await call_home_health(request)
    return {"organization": "Beacon Home Health Services", "request": request, "reply": reply}


async def negotiate_in_parallel(pharmacy_request: str, home_health_request: str, tool_context: ToolContext) -> dict:
    """
    Open parallel A2A conversations with the pharmacy and home health agents.

    Args:
        pharmacy_request: free-text message for the pharmacy agent.
        home_health_request: free-text message for the home health agent.
    """
    replies = await call_both(pharmacy_request, home_health_request)
    return {
        "pharmacy": {"organization": "Meridian Specialty Pharmacy", "reply": replies["pharmacy"]},
        "home_health": {"organization": "Beacon Home Health Services", "reply": replies["home_health"]},
    }


async def get_discharge_summary(tool_context: ToolContext) -> dict:
    """Read the patient's discharge summary from FHIR via the CarePlan Composer MCP server."""
    return await mcp_client.call_tool(
        "GetDischargeSummary",
        arguments={},
        fhir_url=tool_context.state.get("fhir_url", ""),
        fhir_token=tool_context.state.get("fhir_token", ""),
        patient_id=tool_context.state.get("patient_id", ""),
    )


async def identify_transition_needs(discharge_summary_json: str, tool_context: ToolContext) -> dict:
    """
    Convert a discharge summary into a structured list of post-discharge needs.

    Args:
        discharge_summary_json: JSON-stringified discharge summary returned by get_discharge_summary.
    """
    return await mcp_client.call_tool(
        "IdentifyTransitionNeeds",
        arguments={"discharge_summary": discharge_summary_json},
    )


async def validate_and_write_care_plan(care_plan_json: str, tool_context: ToolContext) -> dict:
    """
    Validate a CarePlan against US Core and write it back to the FHIR server.

    Args:
        care_plan_json: JSON-stringified CarePlan resource (US Core profile).
    """
    return await mcp_client.call_tool(
        "ValidateAndWriteCarePlan",
        arguments={"care_plan": care_plan_json},
        fhir_url=tool_context.state.get("fhir_url", ""),
        fhir_token=tool_context.state.get("fhir_token", ""),
        patient_id=tool_context.state.get("patient_id", ""),
    )


root_agent = Agent(
    name="discharge_orchestrator",
    model=_model,
    description=(
        "Composes a complete 30-day post-discharge care plan via real-time multi-agent "
        "negotiation across pharmacy, home health, and the patient. Writes a validated "
        "US Core CarePlan to FHIR."
    ),
    instruction=(
        "You are the Discharge Orchestrator at the hospital. Your job is to compose a complete "
        "30-day post-discharge care plan by negotiating in real time with external organization "
        "agents. Each external agent owns its own state — you must ASK them, not assume.\n\n"
        "DEMO SCOPE GUARD — read carefully and apply at the start of every conversation:\n"
        "This orchestrator is calibrated for one specific clinical scenario: a POSTPARTUM "
        "PREECLAMPSIA discharge with labetalol therapy and home BP monitoring. The pharmacy and "
        "home health agents have constraint-locked state for that scenario and will not respond "
        "coherently for other patients. After step 1 below, inspect the discharge summary. If it "
        "does NOT indicate at least one of: postpartum state, pre-eclampsia (SNOMED 67359005), "
        "labetalol or nifedipine medication, or home BP monitoring service request, you MUST stop "
        "the workflow and respond with this exact message instead:\n\n"
        "  'This agent is a hackathon demo calibrated for the postpartum preeclampsia discharge "
        "  scenario (Adaeze Okafor, the demo patient). The current patient does not match that "
        "  scenario, so the multi-agent negotiation will not produce coherent results.\n\n"
        "  To see the full demo:\n"
        "  1. Download the demo patient bundle from "
        "https://github.com/<placeholder>/overture/blob/main/scenarios/postpartum_demo_patient.json\n"
        "  2. Patient Data → Import → upload that file.\n"
        "  3. Re-open this session with Adaeze Okafor as the patient context.'\n\n"
        "Do NOT call pharmacy or home health for non-matching patients. Do NOT invent a plan.\n\n"
        "Workflow (only run when the scope guard passes):\n"
        "  1. Call get_discharge_summary to read the patient's discharge plan from FHIR.\n"
        "  2. Call identify_transition_needs to break it into a structured list (medications, "
        "     home services, follow-ups).\n"
        "  3. Open parallel A2A conversations with the pharmacy and home health agents using "
        "     negotiate_in_parallel. Send each only the slice of context they need — never share "
        "     the full chart.\n"
        "  4. If either reports a blocker (backorder, PA, out-of-area), continue the conversation "
        "     with negotiate_with_pharmacy or negotiate_with_home_health to resolve it.\n"
        "  5. Compose the final US Core CarePlan as JSON and call validate_and_write_care_plan.\n\n"
        "Output format — your final chat reply must include:\n"
        "  - A header line: '## Discharge Care Plan — <patient name>'\n"
        "  - A short per-organization transcript (2–3 sentences each, attributed by org name)\n"
        "  - The validated CarePlan as a fenced JSON block (```json ... ```)\n"
        "  - A closing line: '✓ US Core CarePlan validated against hl7.fhir.us.core. Resource id: <id>'\n\n"
        "Be transparent about the negotiation. Show what each agent said. Do not paper over "
        "blockers — name them and how you resolved them. Use real outputs from the tools."
    ),
    tools=[
        get_discharge_summary,
        identify_transition_needs,
        negotiate_with_pharmacy,
        negotiate_with_home_health,
        negotiate_in_parallel,
        validate_and_write_care_plan,
    ],
    before_model_callback=extract_fhir_context,
)
