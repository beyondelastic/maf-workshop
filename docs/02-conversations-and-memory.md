# 02 — Conversations & Memory

In the previous lesson each call to `agent.run()` was independent — the agent
had no memory of earlier turns. In this lesson you will learn how to:

1. Use **AgentSession** for multi-turn conversations.
2. Add **InMemoryHistoryProvider** so the agent remembers automatically.

## Why sessions matter

Without a session, every call to `agent.run()` starts from scratch. The agent
does not know what the user said before. A session carries the conversation
state so the agent can build on earlier context.

## AgentSession at a glance

| Property | Purpose |
|----------|---------|
| `session_id` | Local unique identifier for this session |
| `service_session_id` | Remote service conversation ID (when service-managed history is used) |
| `state` | Mutable dictionary shared with context and history providers |

## Example 1 — Multi-turn with AgentSession

File: [`examples/02-conversations/multi_turn.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/02-conversations/multi_turn.py)

```python
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
    result1 = await agent.run(
        "I have been sneezing a lot and my eyes are itchy.",
        session=session,
    )
    print(f"Agent: {result1}\n")

    # Turn 2 — the agent remembers turn 1
    result2 = await agent.run(
        "It started about three days ago.",
        session=session,
    )
    print(f"Agent: {result2}\n")

    # Turn 3 — ask for a summary
    result3 = await agent.run(
        "Can you summarise what you know about my symptoms so far?",
        session=session,
    )
    print(f"Agent: {result3}\n")
```

### What is happening

1. `agent.create_session()` creates a new `AgentSession`.
2. Passing the same `session` to each `agent.run()` call keeps the conversation
   context.
3. By turn 3 the agent can summarise information from turns 1 and 2.

## Example 2 — Memory with InMemoryHistoryProvider

`AgentSession` carries context within a single script run. To make the agent
store and reload conversation messages **automatically**, add a history
provider.

File: [`examples/02-conversations/memory_provider.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/02-conversations/memory_provider.py)

```python
from agent_framework import Agent, InMemoryHistoryProvider
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="MemoryBot",
    instructions="You are a patient-intake assistant. Remember everything the patient tells you.",
    context_providers=[
        InMemoryHistoryProvider("memory", load_messages=True),
    ],
)

session = agent.create_session()

await agent.run("My name is Alice and I am 34 years old.", session=session)
await agent.run("I am allergic to penicillin.", session=session)
result = await agent.run("What do you know about me so far?", session=session)
print(result)
```

### What is `InMemoryHistoryProvider`?

- It is the built-in history provider that stores conversation messages in
  memory.
- `load_messages=True` tells it to reload the full history before each LLM
  call, so the model always sees everything.
- For production you could replace it with a database-backed history provider
  (e.g., Cosmos DB) — the interface is the same.

## Context providers — the bigger picture

History providers are a specific kind of **context provider**. Context providers
run **before** and **after** each agent invocation:

```
before_run()  →  LLM call  →  after_run()
```

They can:

- Inject extra instructions or messages (`context.extend_instructions()`).
- Read or write to `session.state`.
- Store and reload message history.

You can write **custom context providers** by inheriting from `ContextProvider`:

```python
from agent_framework import AgentSession, ContextProvider, SessionContext

class UserPreferenceProvider(ContextProvider):
    def __init__(self) -> None:
        super().__init__("user-preferences")

    async def before_run(self, *, agent, session, context, state):
        if favourite := state.get("favourite_food"):
            context.extend_instructions(
                self.source_id,
                f"User's favourite food is {favourite}.",
            )
```

In this workshop we use `InMemoryHistoryProvider`, which stores history in
memory for the duration of the script. In a real application you would swap it
for a persistent provider (e.g. backed by a database) so the agent remembers
conversations across sessions. Custom context providers like the example above
let you inject any extra information — but that is beyond the scope of this
workshop.

## Try it

```bash
python examples/02-conversations/multi_turn.py
python examples/02-conversations/memory_provider.py
```

## Key takeaways

- **AgentSession** maintains conversation state across `agent.run()` calls.
- **InMemoryHistoryProvider** automatically stores and reloads message history.
- **Context providers** are the extensibility point for injecting context,
  history, and instructions around each LLM call.

## Official references

- [AgentSession](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/session)
- [Context Providers](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/context-providers)
- [Multi-turn sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/03_multi_turn.py)
- [Memory sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/04_memory.py)
