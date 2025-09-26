"""Production-ready configuration loader for ThreatGPT."""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class LLMProviderConfig(BaseModel):
    """Configuration for LLM providers."""
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    base_url: str = "https://api.openai.com/v1"
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout_seconds: int = 30
    retry_attempts: int = 3


class SimulationConfig(BaseModel):
    """Core simulation configuration."""
    max_stages: int = 10
    default_timeout_minutes: int = 30
    enable_safety_checks: bool = True
    enable_content_filtering: bool = True
    enable_audit_logging: bool = True
    max_concurrent_simulations: int = 5


class SafetyConfig(BaseModel):
    """Safety and compliance configuration."""
    enable_safety_validation: bool = True
    blocked_keywords: list = Field(default_factory=list)
    content_moderation: bool = True
    compliance_mode: bool = True
    audit_all_operations: bool = True


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/threatgpt.log"
    max_file_size_mb: int = 50
    backup_count: int = 5
    enable_console_logging: bool = True


class APIConfig(BaseModel):
    """API server configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list = Field(default_factory=lambda: ["http://localhost:3000"])
    rate_limiting: Dict[str, Any] = Field(default_factory=dict)
    authentication: Dict[str, Any] = Field(default_factory=dict)


class ThreatGPTConfig(BaseModel):
    """Main ThreatGPT configuration."""
    
    llm: Dict[str, Any] = Field(default_factory=dict)
    simulation: SimulationConfig = Field(default_factory=SimulationConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    
    # Optional configurations
    templates: Dict[str, Any] = Field(default_factory=dict)
    deployment: Dict[str, Any] = Field(default_factory=dict)
    intelligence: Dict[str, Any] = Field(default_factory=dict)
    database: Dict[str, Any] = Field(default_factory=dict)


class ConfigurationLoader:
    """Production-ready configuration loader."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize configuration loader.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else Path("config.yaml")
        self._config = None
    
    def load_config(self) -> ThreatGPTConfig:
        """Load configuration from file and environment."""
        if self._config is None:
            self._config = load_config(self.config_path)
        return self._config
    
    def load_scenario(self, config_path: str) -> Dict[str, Any]:
        """Load scenario configuration using YAML loader."""
        from .yaml_loader import load_and_validate_scenario
        
        try:
            scenario = load_and_validate_scenario(config_path)
            return {
                "name": scenario.metadata.name,
                "threat_type": scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else str(scenario.threat_type),
                "description": scenario.metadata.description,
                "difficulty": scenario.difficulty_level.value if hasattr(scenario.difficulty_level, 'value') else scenario.difficulty_level,
                "status": "loaded"
            }
        except Exception as e:
            logger.error(f"Failed to load scenario {config_path}: {e}")
            return {
                "name": "Failed to Load",
                "threat_type": "unknown",
                "status": "error",
                "error": str(e)
            }
    
    def __repr__(self) -> str:
        return f"ConfigurationLoader(config_path={self.config_path})"


def load_config(config_path: Optional[Union[str, Path]] = None) -> ThreatGPTConfig:
    """Load ThreatGPT configuration from file and environment variables.
    
    Args:
        config_path: Path to configuration file. Defaults to config.yaml in current directory.
        
    Returns:
        ThreatGPTConfig instance with loaded configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If configuration is invalid
    """
    if config_path is None:
        config_path = Path("config.yaml")
    else:
        config_path = Path(config_path)
    
    # Load base configuration from file
    config_data = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.warning(f"Failed to load config file {config_path}: {e}")
            config_data = {}
    else:
        logger.info(f"Config file {config_path} not found, using defaults")
    
    # Override with environment variables
    config_data = _apply_environment_overrides(config_data)
    
    # Validate and create configuration object
    try:
        config = ThreatGPTConfig.parse_obj(config_data)
        logger.info("Configuration validated successfully")
        return config
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise ValueError(f"Invalid configuration: {e}")


