"""Base LLM provider interface.

This will be fully implemented in Week 3-4.
"""

from abc import ABC, abstractmethod
from typing import Any


class LLMResponse:
    """Placeholder LLM response."""
    def __init__(self, content: str):
        self.content = content


class BaseLLMProvider(ABC):
    """Base LLM provider interface."""
    
    def __init__(self, config: dict):
        """Initialize the provider with configuration."""
        self.config = config
    
    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate response from prompt."""
        pass