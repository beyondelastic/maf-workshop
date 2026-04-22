"""Lesson 06 — Observability with OpenTelemetry.

Traces an agent run so you can see the LLM calls, tool invocations, and timing
in the console.

Reference:
  https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/observability
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework.observability import configure_otel_providers
from azure.identity import AzureCliCredential

load_dotenv()

# ---------------------------------------------------------------------------
# Set up OpenTelemetry tracing — sends traces to the AI Toolkit VS Code panel
# ---------------------------------------------------------------------------
configure_otel_providers(
    enable_console_exporters=False,
    enable_sensitive_data=True,
)


# ---------------------------------------------------------------------------
# A simple tool for the agent
# ---------------------------------------------------------------------------
@tool(name="lookup_symptom", description="Look up common causes for a symptom.")
def lookup_symptom(symptom: str) -> str:
    """Return simulated symptom causes."""
    data = {
        "headache": "Common causes: tension, migraine, dehydration, eyestrain.",
        "chest pain": "Common causes: anxiety, GERD, muscle strain, cardiac issues.",
        "fatigue": "Common causes: poor sleep, anaemia, thyroid issues, stress.",
    }
    return data.get(symptom.lower(), f"No data available for '{symptom}'.")


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
        name="TracedHealthBot",
        instructions=(
            "You are a health assistant. Use the lookup_symptom tool to find "
            "common causes for symptoms the user mentions."
        ),
        tools=[lookup_symptom],
    )

    print("Asking TracedHealthBot about fatigue...\n")
    result = await agent.run("I have been feeling very fatigued lately. What could be causing it?")
    print(f"\nAgent: {result}")
    print("\n(Open the AI Toolkit panel in VS Code to view the trace spans.)")


if __name__ == "__main__":
    asyncio.run(main())
