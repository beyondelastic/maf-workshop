"""Lesson 02b — Agent memory with InMemoryHistoryProvider.

Shows how to add a persistent conversation history provider so the agent
remembers previous interactions automatically.

Reference:
  https://learn.microsoft.com/en-us/agent-framework/agents/conversations/context-providers
  https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/04_memory.py
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, InMemoryHistoryProvider
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    # Add InMemoryHistoryProvider so the agent automatically stores and
    # reloads conversation history for every session turn.
    agent = Agent(
        client=client,
        name="MemoryBot",
        instructions=(
            "You are a patient-intake assistant. "
            "Remember everything the patient tells you. "
            "When asked, recall earlier details accurately."
        ),
        context_providers=[
            InMemoryHistoryProvider("memory", load_messages=True),
        ],
    )

    session = agent.create_session()

    # The patient shares information across several turns
    print("User: My name is Alice and I am 34 years old.")
    r1 = await agent.run("My name is Alice and I am 34 years old.", session=session)
    print(f"Agent: {r1}\n")

    print("User: I am allergic to penicillin.")
    r2 = await agent.run("I am allergic to penicillin.", session=session)
    print(f"Agent: {r2}\n")

    # Ask the agent to recall — InMemoryHistoryProvider reloads the full history
    print("User: What do you know about me so far?")
    r3 = await agent.run("What do you know about me so far?", session=session)
    print(f"Agent: {r3}\n")


if __name__ == "__main__":
    asyncio.run(main())
