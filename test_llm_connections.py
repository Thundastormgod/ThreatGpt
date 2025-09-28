#!/usr/bin/env python3
"""
ThreatGPT LLM Connection Tester

This script helps verify that your LLM providers are working correctly
and distinguishes between real AI responses and mock/fallback content.
"""

import asyncio
import logging
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Set up logging to see detailed LLM communication
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()

async def test_llm_providers():
    """Test all configured LLM providers."""
    from src.threatgpt.llm.manager import LLMManager
    
    console.print(Panel.fit("🧪 ThreatGPT LLM Provider Testing", style="bold blue"))
    
    # Configure providers with environment variables
    llm_config = {}
    
    # Check for OpenRouter API key
    if os.getenv('OPENROUTER_API_KEY'):
        llm_config['openrouter'] = {
            'api_key': os.getenv('OPENROUTER_API_KEY'),
            'model': 'qwen/qwen3-vl-235b-a22b-thinking'  # Your working model
        }
        console.print("OpenRouter API key found")
    else:
        console.print("OpenRouter API key not found (set OPENROUTER_API_KEY)")
    
    # Check for OpenAI API key
    if os.getenv('OPENAI_API_KEY'):
        llm_config['openai'] = {
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': 'gpt-3.5-turbo'
        }
        console.print("OpenAI API key found")
    else:
        console.print("OpenAI API key not found (set OPENAI_API_KEY)")
    
    # Check for Anthropic API key
    if os.getenv('ANTHROPIC_API_KEY'):
        llm_config['anthropic'] = {
            'api_key': os.getenv('ANTHROPIC_API_KEY'),
            'model': 'claude-3-haiku-20240307'
        }
        console.print("Anthropic API key found")
    else:
        console.print("Anthropic API key not found (set ANTHROPIC_API_KEY)")
    
    if not llm_config:
        console.print("No LLM provider API keys found. Please set at least one:")
        console.print("   - OPENROUTER_API_KEY")
        console.print("   - OPENAI_API_KEY") 
        console.print("   - ANTHROPIC_API_KEY")
        return
    
    # Initialize LLM manager
    llm_manager = LLMManager(config=llm_config)
    
    # Get provider status
    status = llm_manager.get_provider_status()
    
    console.print(f"\nProvider Status:")
    console.print(f"   Total providers configured: {status['total_providers']}")
    console.print(f"   Available providers: {len(status['available_providers'])}")
    console.print(f"   Unavailable providers: {len(status['unavailable_providers'])}")
    
    # Test each provider
    console.print(f"\n🧪 Testing Provider Connections:")
    
    results_table = Table(title="LLM Provider Test Results")
    results_table.add_column("Provider", style="cyan")
    results_table.add_column("Status", style="green")
    results_table.add_column("Response Type", style="yellow")
    results_table.add_column("Model", style="blue")
    results_table.add_column("Content Length", justify="right")
    
    test_results = []
    
    for provider_name in llm_manager.get_available_providers():
        console.print(f"\nTesting {provider_name}...")
        
        # Test connection
        result = await llm_manager.test_connection(provider_name)
        test_results.append((provider_name, result))
        
        status_emoji = "PASS" if result["status"] == "success" else "FAIL"
        response_type = result.get("response_type", "Unknown")
        model = result.get("model", "Unknown")
        content_length = result.get("content_length", 0)
        
        results_table.add_row(
            provider_name,
            f"{status_emoji} {result['status']}",
            response_type,
            model,
            str(content_length)
        )
    
    console.print(results_table)
    
    # Test actual content generation
    console.print(f"\nTesting Content Generation:")
    
    test_prompt = "Create a brief professional phishing email targeting a CEO about a board meeting document review."
    
    for provider_name in llm_manager.get_available_providers():
        console.print(f"\nGenerating content with {provider_name}...")
        
        try:
            response = await llm_manager.generate_content(
                prompt=test_prompt,
                scenario_type="phishing",
                max_tokens=200,
                provider_name=provider_name
            )
            
            is_real = getattr(response, 'is_real_ai', False)
            ai_type = "Real AI" if is_real else "Mock/Simulated"
            
            console.print(Panel(
                f"**Provider:** {response.provider}\n"
                f"**Model:** {response.model}\n"
                f"**Type:** {ai_type}\n"
                f"**Length:** {len(response.content)} characters\n\n"
                f"**Content Preview:**\n{response.content[:200]}{'...' if len(response.content) > 200 else ''}",
                title=f"Content from {provider_name}",
                border_style="green" if is_real else "yellow"
            ))
            
        except Exception as e:
            console.print(f"Content generation failed: {str(e)}")
    
    # Summary and recommendations
    console.print(f"\nSummary & Recommendations:")
    
    real_ai_count = sum(1 for _, result in test_results if result.get("is_real_ai", False))
    mock_count = len(test_results) - real_ai_count
    
    if real_ai_count > 0:
        console.print(f"{real_ai_count} provider(s) returning real AI responses")
    
    if mock_count > 0:
        console.print(f"{mock_count} provider(s) returning mock/simulated responses")
        console.print("   This likely means the provider implementation is using placeholder code")
        console.print("   instead of making real API calls.")
    
    if real_ai_count == 0:
        console.print("No providers are returning real AI responses!")
        console.print("   Check your API keys and provider implementations.")
    
    console.print(f"\nNext Steps:")
    console.print("1. Ensure at least one provider returns 'Real AI Response'")
    console.print("2. Check API keys are valid and have credits/quota")
    console.print("3. Review provider implementations for actual API calls")
    console.print("4. Monitor logs during simulations for real vs fallback content")

if __name__ == "__main__":
    asyncio.run(test_llm_providers())