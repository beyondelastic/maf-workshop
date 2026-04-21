# Microsoft Agent Framework Workshop

This repository is a beginner-friendly Microsoft Agent Framework workshop built
around official Microsoft Learn guidance and official samples.

The examples use lightweight healthcare and life-sciences scenarios so the
workshop stays consistent across agents, tools, workflows, orchestration, and
DevUI labs.

## What this workshop covers

1. Prepare your environment and verify Azure prerequisites.
2. Create a simple agent with Microsoft Foundry and get both non-streaming and streaming responses.
3. Build multi-turn conversations with sessions and add agent memory.
4. Define function tools and let the agent call them.
5. Build a deterministic two-agent workflow with executors and edges.
6. Orchestrate multiple specialist agents dynamically with Magentic.
7. Add OpenTelemetry observability to trace agent runs.
8. Launch the DevUI browser interface and interact with your agents visually.

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
- [Python samples](https://github.com/microsoft/agent-framework/tree/main/python/samples)

## Repository layout

```
.
├── docs/
├── examples/
├── mkdocs.yml
├── requirements.txt
└── SETUP.md
```

## Quick start

1. Create a Python virtual environment.
2. Install dependencies.
3. Sign in to Azure.
4. Copy `.env.example` to `.env` and fill in your project values.
5. Start the docs UI with `mkdocs serve`.

Detailed steps are in `SETUP.md`.

## Run the workshop UI

```bash
mkdocs serve
```

Then open the local URL shown in the terminal, usually `http://127.0.0.1:8000`.

## Run the examples

```bash
python examples/01-first-agent/hello_agent.py
python examples/02-conversations/multi_turn.py
python examples/02-conversations/memory_provider.py
python examples/03-tools/function_tools.py
python examples/04-workflow/sequential_workflow.py
python examples/05-orchestration/magentic_orchestration.py
python examples/06-observability/traced_agent.py
python examples/07-devui/run_devui.py
```

## SDK note

This workshop targets `agent-framework>=1.0.0`. If you run into SDK-shape
mismatches, first confirm your installed version with
`pip show agent-framework`.
