"""Test configuration and fixtures."""

import pytest
from typing import Generator, Any


@pytest.fixture
def sample_threat_scenario() -> dict[str, Any]:
    """Sample threat scenario configuration for testing."""
    return {
        "name": "Test Phishing Scenario",
        "description": "A test phishing scenario for unit testing",
        "threat_type": "phishing",
        "delivery_vector": "email",
        "target_profile": {
            "role": "Manager",
            "seniority": "mid",
            "department": "IT",
            "technical_level": "high",
            "industry": "technology",
            "company_size": "medium"
        },
        "difficulty_level": 5,
        "estimated_duration": 30,
        "mitre_attack_techniques": ["T1566.001", "T1566.002"],
        "simulation_parameters": {
            "max_iterations": 3,
            "escalation_enabled": True,
            "response_adaptation": True,
            "time_pressure_simulation": False
        }
    }


@pytest.fixture
def mock_llm_response() -> str:
    """Mock LLM response for testing."""
    return "This is a simulated threat content for testing purposes."


@pytest.fixture
def test_database_url() -> str:
    """Test database URL."""
    return "sqlite:///test_threatgpt.db"


@pytest.fixture
def test_redis_url() -> str:
    """Test Redis URL."""
    return "redis://localhost:6379/1"


# Test markers
pytest_plugins = []