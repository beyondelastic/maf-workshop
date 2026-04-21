# 03 — Tools & Function Calling

So far the agent can only generate text. In this lesson you will give it
**tools** — Python functions that the agent can call during a conversation to
look up information or perform actions.

## How tool calling works

```
User message  ──▶  Agent  ──▶  LLM decides to call a tool
                                       │
                                       ▼
                               Tool executes (your code)
                                       │
                                       ▼
                               LLM uses tool result to answer
```

1. The user sends a message.
2. The LLM decides it needs external information and emits a **tool call**.
3. Agent Framework executes the matching Python function.
4. The tool result is sent back to the LLM.
5. The LLM generates the final answer.

## Defining a function tool

Any Python function can be a tool. Use type annotations and Pydantic `Field` to
describe the parameters so the LLM knows how to call it:

```python
from typing import Annotated
from pydantic import Field
from agent_framework import tool

@tool(name="check_drug_interaction", description="Check for known interactions between two drugs.")
def check_drug_interaction(
    drug_a: Annotated[str, Field(description="First drug name")],
    drug_b: Annotated[str, Field(description="Second drug name")],
) -> str:
    """Return a simulated drug-interaction result."""
    interactions = {
        ("warfarin", "aspirin"): "High risk — increased bleeding risk when combined.",
        ("lisinopril", "potassium"): "Moderate risk — may cause hyperkalaemia.",
    }
    key = (drug_a.lower(), drug_b.lower())
    reverse_key = (drug_b.lower(), drug_a.lower())
    if key in interactions:
        return interactions[key]
    if reverse_key in interactions:
        return interactions[reverse_key]
    return f"No known interaction found between {drug_a} and {drug_b}."
```

!!! tip
    If you omit `name` and `description` in `@tool`, the framework uses the
    function name and docstring as defaults.

## Providing tools to the agent

Pass your tools to the `tools` parameter when creating the agent:

```python
agent = Agent(
    client=client,
    name="ClinicalAssistant",
    instructions="You are a clinical assistant. Use the available tools to answer questions.",
    tools=[check_drug_interaction, get_patient_vitals],
)
```

## Full example

File: `examples/03-tools/function_tools.py`

```python
import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()


@tool(name="check_drug_interaction", description="Check for known interactions between two drugs.")
def check_drug_interaction(
    drug_a: Annotated[str, Field(description="First drug name")],
    drug_b: Annotated[str, Field(description="Second drug name")],
) -> str:
    """Return a simulated drug-interaction result."""
    interactions = {
        ("warfarin", "aspirin"): "High risk — increased bleeding risk when combined.",
        ("lisinopril", "potassium"): "Moderate risk — may cause hyperkalaemia.",
    }
    key = (drug_a.lower(), drug_b.lower())
    reverse_key = (drug_b.lower(), drug_a.lower())
    if key in interactions:
        return interactions[key]
    if reverse_key in interactions:
        return interactions[reverse_key]
    return f"No known interaction found between {drug_a} and {drug_b}."


@tool(name="get_patient_vitals", description="Look up the latest vitals for a patient by ID.")
def get_patient_vitals(
    patient_id: Annotated[str, Field(description="The patient identifier, e.g. P-1234")],
) -> str:
    """Return simulated patient vitals."""
    vitals = {
        "P-1001": "Heart rate: 72 bpm, Blood pressure: 120/80, Temperature: 36.6°C",
        "P-1002": "Heart rate: 95 bpm, Blood pressure: 145/92, Temperature: 37.1°C",
    }
    return vitals.get(patient_id, f"No vitals found for patient {patient_id}.")


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="ClinicalAssistant",
        instructions=(
            "You are a clinical assistant. Use the available tools to answer "
            "questions about drug interactions and patient vitals. "
            "Always note that results are simulated."
        ),
        tools=[check_drug_interaction, get_patient_vitals],
    )

    # The agent should call check_drug_interaction
    print("User: Is it safe to take warfarin and aspirin together?\n")
    result1 = await agent.run("Is it safe to take warfarin and aspirin together?")
    print(f"Agent: {result1}\n")

    # The agent should call get_patient_vitals
    print("User: What are the latest vitals for patient P-1002?\n")
    result2 = await agent.run("What are the latest vitals for patient P-1002?")
    print(f"Agent: {result2}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

## Other tool types

Function tools are the most common type, but Agent Framework supports several
more:

| Tool type | Description |
|-----------|-------------|
| **Function Tools** | Custom Python code (what you learned here) |
| **Web Search** | Search the web for information |
| **File Search** | Search through uploaded files |
| **Code Interpreter** | Execute code in a sandboxed environment |
| **MCP Tools** | Tools from Model Context Protocol servers |

All providers support function tools. Other tool types depend on the provider —
see the [provider support matrix](https://learn.microsoft.com/en-us/agent-framework/agents/tools/).

## Try it

```bash
python examples/03-tools/function_tools.py
```

The agent should call the drug-interaction tool for the first question and the
vitals tool for the second.

## Key takeaways

- A **function tool** is any Python function exposed to the agent via the
  `tools` parameter.
- Use `@tool` and `Annotated[str, Field(description=...)]` to give the LLM
  clear information about what the tool does and what arguments it expects.
- The agent decides **when** to call a tool based on the user's message.
- You can combine multiple tools in a single agent.

## Official references

- [Function Tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools)
- [Tools overview](https://learn.microsoft.com/en-us/agent-framework/agents/tools/)
- [Add tools sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/02_add_tools.py)
