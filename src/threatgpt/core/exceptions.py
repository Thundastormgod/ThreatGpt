"""Core exception classes for ThreatGPT."""

from typing import Optional


class ThreatGPTError(Exception):
    """Base exception for all ThreatGPT errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class SimulationError(ThreatGPTError):
    """Error during threat simulation execution."""
    def __init__(self, message: str, scenario_id: Optional[str] = None, stage_type: Optional[str] = None, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.scenario_id = scenario_id
        self.stage_type = stage_type


class ConfigurationError(ThreatGPTError):
    """Error in configuration loading or validation."""
    def __init__(self, message: str, config_path: Optional[str] = None, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.config_path = config_path


class ValidationError(ThreatGPTError):
    """Error in data validation."""
    def __init__(self, message: str, field_name: Optional[str] = None, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.field_name = field_name


class LLMProviderError(ThreatGPTError):
    """Error with LLM provider operations."""
    def __init__(self, message: str, provider_name: Optional[str] = None, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.provider_name = provider_name