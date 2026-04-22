"""Lesson 05 — Dynamic Orchestration with MagenticBuilder.

Demonstrates a Magentic-style orchestration where a manager agent dynamically
coordinates specialist agents (cardiologist, neurologist, general practitioner)
to handle a patient case.

Reference:
  https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/orchestrations/magentic.py
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import MagenticBuilder
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    # --- Specialist agents ----------------------------------------------------
    cardiologist = Agent(
        client=client,
        name="Cardiologist",
        instructions=(
            "You are a cardiologist. Provide analysis only for heart-related "
            "symptoms. If the case is not cardiac, say so briefly."
        ),
    )

    neurologist = Agent(
        client=client,
        name="Neurologist",
        instructions=(
            "You are a neurologist. Provide analysis only for neurological "
            "symptoms. If the case is not neurological, say so briefly."
        ),
    )

    general_practitioner = Agent(
        client=client,
        name="GeneralPractitioner",
        instructions=(
            "You are a general practitioner. Provide a holistic assessment "
            "and summarise recommendations from the specialists."
        ),
    )

    # --- Manager agent --------------------------------------------------------
    manager = Agent(
        client=client,
        name="Manager",
        instructions=(
            "You coordinate a team of medical specialists. "
            "Delegate tasks to the right specialist based on the patient's symptoms "
            "and synthesise their responses into a final assessment."
        ),
    )

    # --- Build the Magentic orchestration ------------------------------------
    workflow = MagenticBuilder(
        participants=[cardiologist, neurologist, general_practitioner],
        manager_agent=manager,
        intermediate_outputs=True,
    ).build()

    # --- Run with streaming ---------------------------------------------------
    patient_case = (
        "A 55-year-old patient reports chest tightness, occasional headaches, "
        "and numbness in the left arm that started two weeks ago."
    )
    print(f"Patient case: {patient_case}\n")
    print("--- Orchestration output ---\n")

    current_agent = None
    async for event in workflow.run(patient_case, stream=True):
        if event.type == "output" and hasattr(event.data, "text") and event.data.text:
            name = getattr(event.data, "author_name", None)
            if name and name != current_agent:
                current_agent = name
                print(f"\n\n[{current_agent}]\n")
            print(event.data.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
