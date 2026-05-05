import json
from typing import Annotated

from mcp.server.fastmcp import Context
from pydantic import Field

from fhir_client import FhirClient
from fhir_utilities import get_fhir_context
from mcp_utilities import create_text_response


async def write_care_plan(
    care_plan: Annotated[str, Field(description="Validated US Core CarePlan resource as JSON.")],
    ctx: Context = None,
):
    fhir = get_fhir_context(ctx)
    if not fhir:
        return create_text_response("Missing FHIR context.", is_error=True)

    try:
        plan = json.loads(care_plan)
    except json.JSONDecodeError:
        return create_text_response("care_plan must be valid JSON.", is_error=True)

    client = FhirClient(base_url=fhir.url, token=fhir.token)
    created = await client.create("CarePlan", plan)
    return create_text_response(json.dumps({
        "resource_id": created.get("id"),
        "resource_type": created.get("resourceType"),
        "version_id": (created.get("meta") or {}).get("versionId"),
        "last_updated": (created.get("meta") or {}).get("lastUpdated"),
    }, indent=2))
