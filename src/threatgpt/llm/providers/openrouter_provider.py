"""OpenRouter LLM provider for ThreatGPT.

This provider integrates with OpenRouter API to access multiple LLM models
through a single API interface, providing flexibility and cost-effectiveness.
"""

import logging
import asyncio
import aiohttp
from typing import Optional, Dict, Any, List

from ..base import BaseLLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter API provider for multiple LLM models."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenRouter provider.
        
        Args:
            config: Configuration dict with api_key, model, etc.
        """
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'qwen/qwen3-vl-235b-a22b-thinking')  # Default to working Qwen model
        self.base_url = config.get('base_url', 'https://openrouter.ai/api/v1')
        self.app_name = config.get('app_name', 'ThreatGPT')
        self.site_url = config.get('site_url', 'https://github.com/threatgpt/threatgpt')
        
        # Popular model options for ThreatGPT (including user's working Qwen model)
        self.recommended_models = {
            'qwen-3l-235b': 'qwen/qwen3-vl-235b-a22b-thinking',  # User's preferred working model
            'qwen-2.5-72b': 'qwen/qwen-2.5-72b-instruct',
            'qwen-2.5-7b': 'qwen/qwen-2.5-7b-instruct',
            'claude-3-haiku': 'anthropic/claude-3-haiku',
            'claude-3-sonnet': 'anthropic/claude-3-sonnet', 
            'gpt-4o-mini': 'openai/gpt-4o-mini',
            'gpt-4o': 'openai/gpt-4o',
            'llama-3.1-70b': 'meta-llama/llama-3.1-70b-instruct',
            'llama-3.1-8b': 'meta-llama/llama-3.1-8b-instruct',
            'mixtral-8x7b': 'mistralai/mixtral-8x7b-instruct',
            'gemini-pro': 'google/gemini-pro'
        }
        
        if not self.api_key:
            logger.warning("OpenRouter API key not provided")
    
    def is_available(self) -> bool:
        """Check if OpenRouter provider is available."""
        return bool(self.api_key)
    
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate response from prompt (required by base class)."""
        result = await self.generate_content(prompt)
        if result is None:
            return LLMResponse("Error: Failed to generate content")
        return result
    
    async def generate_content(
        self,
        prompt: str,
        scenario_type: str = "general",
        max_tokens: int = 800,  # Reduced from 1000 for faster generation
        temperature: float = 0.7,
        **kwargs
    ) -> Optional[LLMResponse]:
        """Generate content using OpenRouter API.
        
        Args:
            prompt: The input prompt
            scenario_type: Type of scenario for context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse with generated content or None if failed
        """
        if not self.is_available():
            logger.error("OpenRouter provider not available - missing API key")
            return None
        
        try:
            # Prepare request headers
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': self.site_url,
                'X-Title': self.app_name
            }
            
            # Prepare request payload
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': self._get_system_prompt(scenario_type)
                    },
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ],
                'max_tokens': max_tokens,
                'temperature': temperature,
                'stream': False
            }
            
            # Add any additional parameters
            for key, value in kwargs.items():
                if key not in ['prompt', 'scenario_type']:
                    payload[key] = value
            
            # Make API request with retry logic
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries + 1):
                try:
                    async with aiohttp.ClientSession() as session:
                        timeout = aiohttp.ClientTimeout(total=45)  # Reduced from 60s
                        async with session.post(
                            f'{self.base_url}/chat/completions',
                            headers=headers,
                            json=payload,
                            timeout=timeout
                        ) as response:
                            
                            if response.status == 200:
                                data = await response.json()
                                
                                # Extract content from response
                                if 'choices' in data and len(data['choices']) > 0:
                                    content = data['choices'][0]['message']['content']
                                    
                                    # Extract usage information if available
                                    usage = data.get('usage', {})
                                    
                                    # Create simple LLMResponse with just content
                                    response = LLMResponse(content)
                                    
                                    # Add metadata as attributes if needed
                                    response.provider = 'openrouter'
                                    response.model = self.model
                                    response.usage = usage
                                    response.response_id = data.get('id')
                                    response.model_used = data.get('model', self.model)
                                    
                                    return response
                                else:
                                    logger.error("No content in OpenRouter response")
                                    return None
                            else:
                                error_text = await response.text()
                                logger.warning(f"OpenRouter API error {response.status} (attempt {attempt + 1}): {error_text}")
                                if attempt == max_retries:
                                    logger.error(f"OpenRouter API failed after {max_retries + 1} attempts")
                                    return None
                                await asyncio.sleep(retry_delay * (attempt + 1))
                                continue
                        
                except asyncio.TimeoutError:
                    logger.warning(f"OpenRouter API timeout (attempt {attempt + 1})")
                    if attempt == max_retries:
                        logger.error(f"OpenRouter API timed out after {max_retries + 1} attempts")
                        return None
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                except aiohttp.ClientError as e:
                    logger.warning(f"OpenRouter client error (attempt {attempt + 1}): {str(e)}")
                    if attempt == max_retries:
                        logger.error(f"OpenRouter client error after {max_retries + 1} attempts: {str(e)}")
                        return None
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                
                break  # Success, exit retry loop
                        
        except Exception as e:
            logger.error(f"Unexpected error in OpenRouter provider: {str(e)}")
            return None
    
    def _get_system_prompt(self, scenario_type: str) -> str:
        """Get system prompt based on scenario type."""
        base_prompt = """You are ThreatGPT, an AI assistant specialized in cybersecurity education and training. 
Your role is to generate realistic but educational threat simulation content for security awareness training.

IMPORTANT GUIDELINES:
- Generate educational content only - never provide actual attack instructions
- Focus on detection, prevention, and defensive measures
- Use placeholder/example data for any sensitive information
- Emphasize learning objectives and security best practices
- Keep content appropriate for professional security training environments
- Include specific indicators of compromise (IoCs) when relevant"""
        
        scenario_prompts = {
            'threat_simulation_reconnaissance': base_prompt + """

For reconnaissance scenarios, focus on:
- Information gathering techniques that defenders should monitor
- OSINT sources and their detection methods
- Behavioral indicators that security teams should watch for
- Defensive countermeasures and monitoring strategies""",
            
            'threat_simulation_delivery': base_prompt + """

For delivery scenarios, focus on:
- Common attack vectors and their characteristics
- Email security controls and detection methods
- Social engineering indicators and red flags
- User education and awareness training points""",
            
            'threat_simulation_exploitation': base_prompt + """

For exploitation scenarios, focus on:
- Common vulnerability patterns and their mitigation
- System hardening and security controls
- Incident detection and response procedures
- Forensic artifacts and evidence collection""",
            
            'threat_simulation_persistence': base_prompt + """

For persistence scenarios, focus on:
- Persistence mechanism detection methods
- System monitoring and anomaly detection
- Threat hunting techniques and indicators
- Recovery and remediation procedures"""
        }
        
        return scenario_prompts.get(scenario_type, base_prompt)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            'provider': 'openrouter',
            'model': self.model,
            'base_url': self.base_url,
            'available': self.is_available(),
            'recommended_models': self.recommended_models
        }
    
    def list_available_models(self) -> List[str]:
        """List recommended models available through OpenRouter."""
        return list(self.recommended_models.keys())
    
    async def test_connection(self) -> bool:
        """Test connection to OpenRouter API."""
        if not self.is_available():
            return False
        
        try:
            test_response = await self.generate_content(
                prompt="Test connection. Please respond with 'Connection successful.'",
                scenario_type="general",
                max_tokens=50,
                temperature=0.1
            )
            
            return test_response is not None and "successful" in test_response.content.lower()
            
        except Exception as e:
            logger.error(f"OpenRouter connection test failed: {str(e)}")
            return False