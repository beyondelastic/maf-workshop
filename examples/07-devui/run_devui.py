"""Lesson 07 — Launch DevUI to interact with agents in the browser.

Run this script and open http://localhost:8080 in your browser.

Reference:
  https://github.com/microsoft/agent-framework/tree/main/python/packages/devui
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Ensure the agents directory is discoverable
agents_dir = os.path.join(os.path.dirname(__file__), "agents")

from agent_framework.devui import serve

# serve() auto-discovers agent directories and starts a web server.
serve(directory=agents_dir, port=8080, auto_open=True)
