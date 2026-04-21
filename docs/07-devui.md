# 07 — DevUI

In this final lesson you will launch **DevUI** — the Agent Framework's
built-in browser-based developer interface. It lets you interact with your
agents visually, inspect conversations, and test tool calls without writing a
custom frontend.

## What is DevUI?

DevUI is a lightweight web application that ships with the `agent-framework`
package. It provides:

- **Chat interface** — talk to any agent in the browser.
- **Directory-based discovery** — agents are auto-discovered from a folder.
- **Multi-turn conversations** — built-in session management.
- **OpenAI-compatible API** — standard REST endpoints.
- **Telemetry** — optional OpenTelemetry trace viewer.

## Agent directory structure

DevUI expects each agent to live in its own subdirectory with an `__init__.py`
that exports a module-level `agent` variable:

```
agents/
└── health_bot/
    └── __init__.py      # must export: agent = Agent(...)
```

## The agent module

File: `examples/07-devui/agents/health_bot/__init__.py`

```python
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

# The variable MUST be named ``agent`` for DevUI discovery.
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
```

## The launcher script

File: `examples/07-devui/run_devui.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

agents_dir = os.path.join(os.path.dirname(__file__), "agents")

from agent_framework.devui import serve

serve(directory=agents_dir, port=8080, auto_open=True)
```

## How to run it

```bash
python examples/07-devui/run_devui.py
```

This starts a local web server. Your browser should open automatically to
`http://localhost:8080`. If it does not, open that URL manually.

## What you will see

- A **sidebar** listing all discovered agents (in this case, **HealthBot**).
- A **chat panel** where you can type messages and see the agent's responses.
- Tool calls are shown inline so you can see when the agent invokes
  `lookup_symptom`.

## DevUI API endpoints

DevUI also exposes an OpenAI-compatible REST API:

| Endpoint | Description |
|----------|-------------|
| `POST /v1/responses` | Execute an agent or workflow |
| `POST /v1/conversations` | Create a new conversation |
| `GET /v1/conversations/{id}` | Get conversation history |
| `GET /v1/entities` | List all discovered agents and workflows |
| `GET /health` | Health check |

You can use these endpoints with the standard OpenAI Python client or any HTTP
tool.

## CLI alternative

You can also launch DevUI from the command line without a script:

```bash
devui ./examples/07-devui/agents --port 8080
```

## Adding more agents

To add another agent to DevUI, create a new subdirectory under `agents/`:

```
agents/
├── health_bot/
│   └── __init__.py
└── triage_bot/
    └── __init__.py    # export: agent = Agent(...)
```

DevUI will automatically discover and list both agents.

## Try it

```bash
python examples/07-devui/run_devui.py
```

Then try:

- "What causes headaches?"
- "I have been feeling fatigued lately."
- "What about chest pain?"

## Key takeaways

- **DevUI** provides a browser-based chat interface for testing agents.
- Agents are discovered from a **directory structure** — each agent needs an
  `__init__.py` exporting an `agent` variable.
- DevUI exposes an **OpenAI-compatible API** alongside the web UI.
- It supports **multi-turn conversations** and **tool call inspection** out of
  the box.

## Official references

- [DevUI package](https://github.com/microsoft/agent-framework/tree/main/python/packages/devui)
- [DevUI sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/devui)
