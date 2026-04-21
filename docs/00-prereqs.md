# 00 — Prerequisites

Before you start the workshop, make sure the following items are in place.

## Azure subscription

You need an active Azure subscription. If you do not have one, create a
[free account](https://azure.microsoft.com/free/).

## Azure CLI

Install the Azure CLI (version 2.67.0 or later) and sign in:

```bash
az login
az account show
```

## Python

Install **Python 3.10** or later. Verify with:

```bash
python --version
```

## Create a Microsoft Foundry project

1. Go to the [Azure portal](https://portal.azure.com) and create an
   **Azure AI Foundry** resource (or use an existing one).
2. Inside the resource, create a **project**.
3. Copy the **project endpoint** — it looks like:
   `https://<your-resource>.services.ai.azure.com/api/projects/<your-project>`

!!! tip
    The project endpoint is shown on the project overview page in the Azure
    portal.

## Deploy a model

Inside your Foundry project, deploy a model. This workshop recommends
**gpt-5.4-mini** because it is fast and cost-effective for learning.

1. Open your Foundry project in the Azure portal.
2. Navigate to **Deployments** → **Deploy model**.
3. Select `gpt-5.4-mini` and complete the deployment wizard.
4. Note the **deployment name** — you will use it as `FOUNDRY_MODEL` in your
   `.env` file.

## Install workshop dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set the two required values:

```
FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL=gpt-5.4-mini
```

## Verify your setup

Run a quick check to make sure everything works:

```bash
az account show          # should show your subscription
python -c "import agent_framework; print('OK')"
```

If both commands succeed, you are ready to start **Lesson 01**.

## Official references

- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Microsoft Foundry quickstart](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)
- [Azure CLI installation](https://learn.microsoft.com/cli/azure/install-azure-cli)
