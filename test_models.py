#!/usr/bin/env python3
"""Debug OpenRouter API calls to find working models"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_openrouter_models():
    """Test different OpenRouter models to find one that works"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return None
    
    print(f"✅ Using API key: {api_key[:20]}...")
    
    # Exact headers from ThreatGPT
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
        'X-Title': 'ThreatGPT'
    }
    
    # System prompt from ThreatGPT
    system_prompt = """You are ThreatGPT, an AI assistant specialized in cybersecurity education and training. 
Your role is to generate realistic but educational threat simulation content for security awareness training.

IMPORTANT GUIDELINES:
- Generate educational content only - never provide actual attack instructions
- Focus on detection, prevention, and defensive measures
- Use placeholder/example data for any sensitive information
- Emphasize learning objectives and security best practices
- Keep content appropriate for professional security training environments
- Include specific indicators of compromise (IoCs) when relevant

For reconnaissance scenarios, focus on:
- Information gathering techniques that defenders should monitor
- OSINT sources and their detection methods
- Behavioral indicators that security teams should watch for
- Defensive countermeasures and monitoring strategies"""
    
    # Simple test prompt
    user_prompt = """Generate educational content about email phishing detection for security training. Focus on defensive measures and indicators to watch for."""
    
    # Try different models to see which ones work
    models_to_test = [
        'openai/gpt-4o-mini',
        'openai/gpt-3.5-turbo', 
        'meta-llama/llama-3.1-8b-instruct',
        'google/gemini-pro',
        'anthropic/claude-3-haiku-20240307'
    ]
    
    working_models = []
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        
        # Request payload
        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user', 
                    'content': user_prompt
                }
            ],
            'max_tokens': 200,
            'temperature': 0.7,
            'stream': False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    response_text = await response.text()
                    
                    if response.status == 200:
                        try:
                            data = json.loads(response_text)
                            print("✅ SUCCESS!")
                            print(f"Model Used: {data.get('model', 'N/A')}")
                            
                            if 'choices' in data and len(data['choices']) > 0:
                                content = data['choices'][0]['message']['content']
                                print(f"Content Length: {len(content)} chars")
                                print(f"Content Preview: {content[:200]}...")
                                working_models.append(model)
                            
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON decode error: {e}")
                            
                    else:
                        print(f"❌ Error {response.status}")
                        try:
                            error_data = json.loads(response_text)
                            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                            print(f"Error: {error_msg}")
                        except:
                            print(f"Raw response: {response_text[:100]}...")
                            
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print(f"\n🎯 Summary:")
    if working_models:
        print(f"✅ Working models: {', '.join(working_models)}")
        return working_models[0]  # Return first working model
    else:
        print("❌ No models worked successfully")
        return None

if __name__ == "__main__":
    working_model = asyncio.run(test_openrouter_models())
    if working_model:
        print(f"\n🚀 Recommended model for ThreatGPT: {working_model}")
    else:
        print("\n💡 Suggestions:")
        print("1. Check OpenRouter account billing setup")
        print("2. Verify API key permissions") 
        print("3. Try creating a new API key")
        print("4. Contact OpenRouter support")