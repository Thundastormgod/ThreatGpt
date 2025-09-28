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
            provider_name = type(provider).__name__
            logger.info(f"🤖 Attempting to generate content with {provider_name}")
            logger.info(f"📝 Prompt length: {len(enhanced_prompt)} characters")
            logger.info(f"🎯 Scenario type: {scenario_type}")
            
            response = await provider.generate_content(
                prompt=enhanced_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Check if this is a real API response or mock content
            if response and hasattr(response, 'provider') and response.provider != "fallback":
                logger.info(f"✅ Real AI content generated from {response.provider}")
                logger.info(f"📊 Content length: {len(response.content)} characters")
                logger.info(f"🤖 Model used: {getattr(response, 'model', 'unknown')}")
                
                # Validate and sanitize response
                response = self._validate_response(response, scenario_type)
                response.is_real_ai = True
                return response
            else:
                logger.warning(f"⚠️  Received mock/simulated content from {provider_name}")
                if response:
                    response.is_real_ai = False
                    return response
                else:
                    raise RuntimeError("Provider returned None response")
            
        except Exception as e:
            logger.error(f"❌ Content generation failed with {type(provider).__name__}: {str(e)}")
            logger.error(f"🔄 Returning fallback content for {scenario_type} scenario")
            
            # Create clear fallback response
            fallback_response = LLMResponse(
                content=f"[FALLBACK CONTENT] Unable to generate real AI content for {scenario_type} scenario. Error: {str(e)}"
            )
            fallback_response.provider = "fallback"
            fallback_response.model = "none"
            fallback_response.error = str(e)
            fallback_response.scenario_type = scenario_type
            fallback_response.is_real_ai = False
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
            logger.warning(f"⚠️  Received insufficient content (length: {len(response.content if response.content else 'None')})")
            response.content = f"[Insufficient content generated for {scenario_type} scenario]"
            response.is_real_ai = False
        
        # Log content type and quality
        is_fallback = response.content.startswith("[FALLBACK") or response.content.startswith("[Content generation unavailable")
        if is_fallback:
            logger.warning("⚠️  Response contains fallback content")
            response.is_real_ai = False
        
        # Add safety metadata as attributes if metadata doesn't exist
        if hasattr(response, 'metadata') and response.metadata:
            response.metadata["safety_validated"] = True
            response.metadata["scenario_type"] = scenario_type
            response.metadata["validation_timestamp"] = datetime.utcnow().isoformat()
            response.metadata["is_real_ai"] = getattr(response, 'is_real_ai', False)
        else:
            # Simple LLMResponse - add as attributes
            response.safety_validated = True
            response.scenario_type = scenario_type
            response.validation_timestamp = datetime.utcnow().isoformat()
            response.is_real_ai = getattr(response, 'is_real_ai', False)
        
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
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get detailed status of all providers."""
        status = {
            "total_providers": len(self._providers),
            "available_providers": [],
            "unavailable_providers": [],
            "current_provider": None
        }
        
        for name, provider in self._providers.items():
            provider_info = {
                "name": name,
                "class": type(provider).__name__,
                "available": provider.is_available() if hasattr(provider, 'is_available') else True,
                "has_api_key": bool(getattr(provider, 'api_key', None))
            }
            
            if provider_info["available"]:
                status["available_providers"].append(provider_info)
            else:
                status["unavailable_providers"].append(provider_info)
        
        if self.provider:
            status["current_provider"] = {
                "name": type(self.provider).__name__,
                "available": self.provider.is_available() if hasattr(self.provider, 'is_available') else True
            }
        
        return status
    
    async def test_connection(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Test connection to LLM provider with real/mock detection."""
        provider = self._get_provider(provider_name)
        if not provider:
            return {"status": "error", "message": "No provider available"}
        
        provider_class_name = type(provider).__name__
        logger.info(f"🧪 Testing connection to {provider_class_name}...")
        
        try:
            test_response = await provider.generate_content(
                prompt="Hello, this is a connection test. Please respond with 'Connection successful'.",
                max_tokens=50
            )
            
            is_real_ai = getattr(test_response, 'is_real_ai', False)
            response_type = "Real AI Response" if is_real_ai else "Mock/Simulated Response"
            
            result = {
                "status": "success",
                "provider": provider_class_name,
                "model": getattr(test_response, 'model', 'unknown'),
                "response_type": response_type,
                "is_real_ai": is_real_ai,
                "content_length": len(test_response.content) if test_response.content else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if is_real_ai:
                logger.info(f"✅ {provider_class_name} connection successful - Real AI response received")
            else:
                logger.warning(f"⚠️  {provider_class_name} connection returned mock/simulated content")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ {provider_class_name} connection failed: {str(e)}")
            return {
                "status": "error",
                "provider": provider_class_name,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }