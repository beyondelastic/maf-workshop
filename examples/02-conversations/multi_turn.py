"""Lesson 02a — Multi-turn conversations with AgentSession.

Demonstrates how to use AgentSession to maintain context across multiple
turns of a symptom-checker conversation.

Reference:
  https://learn.microsoft.com/en-us/agent-framework/agents/conversations/session
  https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/03_multi_turn.py
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="SymptomChecker",
        instructions=(
            "You are a helpful symptom-checker assistant. "
            "Ask clarifying questions about the patient's symptoms. "
            "Remember what the patient has already told you. "
            "Always remind the user to see a real doctor."
        ),
    )

    # Create a session to maintain conversation state across turns
    session = agent.create_session()

    # Turn 1
    print("User: I have been sneezing a lot and my eyes are itchy.")
    result1 = await agent.run(
        "I have been sneezing a lot and my eyes are itchy.",
        session=session,
    )
    print(f"Agent: {result1}\n")

    # Turn 2 — the agent should remember the symptoms from turn 1
    print("User: It started about three days ago.")
    result2 = await agent.run(
        "It started about three days ago.",
        session=session,
    )
    print(f"Agent: {result2}\n")

    # Turn 3 — ask the agent to summarise what it knows
    print("User: Can you summarise what you know about my symptoms so far?")
    result3 = await agent.run(
        "Can you summarise what you know about my symptoms so far?",
        session=session,
    )
    print(f"Agent: {result3}\n")


if __name__ == "__main__":
    asyncio.run(main())
