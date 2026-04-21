"""Lesson 03 — Tools & Function Calling.

Demonstrates how to define function tools that the agent can call during a
conversation. The healthcare scenario uses a drug-interaction checker and a
patient-vitals lookup.

Reference:
  https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools
  https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/02_add_tools.py
"""

import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


# ---------------------------------------------------------------------------
# Function tools
# ---------------------------------------------------------------------------

@tool(name="check_drug_interaction", description="Check for known interactions between two drugs.")
def check_drug_interaction(
    drug_a: Annotated[str, Field(description="First drug name")],
    drug_b: Annotated[str, Field(description="Second drug name")],
) -> str:
    """Return a simulated drug-interaction result."""
    interactions = {
        ("warfarin", "aspirin"): "High risk — increased bleeding risk when combined.",
        ("lisinopril", "potassium"): "Moderate risk — may cause hyperkalaemia.",
    }
    key = (drug_a.lower(), drug_b.lower())
    reverse_key = (drug_b.lower(), drug_a.lower())
    if key in interactions:
        return interactions[key]
    if reverse_key in interactions:
        return interactions[reverse_key]
    return f"No known interaction found between {drug_a} and {drug_b}."


@tool(name="get_patient_vitals", description="Look up the latest vitals for a patient by ID.")
def get_patient_vitals(
    patient_id: Annotated[str, Field(description="The patient identifier, e.g. P-1234")],
) -> str:
    """Return simulated patient vitals."""
    vitals = {
        "P-1001": "Heart rate: 72 bpm, Blood pressure: 120/80, Temperature: 36.6°C",
        "P-1002": "Heart rate: 95 bpm, Blood pressure: 145/92, Temperature: 37.1°C",
    }
    return vitals.get(patient_id, f"No vitals found for patient {patient_id}.")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="ClinicalAssistant",
        instructions=(
            "You are a clinical assistant. Use the available tools to answer "
            "questions about drug interactions and patient vitals. "
            "Always note that results are simulated."
        ),
        tools=[check_drug_interaction, get_patient_vitals],
    )

    # The agent should call check_drug_interaction
    print("User: Is it safe to take warfarin and aspirin together?\n")
    result1 = await agent.run("Is it safe to take warfarin and aspirin together?")
    print(f"Agent: {result1}\n")

    # The agent should call get_patient_vitals
    print("User: What are the latest vitals for patient P-1002?\n")
    result2 = await agent.run("What are the latest vitals for patient P-1002?")
    print(f"Agent: {result2}\n")


if __name__ == "__main__":
    asyncio.run(main())
