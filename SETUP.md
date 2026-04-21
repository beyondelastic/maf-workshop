# Setup

This workshop assumes you have an Azure subscription and permission to use
Microsoft Foundry.

## 1. Azure prerequisites

Before you begin, verify:

- Your Azure subscription is active.
- You can sign in with `az login`.
- You have a role such as **Azure AI User** on the Foundry project.
- You already have, or can create, a Foundry resource and project.

Official references:

- [Set up Microsoft Foundry resources](https://learn.microsoft.com/azure/foundry/tutorials/quickstart-create-foundry-resources)
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)

## 2. Local prerequisites

- **Python 3.10** or later
- **Azure CLI 2.67.0** or later
- A **deployed model** in your Foundry project (recommended: `gpt-5.4-mini`)

## 3. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Authenticate

```bash
az login
az account show
```

## 5. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.example .env
```

Required values:

- `FOUNDRY_PROJECT_ENDPOINT` — your Foundry project endpoint from the Azure
  portal.
- `FOUNDRY_MODEL` — the model deployment name (default: `gpt-5.4-mini`).

## 6. Start the workshop UI

```bash
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.

## 7. Suggested workshop order

1. Read `docs/00-prereqs.md`
2. Run `examples/01-first-agent/hello_agent.py`
3. Run `examples/02-conversations/multi_turn.py`
4. Run `examples/02-conversations/memory_provider.py`
5. Run `examples/03-tools/function_tools.py`
6. Run `examples/04-workflow/sequential_workflow.py`
7. Run `examples/05-orchestration/magentic_orchestration.py`
8. Run `examples/06-observability/traced_agent.py`
9. Run `examples/07-devui/run_devui.py`

## Troubleshooting

**DefaultAzureCredential cannot get a token:**

1. Run `az login` again.
2. Verify your role assignment on the Foundry project.
3. Confirm your project endpoint matches the format from the Foundry portal.

**SDK errors:**

1. Check `pip show agent-framework`.
2. Ensure you are using `agent-framework>=1.0.0`.
3. Make sure your `.env` file has the correct `FOUNDRY_PROJECT_ENDPOINT` format.
