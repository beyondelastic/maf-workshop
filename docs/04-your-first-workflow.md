# 04 — Your First Workflow

Until now every example used a single agent. In this lesson you will build a
**workflow** — a graph of processing steps that passes data from one agent to
the next in a defined order.

## Agents vs Workflows

| | Agent | Workflow |
|---|-------|---------|
| **Steps** | Dynamic — the LLM decides what to do | Predefined — you define the execution path |
| **Control** | The model drives the loop | You control the flow explicitly |
| **Use case** | Open-ended conversation, tool use | Multi-step business processes, pipelines |

!!! tip
    If you can describe the process as a flowchart, a workflow is the right
    choice. If the task is open-ended and conversational, use an agent.

## Core concepts

### Executors

An **executor** is a single processing unit in a workflow. It can be:

- An **Agent** (LLM-powered)
- A plain Python **function** (deterministic logic)

### Edges

An **edge** connects two executors and determines the flow of messages. The
output of one executor becomes the input of the next.

```
[TriageAgent]  ──edge──▶  [RoutingAgent]
```

## The healthcare scenario

We will build a **patient triage pipeline**:

1. **TriageAgent** — classifies a patient complaint by severity (LOW / MEDIUM / HIGH).
2. **RoutingAgent** — reads the triage result and recommends a hospital department.

## The code

File: [`examples/04-workflow/sequential_workflow.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/04-workflow/sequential_workflow.py)

```python
import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.workflows import Workflow
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    # Agent 1: Triage
    triage_agent = Agent(
        client=client,
        name="TriageAgent",
        instructions=(
            "You are a hospital triage assistant. "
            "Given a patient complaint, classify its severity as LOW, MEDIUM, or HIGH "
            "and briefly explain your reasoning. "
            "Output format: 'Severity: <LEVEL>. Reason: <text>'"
        ),
    )

    # Agent 2: Routing
    routing_agent = Agent(
        client=client,
        name="RoutingAgent",
        instructions=(
            "You are a hospital department router. "
            "Given a triage assessment, recommend the most appropriate department "
            "(e.g. General Practice, Cardiology, Neurology, Emergency). "
            "Output format: 'Department: <name>. Recommendation: <text>'"
        ),
    )

    # Build the workflow
    workflow = Workflow()
    workflow.add_executor("triage", triage_agent)
    workflow.add_executor("routing", routing_agent)
    workflow.add_edge("triage", "routing")

    # Run
    patient_complaint = "I have had a persistent headache for two weeks and occasional dizziness."
    print(f"Patient complaint: {patient_complaint}\n")

    result = await workflow.run(patient_complaint)
    print(f"Workflow result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Step-by-step walkthrough

### 1. Create two agents

Each agent has a focused role and clear output format. Keeping instructions
narrow helps the LLM produce predictable results.

### 2. Build the workflow graph

```python
workflow = Workflow()
workflow.add_executor("triage", triage_agent)
workflow.add_executor("routing", routing_agent)
workflow.add_edge("triage", "routing")
```

- `add_executor(name, agent_or_function)` registers a node.
- `add_edge(source, target)` connects them. The output of `triage` becomes the
  input of `routing`.

### 3. Run the workflow

```python
result = await workflow.run(patient_complaint)
```

The framework executes `triage` first, passes its output to `routing`, and
returns the final result.

## What you can build from here

Workflows support much more than two sequential agents:

| Pattern | Description |
|---------|-------------|
| **Conditional edges** | Route to different executors based on a condition |
| **Fan-out / fan-in** | Run multiple executors in parallel and aggregate results |
| **Loops** | Repeat steps until a condition is met |
| **Human-in-the-loop** | Pause the workflow and wait for user input |
| **Checkpointing** | Save and resume long-running workflows |

These advanced patterns are covered in the
[official workflow samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows).

## Try it

```bash
python examples/04-workflow/sequential_workflow.py
```

You should see the triage assessment followed by a department recommendation.

## Key takeaways

- A **workflow** is a directed graph of executors connected by edges.
- **Executors** can be agents or plain functions.
- **Edges** define the data flow between executors.
- Workflows give you **explicit control** over multi-step processes.

## Official references

- [Workflows overview](https://learn.microsoft.com/en-us/agent-framework/workflows/)
- [Executors](https://learn.microsoft.com/en-us/agent-framework/workflows/executors)
- [Edges](https://learn.microsoft.com/en-us/agent-framework/workflows/edges)
- [Start-here samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/_start-here)
