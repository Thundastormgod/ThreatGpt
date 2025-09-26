"""REST API for ThreatGPT.

Provides FastAPI-based REST endpoints for threat simulation,
scenario management, and system integration.
"""

from threatgpt.api.main import app

__all__ = [
    "app",
]