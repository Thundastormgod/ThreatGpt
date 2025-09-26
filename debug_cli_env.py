#!/usr/bin/env python3
"""Debug script to check what the CLI sees for environment variables."""

import os
from dotenv import load_dotenv
from src.threatgpt.llm.manager import LLMManager

print("🔍 Debugging CLI environment loading...")
print()

# Check system environment first
print("1. System Environment (before load_dotenv):")
print(f"   OPENROUTER_API_KEY: {os.environ.get('OPENROUTER_API_KEY', 'NOT_SET')[:25]}...")
print()

# Load .env file
print("2. Loading .env file...")
load_dotenv()
print(f"   OPENROUTER_API_KEY after load_dotenv: {os.getenv('OPENROUTER_API_KEY', 'NOT_SET')[:25]}...")
print()

# Check what LLMManager sees
print("3. Testing LLMManager initialization...")
try:
    # Create config with OpenRouter
    config = {
        'openrouter': {
            'api_key': os.getenv('OPENROUTER_API_KEY'),
            'model': 'qwen/qwen3-vl-235b-a22b-thinking'
        }
    }
    print(f"   Config API key: {config['openrouter']['api_key'][:25]}...")
    
    llm_manager = LLMManager(config=config)
    providers = llm_manager.get_available_providers()
    print(f"   Available providers: {providers}")
    
    if 'openrouter' in providers:
        print("   ✅ OpenRouter provider is available")
        
        # Test a simple generation
        print("4. Testing content generation...")
        import asyncio
        result = asyncio.run(llm_manager.generate_content("Test message", provider_name='openrouter'))
        if result:
            print(f"   ✅ Generation successful: {len(result.content)} characters")
            print(f"   Model used: {getattr(result, 'model_used', 'unknown')}")
        else:
            print("   ❌ Generation failed")
    else:
        print("   ❌ OpenRouter provider not available")
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("🎯 Environment debugging complete!")