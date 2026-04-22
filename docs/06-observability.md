# 06 — Observability

When agents call LLMs and tools behind the scenes, it can be hard to
understand what actually happened. **Observability** gives you visibility into
every step of an agent run through traces and spans.

## Why observability matters for agents

- **Debugging** — see exactly which tools were called and what the LLM returned.
- **Performance** — measure latency of each LLM call and tool execution.
- **Reliability** — detect retries, errors, and unexpected tool results.
- **Cost** — track token usage per call.

## OpenTelemetry integration

Agent Framework has built-in support for
[OpenTelemetry](https://opentelemetry.io/) (OTel). When tracing is configured
with `configure_otel_providers`, the framework automatically emits spans for:

- Agent runs
- LLM calls (chat completions / responses)
- Tool invocations
- Workflow executor steps

## Viewing traces in the AI Toolkit

Rather than dumping verbose JSON spans to the terminal, we will send traces to
the **AI Toolkit** VS Code extension, which provides a visual trace viewer.

### Prerequisites

Install the **AI Toolkit** extension in VS Code. Open the Extensions panel
(`Ctrl+Shift+X`), search for **AI Toolkit** ([ms-windows-ai-studio.windows-ai-studio](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)),
and click **Install**.

You also need the OTLP gRPC exporter package (already in `requirements.txt`):

```bash
pip install opentelemetry-exporter-otlp-proto-grpc
```

### Start the trace collector

1. Open the **AI Toolkit** panel in VS Code (click the AI Toolkit icon in the
   sidebar).
2. Navigate to **Developer Tools → Monitor → Tracing**.
3. Click **Start** to begin the collector. Note the **gRPC port** shown
   (typically `4317`).

### Run the script with the collector port

Set the `VS_CODE_EXTENSION_PORT` environment variable to the gRPC port and run
the example:

```bash
VS_CODE_EXTENSION_PORT=4317 python examples/06-observability/traced_agent.py
```

The terminal shows only the agent response. The trace data (LLM calls, tool
invocations, token usage, timing) is sent to the AI Toolkit panel where you
can inspect it visually.

## The code

File: [`examples/06-observability/traced_agent.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/06-observability/traced_agent.py)

```python
import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework.observability import configure_otel_providers
from azure.identity import AzureCliCredential

load_dotenv()

# Set up OpenTelemetry tracing — sends traces to the AI Toolkit VS Code panel
configure_otel_providers(
    enable_console_exporters=False,
    enable_sensitive_data=True,
)


@tool(name="lookup_symptom", description="Look up common causes for a symptom.")
def lookup_symptom(symptom: str) -> str:
    """Return simulated symptom causes."""
    data = {
        "headache": "Common causes: tension, migraine, dehydration, eyestrain.",
        "chest pain": "Common causes: anxiety, GERD, muscle strain, cardiac issues.",
        "fatigue": "Common causes: poor sleep, anaemia, thyroid issues, stress.",
    }
    return data.get(symptom.lower(), f"No data available for '{symptom}'.")


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="TracedHealthBot",
        instructions=(
            "You are a health assistant. Use the lookup_symptom tool to find "
            "common causes for symptoms the user mentions."
        ),
        tools=[lookup_symptom],
    )

    print("Asking TracedHealthBot about fatigue...\n")
    result = await agent.run(
        "I have been feeling very fatigued lately. What could be causing it?"
    )
    print(f"\nAgent: {result}")
    print("\n(Open the AI Toolkit panel in VS Code to view the trace spans.)")


if __name__ == "__main__":
    asyncio.run(main())
```

## Step-by-step walkthrough

### 1. Configure tracing

```python
from agent_framework.observability import configure_otel_providers

configure_otel_providers(
    enable_console_exporters=False,
    enable_sensitive_data=True,
)
```

`configure_otel_providers` sets up OpenTelemetry providers and enables the
framework's internal instrumentation. When `VS_CODE_EXTENSION_PORT` is set in
the environment, it automatically creates OTLP exporters that send traces to
the AI Toolkit collector on that port. Setting `enable_sensitive_data=True`
includes the actual prompt and response content in the traces so you can
inspect the full conversation.

### 2. Define a tool and agent

The `@tool` decorator and `Agent` setup are the same as previous lessons. The
difference is that with tracing enabled, every tool call and LLM interaction is
now automatically traced — no extra code needed.

### 3. Inspect the trace

In the AI Toolkit trace viewer you will see:

| Span | Description |
|------|-------------|
| **Agent run** | Top-level span wrapping the entire `agent.run()` call |
| **Chat completion** | Each LLM call with model name, token counts, and duration |
| **Tool invocation** | `lookup_symptom` call with arguments and duration |

The spans are nested to show the call chain: agent run → LLM call → tool
invocation → second LLM call → response.

## Console exporter (alternative)

If you prefer to see spans in the terminal (e.g. in a CI environment), set
`enable_console_exporters=True`:

```python
configure_otel_providers(
    enable_console_exporters=True,
    enable_sensitive_data=True,
)
```

Then run without the port variable:

```bash
python examples/06-observability/traced_agent.py
```

This prints detailed JSON span objects to stdout — useful for debugging but
verbose.

## Viewing traces in Microsoft Foundry

Microsoft Foundry's **Tracing** view reads from an Application Insights
resource linked to your Foundry project. To see your agent traces there:

### 1. Connect Application Insights to your Foundry project

In the [Microsoft Foundry portal](https://ai.azure.com):

1. Select **Operate** in the upper-right navigation.
2. Select **Admin** in the left pane.
3. Select your **project name** in the "Manage all projects" list.
4. Under **Connected resources**, click **Add connection**.
5. Select **Application Insights** from the list of available services.
6. Browse for and select your Application Insights resource, then click
   **Add connection**.
7. Confirm it appears in the connected resources list.

### 2. Install the Azure Monitor package

```bash
pip install azure-monitor-opentelemetry
```

### 3. Get the connection string

Find it in one of two places:

- **Foundry portal** → **Operate** → **Admin** → select your project →
  **Connected resources** → click on the Application Insights connection to
  view its details including the connection string.
- **Azure portal** → your Application Insights resource → **Overview** →
  **Connection String**.

Add it to your `.env` file:

```
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

### 4. Update the code

Replace the `configure_otel_providers` call with `configure_azure_monitor` and
then enable the Agent Framework instrumentation:

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework.observability import enable_instrumentation

# Send traces to Application Insights (and therefore Foundry)
configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
)

