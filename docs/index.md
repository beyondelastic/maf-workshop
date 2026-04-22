# Microsoft Agent Framework Workshop

Welcome to this beginner-friendly Microsoft Agent Framework workshop. Every
exercise is based on official Microsoft Learn documentation and the
[microsoft/agent-framework](https://github.com/microsoft/agent-framework)
repository so you can trust the patterns you learn here.

The examples use lightweight **healthcare and life-sciences** scenarios to keep a
consistent thread across all lessons.

## What this workshop covers

| # | Lesson | What you will learn |
|---|--------|---------------------|
| 00 | [Prerequisites](00-prereqs.md) | Azure subscription, Python environment, Foundry project and model deployment |
| 01 | [Your First Agent](01-your-first-agent.md) | Create an agent with `FoundryChatClient`, get non-streaming and streaming responses |
| 02 | [Conversations & Memory](02-conversations-and-memory.md) | Multi-turn conversations with `AgentSession`, persistent memory with `InMemoryHistoryProvider` |
| 03 | [Tools & Function Calling](03-tools-and-function-calling.md) | Define function tools with `@tool`, let the agent call custom code |
| 04 | [Your First Workflow](04-your-first-workflow.md) | Build a deterministic two-agent pipeline with executors and edges |
| 05 | [Dynamic Orchestration](05-dynamic-orchestration.md) | Coordinate specialist agents dynamically with `MagenticBuilder` |
| 06 | [Observability](06-observability.md) | Trace agent runs with OpenTelemetry |
| 07 | [DevUI](07-devui.md) | Launch the browser-based developer UI and interact with your agents visually |

## Design goals

- Keep the flow easy to follow.
- Favour official documentation over custom theory.
- Keep examples short and runnable.
- Use a lightweight docs-first web UI.

## Official sources used

- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Your First Agent tutorial](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent)
- [Sessions & Conversations](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/session)
- [Context Providers](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/context-providers)
- [Function Tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools)
- [Workflows overview](https://learn.microsoft.com/en-us/agent-framework/workflows/)
- [microsoft/agent-framework GitHub repository](https://github.com/microsoft/agent-framework)

## Repository layout

```
.
├── docs/           ← lesson pages (served by MkDocs)
├── examples/       ← runnable Python scripts
├── mkdocs.yml
├── requirements.txt
└── SETUP.md
```

## Quick start

1. Clone the repository and set up the Python environment:

    ```bash
    git clone https://github.com/beyondelastic/maf-workshop.git
    cd maf-workshop
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Sign in to Azure:

    ```bash
    az login
    ```

3. Configure your environment variables:

    ```bash
    cp .env.example .env   # fill in your values
    ```

4. Follow the lessons on this site starting with [Prerequisites](00-prereqs.md).

Full setup instructions are in [SETUP.md](https://github.com/beyondelastic/maf-workshop/blob/main/SETUP.md).
