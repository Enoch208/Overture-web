"""
Smoke test for the ValidateAndWriteCarePlan MCP tool.

Exercises three paths offline (FHIR client is mocked):
  1. Bad JSON string                -> is_error, no write attempted.
  2. Plan that fails validation     -> is_error + issues list, no write.
  3. Valid plan + mocked FHIR write -> success, returns resource_id.

Run:
    python -m scripts.test_validate_and_write_care_plan

Exits non-zero on any failure so it's safe to wire into CI later.
"""

import asyncio
import importlib
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "mcp" / "careplan_composer"))

# tools/__init__.py re-exports the function under the same name as the
# submodule, which shadows the module in normal `from tools import ...` form.
# importlib.import_module returns the actual module object so we can patch it.
vawc_module = importlib.import_module("tools.validate_and_write_care_plan")

US_CORE_CAREPLAN_PROFILE = vawc_module.US_CORE_CAREPLAN_PROFILE
validate_and_write_care_plan = vawc_module.validate_and_write_care_plan


def _valid_plan() -> dict:
    return {
        "resourceType": "CarePlan",
        "meta": {"profile": [US_CORE_CAREPLAN_PROFILE]},
        "text": {"status": "generated", "div": "<div>postpartum 30-day plan</div>"},
        "status": "active",
        "intent": "plan",
        "category": [{"text": "Assess and plan"}],
        "subject": {"reference": "Patient/demo-postpartum"},
        "activity": [{"reference": {"reference": "MedicationRequest/abc"}}],
    }


def _payload(result) -> dict:
    return json.loads(result.content[0].text)


async def case_bad_json():
    result = await validate_and_write_care_plan(care_plan="not-json", ctx=None)
    assert result.isError, "bad JSON should be an error"
    assert "valid JSON" in result.content[0].text
    print("  ok: bad JSON rejected")


async def case_validation_fails():
    plan = _valid_plan()
    plan.pop("status")  # required field
    plan["activity"] = []  # also required

    with patch.object(vawc_module, "FhirClient") as fhir_cls:
        result = await validate_and_write_care_plan(
            care_plan=json.dumps(plan), ctx=MagicMock()
        )
        assert result.isError, "missing required fields should be an error"
        body = _payload(result)
        assert body["valid"] is False
        assert any("status" in i for i in body["issues"])
        assert any("activity" in i for i in body["issues"])
        fhir_cls.assert_not_called()  # no write on validation failure
    print("  ok: validation failure surfaces issues, no FHIR write attempted")


async def case_valid_and_writes():
    fake_client = MagicMock()
    fake_client.create = AsyncMock(return_value={
        "id": "cp-123",
        "resourceType": "CarePlan",
        "meta": {"versionId": "1", "lastUpdated": "2026-05-11T00:00:00Z"},
    })
    fake_ctx = MagicMock(url="https://fhir.example/fhir", token="t")

    with patch.object(vawc_module, "FhirClient", return_value=fake_client), \
         patch.object(vawc_module, "get_fhir_context", return_value=fake_ctx):
        result = await validate_and_write_care_plan(
            care_plan=json.dumps(_valid_plan()), ctx=MagicMock()
        )
        assert not result.isError, f"valid plan should succeed, got: {result.content[0].text}"
        body = _payload(result)
        assert body["valid"] is True
        assert body["resource_id"] == "cp-123"
        assert body["version_id"] == "1"
        fake_client.create.assert_awaited_once()
        args, _ = fake_client.create.call_args
        assert args[0] == "CarePlan"
    print("  ok: valid plan validates and writes, returns resource id")


async def main():
    print("ValidateAndWriteCarePlan smoke test")
    await case_bad_json()
    await case_validation_fails()
    await case_valid_and_writes()
    print("all cases passed")


if __name__ == "__main__":
    asyncio.run(main())