def _apply_environment_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply environment variable overrides to configuration.
    
    Args:
        config_data: Base configuration data from file
        
    Returns:
        Configuration data with environment overrides applied
    """
    # LLM API Keys
    if os.getenv('OPENAI_API_KEY'):
        if 'llm' not in config_data:
            config_data['llm'] = {}
        if 'openai' not in config_data['llm']:
            config_data['llm']['openai'] = {}
        config_data['llm']['openai']['api_key'] = os.getenv('OPENAI_API_KEY')
    
    if os.getenv('ANTHROPIC_API_KEY'):
        if 'llm' not in config_data:
            config_data['llm'] = {}
        if 'anthropic' not in config_data['llm']:
            config_data['llm']['anthropic'] = {}
        config_data['llm']['anthropic']['api_key'] = os.getenv('ANTHROPIC_API_KEY')
    
    if os.getenv('OPENROUTER_API_KEY'):
        if 'llm' not in config_data:
            config_data['llm'] = {}
        if 'openrouter' not in config_data['llm']:
            config_data['llm']['openrouter'] = {}
        config_data['llm']['openrouter']['api_key'] = os.getenv('OPENROUTER_API_KEY')
    
    # API Configuration
    if os.getenv('API_KEY'):
        if 'api' not in config_data:
            config_data['api'] = {}
        if 'authentication' not in config_data['api']:
            config_data['api']['authentication'] = {}
        config_data['api']['authentication']['api_key'] = os.getenv('API_KEY')
        config_data['api']['authentication']['enabled'] = True
    
    # Logging level override
    if os.getenv('LOG_LEVEL'):
        if 'logging' not in config_data:
            config_data['logging'] = {}
        config_data['logging']['level'] = os.getenv('LOG_LEVEL')
    
    # Debug mode override
    if os.getenv('DEBUG'):
        if 'api' not in config_data:
            config_data['api'] = {}
        config_data['api']['debug'] = os.getenv('DEBUG').lower() in ('true', '1', 'yes')
    
    # Safety mode override
    if os.getenv('SAFETY_MODE'):
        if 'safety' not in config_data:
            config_data['safety'] = {}
        config_data['safety']['compliance_mode'] = os.getenv('SAFETY_MODE').lower() in ('true', '1', 'yes')
    
    return config_data


def setup_logging(config: ThreatGPTConfig) -> None:
    """Set up logging based on configuration.
    
    Args:
        config: ThreatGPT configuration instance
    """
    import logging.handlers
    
    # Create logs directory if it doesn't exist
    log_file = Path(config.logging.file_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Set up logging configuration
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
        handlers=[]
    )
    
    # Add file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=config.logging.max_file_size_mb * 1024 * 1024,
        backupCount=config.logging.backup_count
    )
    file_handler.setFormatter(logging.Formatter(config.logging.format))
    
    # Add console handler if enabled
    handlers = [file_handler]
    if config.logging.enable_console_logging:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(config.logging.format))
        handlers.append(console_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = handlers
    
    logger.info("Logging configured successfully")


def get_llm_config(config: ThreatGPTConfig, provider_name: str) -> Optional[LLMProviderConfig]:
    """Get LLM provider configuration.
    
    Args:
        config: ThreatGPT configuration instance
        provider_name: Name of the LLM provider
        
    Returns:
        LLM provider configuration or None if not found
    """
    provider_config = config.llm.get(provider_name)
    if provider_config:
        return LLMProviderConfig.parse_obj(provider_config)
    return None


def validate_production_config(config: ThreatGPTConfig) -> list:
    """Validate configuration for production deployment.
    
    Args:
        config: ThreatGPT configuration instance
        
    Returns:
        List of validation warnings/errors
    """
    issues = []
    
    # Check for API keys
    if not any(provider.get('api_key') for provider in config.llm.values()):
        issues.append("No LLM API keys configured - content generation will use fallback mode")
    
    # Check safety settings
    if not config.safety.enable_safety_validation:
        issues.append("Safety validation is disabled - not recommended for production")
    
    if not config.safety.compliance_mode:
        issues.append("Compliance mode is disabled - ensure this is intentional")
    
    # Check API security
    if config.api.debug:
        issues.append("Debug mode is enabled - disable for production")
    
    if not config.api.authentication.get('enabled', False):
        issues.append("API authentication is disabled - enable for production")
    
    # Check logging
    if config.logging.level.upper() == 'DEBUG':
        issues.append("Debug logging enabled - may impact performance in production")
    
    return issues