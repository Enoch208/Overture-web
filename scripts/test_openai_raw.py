"""
Sanity check that the OpenAI API key works.

This does NOT exercise the multi-agent system — it just sends the prompt to
gpt-4o directly. Useful for confirming the key is valid and the model is
reachable. If you want the real Discharge Orchestrator flow, use
test_orchestrator.py instead.

WARNING: this file has the API key hardcoded. Do NOT commit it to git.
Rotate the key when you're done testing.

Usage:
    python -m scripts.test_openai_raw
"""

from openai import OpenAI

OPENAI_API_KEY = "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"
MODEL = "gpt-5.4"

PROMPT = (
    "Consult the Discharge Orchestrator. Compose the 30-day post-discharge plan, "
    "but specifically confirm same-day medication delivery and a postpartum nurse "
    "visit within 24 hours. Surface any blockers."
)


def main() -> None:
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Discharge Orchestrator at a hospital. Compose a complete "
                    "30-day post-discharge care plan. Note: in this raw test you have no "
                    "tools — describe what you would do."
                ),
            },
            {"role": "user", "content": PROMPT},
        ],
    )

    print(f"model: {MODEL}")
    print(f"prompt: {PROMPT}\n")
    print("--- response ---")
    print(resp.choices[0].message.content)
    print(f"\n--- usage ---\n{resp.usage}")


if __name__ == "__main__":
    main()