# Enable Agent Framework's built-in span instrumentation
enable_instrumentation(enable_sensitive_data=True)
```

`configure_azure_monitor` sets up the OpenTelemetry provider with the Azure
Monitor exporter. `enable_instrumentation` then hooks the Agent Framework's
internal spans (LLM calls, tool invocations, agent runs) into that provider.

### 5. Run and view traces in Application Insights

```bash
python examples/06-observability/traced_agent.py
```

In this workshop we use **ephemeral** agents, they only exists for the duration of the script. They will
not appear as a persistent agent in the Foundry portal. The traces are still
exported to Application Insights and can be viewed there.

After a minute or two (telemetry ingestion is not instant), open the
**Azure portal** → your **Application Insights** resource → **Search**. You should see the trace with nested spans for the agent run, LLM
calls, and tool invocations. You can also use **Logs** to query traces with
KQL.

!!! tip
    Set `enable_sensitive_data=True` to include the actual prompt and response
    content in traces. Without it you see timing and token counts but not the
    message text.

## Key takeaways

- Agent Framework emits **OpenTelemetry spans** automatically when
  `configure_otel_providers` is called.
- Use the **AI Toolkit** extension in VS Code for a visual trace viewer
  during development.
- Set `VS_CODE_EXTENSION_PORT` to the collector's gRPC port (typically
  `4317`) before running your script.
- Use `enable_sensitive_data=True` to include prompt/response content in
  traces.
- Traces show the **full call chain**: agent → LLM → tools → response.
- For production, export to **Azure Monitor / Application Insights**.

## Official references

- [Observability samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/observability)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)
