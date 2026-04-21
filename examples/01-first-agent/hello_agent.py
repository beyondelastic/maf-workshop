"""Lesson 01 — Your First Agent.

Create a simple health assistant agent using Microsoft Foundry and get both
non-streaming and streaming responses.

Reference:
  https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
  https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/01_hello_agent.py
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    # --- Create the client and agent ------------------------------------------
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="HealthBot",
        instructions=(
            "You are a friendly healthcare assistant. "
            "Give brief, helpful answers to general health questions. "
            "Always remind the user to consult a real doctor for medical advice."
        ),
    )

    # --- Non-streaming response -----------------------------------------------
    print("=== Non-streaming ===")
    result = await agent.run("What are common symptoms of seasonal allergies?")
    print(f"HealthBot: {result}\n")

    # --- Streaming response ---------------------------------------------------
    print("=== Streaming ===")
    print("HealthBot: ", end="", flush=True)
    async for chunk in agent.run(
        "What simple steps can I take to manage hay fever at home?",
        stream=True,
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
