"""Ollama local LLM provider implementation for ThreatGPT.

This module provides integration with Ollama for running local LLMs,
enabling offline usage without requiring API keys or internet connectivity.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from ..base import BaseLLMProvider
from ..models import LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider implementation.
    
    Connects to a local Ollama instance for running LLMs offline.
    Default endpoint: http://localhost:11434
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Ollama provider.
        
        Args:
            config: Configuration dictionary with Ollama settings
                - base_url: Ollama server URL (default: http://localhost:11434)
                - model: Model name (e.g., 'llama2', 'mistral', 'codellama')
                - timeout: Request timeout in seconds (default: 120)
        """
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model = config.get('model', 'llama2')
        self.timeout = config.get('timeout', 120)
        self.api_endpoint = f"{self.base_url}/api"
        
        logger.info(f"Initialized Ollama provider with model: {self.model}")
    
    def is_available(self) -> bool:
        """Check if Ollama server is available.
        
        Returns:
            bool: True if Ollama server is reachable
        """
        try:
            import httpx
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama server not available: {e}")
            return False
    
    async def generate_content(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Generate content using Ollama API.
        
        Args:
            prompt: The prompt to send to Ollama
            max_tokens: Maximum tokens to generate (not directly supported, uses num_predict)
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional Ollama parameters
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            Exception: If Ollama server is not available or request fails
        """
        if not self.is_available():
            raise ConnectionError(
                f"Ollama server not available at {self.base_url}. "
                "Please ensure Ollama is running: 'ollama serve'"
            )
        
        try:
            start_time = datetime.utcnow()
            
            # Prepare request payload for Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,  # Get complete response
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,  # Ollama's equivalent to max_tokens
                }
            }
            
            # Add any additional options from kwargs
            if 'top_p' in kwargs:
                payload['options']['top_p'] = kwargs['top_p']
            if 'top_k' in kwargs:
                payload['options']['top_k'] = kwargs['top_k']
            if 'repeat_penalty' in kwargs:
                payload['options']['repeat_penalty'] = kwargs['repeat_penalty']
            
            # Make request to Ollama
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_endpoint}/generate",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract response data
                content = result.get('response', '')
                
                # Calculate response time
                end_time = datetime.utcnow()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                # Ollama provides token counts in the response
                eval_count = result.get('eval_count', 0)  # Generated tokens
                prompt_eval_count = result.get('prompt_eval_count', 0)  # Prompt tokens
                
                logger.info(
                    f"Ollama generated {eval_count} tokens in {response_time:.2f}ms"
                )
                
                return LLMResponse(
                    content=content,
                    provider="ollama",
                    model=self.model,
                    tokens_used=eval_count,
                    timestamp=end_time,
                    metadata={
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "prompt_length": len(prompt),
                        "prompt_tokens": prompt_eval_count,
                        "completion_tokens": eval_count,
                        "total_tokens": prompt_eval_count + eval_count,
                        "response_time_ms": response_time,
                        "eval_duration": result.get('eval_duration', 0),
                        "total_duration": result.get('total_duration', 0),
                    }
                )
                
        except httpx.HTTPStatusError as e:
            error_msg = f"Ollama HTTP error: {e.response.status_code}"
            logger.error(f"{error_msg} - {e.response.text}")
            raise Exception(error_msg)
        except httpx.TimeoutException:
            error_msg = f"Ollama request timed out after {self.timeout}s"
            logger.error(error_msg)
            raise TimeoutError(error_msg)
        except Exception as e:
            logger.error(f"Ollama content generation failed: {e}")
            raise
    
    async def validate_connection(self) -> bool:
        """Validate connection to Ollama server.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Check if server is running
                response = await client.get(f"{self.api_endpoint}/tags")
                if response.status_code != 200:
                    return False
                
                # Check if the specified model is available
                models_data = response.json()
                available_models = [m['name'] for m in models_data.get('models', [])]
                
                if self.model not in available_models:
                    logger.warning(
                        f"Model '{self.model}' not found. Available: {available_models}"
                    )
                    logger.info(f"To pull the model, run: ollama pull {self.model}")
                    return False
                
                return True
                
        except Exception as e:
            logger.error(f"Ollama connection validation failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current Ollama model.
        
        Returns:
            Dict with model information
        """
        return {
            "provider": "ollama",
            "model": self.model,
            "base_url": self.base_url,
            "endpoint": self.api_endpoint,
            "configured": True,
            "requires_api_key": False,
            "offline_capable": True
        }
    
    async def list_available_models(self) -> list:
        """List all models available in local Ollama instance.
        
        Returns:
            List of available model names
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.api_endpoint}/tags")
                if response.status_code == 200:
                    models_data = response.json()
                    models = models_data.get('models', [])
                    return [
                        {
                            'name': m['name'],
                            'size': m.get('size', 0),
                            'modified': m.get('modified_at', '')
                        }
                        for m in models
                    ]
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
        return []
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull/download a model from Ollama registry.
        
        Args:
            model_name: Name of the model to pull (e.g., 'llama2', 'mistral')
            
        Returns:
            bool: True if model was pulled successfully
        """
        try:
            logger.info(f"Pulling Ollama model: {model_name}")
            
            async with httpx.AsyncClient(timeout=600.0) as client:  # 10 min timeout
                response = await client.post(
                    f"{self.api_endpoint}/pull",
                    json={"name": model_name},
                    timeout=600.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully pulled model: {model_name}")
                    return True
                else:
                    logger.error(f"Failed to pull model: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
    
    def get_system_prompt(self, scenario_type: str = "general") -> str:
        """Get system prompt for different scenario types.
        
        Args:
            scenario_type: Type of threat scenario
            
        Returns:
            System prompt string
        """
        prompts = {
            "phishing": (
                "You are a cybersecurity training assistant creating educational "
                "phishing simulation content. Generate realistic but clearly marked "
                "training materials for security awareness."
            ),
            "malware": (
                "You are a cybersecurity educator creating malware awareness training. "
                "Generate educational content about malware threats and indicators "
                "for security training purposes."
            ),
            "social_engineering": (
                "You are creating social engineering awareness training content. "
                "Generate realistic training scenarios to educate users about "
                "social engineering tactics."
            ),
            "general": (
                "You are a cybersecurity training assistant. Generate educational "
                "security content for training and awareness purposes."
            )
        }
        return prompts.get(scenario_type, prompts["general"])
