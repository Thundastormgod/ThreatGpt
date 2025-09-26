#!/usr/bin/env python3
"""Debug OpenRouter API calls to understand the exact request/response"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_openrouter_call():
    """Make the exact same API call as ThreatGPT"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return
    
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
    
    # User prompt from simulation
    user_prompt = """Target: Chief Executive Officer (CEO) in Financial Services industry
Seniority Level: C Level
Security Awareness: 6/10

Scenario: Executive Spear-Phishing Campaign
Description: Advanced spear-phishing attack targeting C-level executives with board meeting pretext and document sharing lure
Stage: reconnaissance

Requirements:
1. Generate educational cybersecurity content only
2. Focus on detection, prevention, and training aspects
3. Include specific indicators of compromise (IoCs)
4. Provide defensive recommendations
5. Use placeholder data for sensitive information
6. Keep content appropriate for security training

Generate comprehensive content for this simulation stage:"""
    
    # Try different models to see which ones work
    models_to_test = [
        'openai/gpt-4o-mini',
        'openai/gpt-3.5-turbo',
        'anthropic/claude-3-haiku-20240307',
        'meta-llama/llama-3.1-8b-instruct',
        'google/gemini-pro'
    ]
    
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
            'max_tokens': 800,
            'temperature': 0.7,
            'stream': False
        }
    
        print(f"Testing model: {model}")
        print(f"Max Tokens: {payload['max_tokens']}")
        print(f"Temperature: {payload['temperature']}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    print(f"Response Status: {response.status}")
                    
                    response_text = await response.text()
                    
                    if response.status == 200:
                        try:
                            data = json.loads(response_text)
                            print("✅ SUCCESS!")
                            print(f"Model Used: {data.get('model', 'N/A')}")
                            
                            if 'choices' in data and len(data['choices']) > 0:
                                content = data['choices'][0]['message']['content']
                                print(f"Content Length: {len(content)} chars")
                                print(f"Content Preview: {content[:300]}...")
                                return model  # Return successful model
                            
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON decode error: {e}")
                            
                    else:
                        print(f"❌ Error {response.status}")
                        try:
                            error_data = json.loads(response_text)
                            print(f"Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
                        except:
                            print(f"Raw response: {response_text[:100]}...")
                            
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print()  # Add space between tests
    
    print("❌ No models worked successfully")
    return None
                        
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_openrouter_call())