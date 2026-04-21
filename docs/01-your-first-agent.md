# 01 — Your First Agent

In this lesson you will create your first agent using Microsoft Agent Framework,
send it a question, and receive both a **non-streaming** and a **streaming**
response.

## What is an Agent?

An **Agent** in the Microsoft Agent Framework is an object that wraps a large
language model (LLM) together with a name, instructions, and optional tools. You
talk to the agent by calling `agent.run()` with a user message and the agent
returns a model-generated response.

```
User message  ──▶  Agent  ──▶  LLM  ──▶  Response
```

## Providers

The agent needs a **client** that connects it to a model. Agent Framework calls
these clients *providers*. This workshop uses **FoundryChatClient** (backed by
Microsoft Foundry), but the framework supports many others:

| Provider | Client class |
|----------|-------------|
| **Microsoft Foundry** | `FoundryChatClient` |
| Azure OpenAI | `AzureOpenAIChatCompletionClient` |
| OpenAI | `OpenAIChatClient` / `OpenAIChatCompletionClient` |
| Anthropic | `AnthropicChatClient` |
| Ollama | `OllamaChatClient` |
| Amazon Bedrock | `BedrockChatClient` |

All providers share the same `Agent` interface, so you can swap one for another
by changing only the client.

## The code

Create the file [`examples/01-first-agent/hello_agent.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/01-first-agent/hello_agent.py):

```python
import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    # Create the client and agent
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

    # Non-streaming response
    print("=== Non-streaming ===")
    result = await agent.run("What are common symptoms of seasonal allergies?")
    print(f"HealthBot: {result}\n")

    # Streaming response
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
```

## Step-by-step walkthrough

### 1. Load environment variables

```python
from dotenv import load_dotenv
load_dotenv()
```

Agent Framework does **not** load `.env` files automatically. Call
`load_dotenv()` at the start of your script.

### 2. Create the client

```python
client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
    credential=AzureCliCredential(),
)
```

`FoundryChatClient` connects to a model deployed in your Microsoft Foundry
project. Authentication is handled by `AzureCliCredential`, which reuses your
`az login` session.

### 3. Create the agent

```python
agent = Agent(
    client=client,
    name="HealthBot",
    instructions="You are a friendly healthcare assistant. ...",
)
```

- **name** — a human-readable label for logging and debugging.
- **instructions** — the system prompt that shapes the agent's personality and
  behaviour.

### 4. Non-streaming response

```python
result = await agent.run("What are common symptoms of seasonal allergies?")
print(f"HealthBot: {result}")
```

`agent.run()` sends the message to the LLM and returns the complete response
once generation finishes.

### 5. Streaming response

```python
async for chunk in agent.run("What simple steps can I take to manage hay fever at home?", stream=True):
    if chunk.text:
        print(chunk.text, end="", flush=True)
```

With `stream=True`, `agent.run()` returns an async iterator. Each chunk arrives
as soon as the model produces it, giving a more responsive user experience.

## Try it

```bash
python examples/01-first-agent/hello_agent.py
```

You should see two answers from **HealthBot**: one printed all at once
(non-streaming) and one printed token by token (streaming).

## Key takeaways

- An **Agent** wraps an LLM with a name, instructions, and optional tools.
- A **provider client** (like `FoundryChatClient`) connects the agent to a model.
- You can swap providers without changing the agent logic.
- `agent.run()` supports both non-streaming and streaming modes.

## Official references

- [Your First Agent tutorial](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent)
- [Agents overview](https://learn.microsoft.com/en-us/agent-framework/agents/)
- [Providers](https://learn.microsoft.com/en-us/agent-framework/agents/providers/)
- [Full sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/01_hello_agent.py)
