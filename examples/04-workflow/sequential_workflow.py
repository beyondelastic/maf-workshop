"""Lesson 04 — Your First Workflow.

A deterministic two-agent pipeline using executors and edges:
  Agent 1 (TriageAgent)    → classifies a patient complaint by severity
  Agent 2 (RoutingAgent)   → recommends the appropriate hospital department

Reference:
  https://learn.microsoft.com/en-us/agent-framework/workflows/
  https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/_start-here/step2_agents_in_a_workflow.py
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.workflows import Workflow
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    # --- Agent 1: Triage ------------------------------------------------------
    triage_agent = Agent(
        client=client,
        name="TriageAgent",
        instructions=(
            "You are a hospital triage assistant. "
            "Given a patient complaint, classify its severity as LOW, MEDIUM, or HIGH "
            "and briefly explain your reasoning. "
            "Output format: 'Severity: <LEVEL>. Reason: <text>'"
        ),
    )

    # --- Agent 2: Routing -----------------------------------------------------
    routing_agent = Agent(
        client=client,
        name="RoutingAgent",
        instructions=(
            "You are a hospital department router. "
            "Given a triage assessment, recommend the most appropriate department "
            "(e.g. General Practice, Cardiology, Neurology, Emergency). "
            "Output format: 'Department: <name>. Recommendation: <text>'"
        ),
    )

    # --- Build the workflow ---------------------------------------------------
    workflow = Workflow()

    # Add agents as executors
    workflow.add_executor("triage", triage_agent)
    workflow.add_executor("routing", routing_agent)

    # Connect them: triage output feeds into routing input
    workflow.add_edge("triage", "routing")

    # --- Run the workflow -----------------------------------------------------
    patient_complaint = "I have had a persistent headache for two weeks and occasional dizziness."
    print(f"Patient complaint: {patient_complaint}\n")

    result = await workflow.run(patient_complaint)

    print(f"Workflow result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
