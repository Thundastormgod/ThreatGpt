"""Core exception classes for ThreatGPT."""


class ThreatGPTError(Exception):
    """Base exception for all ThreatGPT errors."""
    pass


class SimulationError(ThreatGPTError):
    """Error during threat simulation execution."""
    pass


class ConfigurationError(ThreatGPTError):
    """Error in configuration loading or validation."""
    pass


class ValidationError(ThreatGPTError):
    """Error in data validation."""
    pass