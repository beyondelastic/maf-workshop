"""DevUI agent module — HealthBot with a symptom lookup tool.

DevUI discovers agents from directories. Each agent directory must have an
__init__.py that exports an ``agent`` variable.

Reference:
  https://github.com/microsoft/agent-framework/tree/main/python/packages/devui
"""

import os

from dotenv import load_dotenv

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


@tool(name="lookup_symptom", description="Look up common causes for a symptom.")
def lookup_symptom(symptom: str) -> str:
    """Return simulated symptom causes."""
    data = {
        "headache": "Common causes: tension, migraine, dehydration, eyestrain.",
        "chest pain": "Common causes: anxiety, GERD, muscle strain, cardiac issues.",
        "fatigue": "Common causes: poor sleep, anaemia, thyroid issues, stress.",
        "fever": "Common causes: infection, inflammation, heat exhaustion.",
    }
    return data.get(symptom.lower(), f"No data available for '{symptom}'.")


client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
    credential=AzureCliCredential(),
)

# The variable MUST be named ``agent`` for DevUI directory-based discovery.
agent = Agent(
    client=client,
    name="HealthBot",
    instructions=(
        "You are a friendly healthcare assistant. "
        "Use the lookup_symptom tool when the user asks about symptoms. "
        "Always remind the user to consult a real doctor."
    ),
    tools=[lookup_symptom],
)
