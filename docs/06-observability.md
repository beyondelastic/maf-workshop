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
[OpenTelemetry](https://opentelemetry.io/) (OTel). When a tracer provider is
configured, the framework automatically emits spans for:

- Agent runs
- LLM calls (chat completions / responses)
- Tool invocations
- Workflow executor steps

## The code

This example sets up a **console exporter** so you can see spans printed
directly to the terminal. In production you would export to Azure Monitor,
Jaeger, or another backend.

File: [`examples/06-observability/traced_agent.py`](https://github.com/beyondelastic/maf-workshop/blob/main/examples/06-observability/traced_agent.py)

```python
import asyncio
import os

from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()

# Set up OpenTelemetry tracing to print spans to the console
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)


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
    result = await agent.run("I have been feeling very fatigued lately. What could be causing it?")
    print(f"\nAgent: {result}")
    print("\n(Check the console output above for OpenTelemetry trace spans.)")


if __name__ == "__main__":
    asyncio.run(main())
```

## What you will see

When you run the script, the console exporter prints JSON-like span objects.
Each span includes:

| Field | Description |
|-------|-------------|
| `name` | The operation (e.g. `agent.run`, `chat.completions`, `tool.lookup_symptom`) |
| `trace_id` | Groups all spans from one workflow execution |
| `parent_id` | Shows the nesting (agent → LLM call → tool call) |
| `start_time` / `end_time` | Timing for latency analysis |
| `attributes` | Model name, token counts, tool arguments, etc. |

## Exporting to Azure Monitor

For a production setup, replace the console exporter with the Azure Monitor
exporter:

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(connection_string="InstrumentationKey=...")
```

This sends traces to Application Insights where you can query and visualise
them.

!!! tip
    Set the environment variable
    `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` to include
    message content in spans. This is useful for debugging but may increase
    data volume.

## Try it

```bash
python examples/06-observability/traced_agent.py
```

Look at the console output for span details. You should see a parent span for
the agent run, a child span for the LLM call, and (if the tool was called) a
child span for the tool invocation.

## Key takeaways

- Agent Framework emits **OpenTelemetry spans** automatically when a tracer is
  configured.
- Use a **console exporter** for local debugging and an **Azure Monitor
  exporter** for production.
- Traces show the **full call chain**: agent → LLM → tools → response.
- Observability is essential for debugging, performance tuning, and cost
  tracking.

## Official references

- [Observability samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/observability)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)
