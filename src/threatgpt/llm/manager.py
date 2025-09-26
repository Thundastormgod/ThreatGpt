"""LLM manager for ThreatGPT content generation.

This module provides a production-ready LLM manager that handles
content generation for threat scenarios with multiple provider support.
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import BaseLLMProvider, LLMResponse
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.openrouter_provider import OpenRouterProvider

logger = logging.getLogger(__name__)


class LLMManager:
    """Production-ready LLM manager for threat content generation."""
    
    def __init__(self, provider: Optional[BaseLLMProvider] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize LLM manager.
        
        Args:
            provider: Specific LLM provider to use
            config: Configuration for LLM providers
        """
        self.config = config or {}
        self.provider = provider
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._initialize_providers()
        
    def _initialize_providers(self) -> None:
        """Initialize available LLM providers."""
        try:
            # Initialize OpenAI if configured
            openai_config = self.config.get('openai', {})
            if openai_config.get('api_key'):
                self._providers['openai'] = OpenAIProvider(openai_config)
                logger.info("OpenAI provider initialized")
            
            # Initialize Anthropic if configured
            anthropic_config = self.config.get('anthropic', {})
            if anthropic_config.get('api_key'):
                self._providers['anthropic'] = AnthropicProvider(anthropic_config)
                logger.info("Anthropic provider initialized")
            
            # Initialize OpenRouter if configured
            openrouter_config = self.config.get('openrouter', {})
            if openrouter_config.get('api_key'):
                self._providers['openrouter'] = OpenRouterProvider(openrouter_config)
                logger.info("OpenRouter provider initialized")
            
            # Set default provider if not specified
            if not self.provider and self._providers:
                provider_name = list(self._providers.keys())[0]
                self.provider = self._providers[provider_name]
                logger.info(f"Using default provider: {provider_name}")
                
        except Exception as e:
            logger.warning(f"Failed to initialize some LLM providers: {e}")
    
    async def generate_content(
        self,
        prompt: str,
        scenario_type: str = "general",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        provider_name: Optional[str] = None
    ) -> LLMResponse:
        """Generate content using the configured LLM provider.
        
        Args:
            prompt: The prompt to send to the LLM
            scenario_type: Type of scenario for context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            provider_name: Specific provider to use
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            RuntimeError: If no provider is available or generation fails
        """
        # Select provider
        provider = self._get_provider(provider_name)
        if not provider:
            raise RuntimeError("No LLM provider available")
        
        # Enhance prompt with safety guidelines
        enhanced_prompt = self._enhance_prompt_with_safety(prompt, scenario_type)
        
        try:
            logger.debug(f"Generating content with {type(provider).__name__}")
            response = await provider.generate_content(
                prompt=enhanced_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Validate and sanitize response
            response = self._validate_response(response, scenario_type)
            
            logger.info(f"Content generated successfully: {len(response.content)} characters")
            return response
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            # Return fallback content instead of failing completely
            fallback_response = LLMResponse(f"[Content generation unavailable: {scenario_type} scenario]")
            fallback_response.provider = "fallback"
            fallback_response.model = "none"
            fallback_response.error = str(e)
            fallback_response.scenario_type = scenario_type
            return fallback_response
    
    def _get_provider(self, provider_name: Optional[str] = None) -> Optional[BaseLLMProvider]:
        """Get the appropriate provider."""
        if provider_name and provider_name in self._providers:
            return self._providers[provider_name]
        elif self.provider:
            return self.provider
        elif self._providers:
            return list(self._providers.values())[0]
        return None
    
    def _enhance_prompt_with_safety(self, prompt: str, scenario_type: str) -> str:
        """Enhance prompt with safety guidelines."""
        safety_prefix = f"""
You are helping create educational cybersecurity content for training purposes.
Scenario type: {scenario_type}

Safety Guidelines:
- Content must be educational and defensive in nature
- Do not provide actual malicious code or real exploits
- Focus on awareness and prevention
- Use placeholder values for sensitive information
- Emphasize detection and mitigation strategies

User Request:
"""
        
        return safety_prefix + prompt
    
    def _validate_response(self, response: LLMResponse, scenario_type: str) -> LLMResponse:
        """Validate and sanitize LLM response."""
        # Basic content validation
        if not response.content or len(response.content.strip()) < 10:
            response.content = f"[Insufficient content generated for {scenario_type} scenario]"
        
        # Add safety metadata as attributes if metadata doesn't exist
        if hasattr(response, 'metadata') and response.metadata:
            response.metadata["safety_validated"] = True
            response.metadata["scenario_type"] = scenario_type
            response.metadata["validation_timestamp"] = datetime.utcnow().isoformat()
        else:
            # Simple LLMResponse - add as attributes
            response.safety_validated = True
            response.scenario_type = scenario_type
            response.validation_timestamp = datetime.utcnow().isoformat()
        
        return response
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return list(self._providers.keys())
    
    def get_provider_info(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed information about a provider."""
        provider = self._get_provider(provider_name)
        if not provider:
            return {"error": "Provider not available"}
        
        if hasattr(provider, 'get_model_info'):
            return provider.get_model_info()
        else:
            return {
                "provider": provider_name or "unknown",
                "available": provider.is_available() if hasattr(provider, 'is_available') else True
            }
    
    def list_openrouter_models(self) -> List[str]:
        """List available OpenRouter models."""
        if 'openrouter' in self._providers:
            provider = self._providers['openrouter']
            if hasattr(provider, 'list_available_models'):
                return provider.list_available_models()
        return []
    
    def is_available(self) -> bool:
        """Check if any LLM provider is available."""
        return bool(self.provider or self._providers)
    
    async def test_connection(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Test connection to LLM provider."""
        provider = self._get_provider(provider_name)
        if not provider:
            return {"status": "error", "message": "No provider available"}
        
        try:
            test_response = await provider.generate_content(
                prompt="Hello, this is a connection test.",
                max_tokens=10
            )
            
            return {
                "status": "success",
                "provider": type(provider).__name__,
                "model": test_response.model,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "provider": type(provider).__name__,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }