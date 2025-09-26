"""ThreatGPT: AI-Powered Threat Simulation Platform.

A production-grade cybersecurity threat simulation platform that leverages
Large Language Models (LLMs) to generate realistic, context-aware threat
scenarios for training, awareness, and red teaming activities.
"""

__version__ = "0.1.0"
__author__ = "ThreatGPT Team"
__email__ = "okino007@gmail.com"
__license__ = "MIT"

# Core imports for public API
from threatgpt.core.models import SimulationResult, ThreatScenario
from threatgpt.core.simulator import ThreatSimulator
from threatgpt.config.loader import ConfigurationLoader

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "SimulationResult",
    "ThreatScenario",
    "ThreatSimulator",
    "ConfigurationLoader",
]