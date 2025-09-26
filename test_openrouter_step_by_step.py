#!/usr/bin/env python3
"""Test OpenRouter API step by step to isolate the issue"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_step_by_step():
    """Test OpenRouter API step by step"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return
    
    print(f"✅ Using API key: {api_key[:20]}...")
    
    # Step 1: Test models endpoint (this worked before)
    print("\n🔍 Step 1: Testing models endpoint...")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://openrouter.ai/api/v1/models',
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Models endpoint works - found {len(data.get('data', []))} models")
                    
                    # Find free models
                    free_models = []
                    for model in data.get('data', [])[:10]:  # Check first 10 models
                        pricing = model.get('pricing', {})
                        if pricing.get('prompt') == '0' or pricing.get('completion') == '0':
                            free_models.append(model.get('id'))
                    
                    if free_models:
                        print(f"Found {len(free_models)} potentially free models:")
                        for model in free_models[:3]:
                            print(f"  - {model}")
                    
                else:
                    text = await response.text()
                    print(f"❌ Models endpoint failed: {response.status} - {text}")
                    return
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return
    
    # Step 2: Test a very simple chat completion
    print("\n🔍 Step 2: Testing simple chat completion...")
    
    # Try the most basic possible request
    simple_payload = {
        'model': 'openai/gpt-3.5-turbo',  # Most common model
        'messages': [
            {'role': 'user', 'content': 'Hello'}
        ],
        'max_tokens': 10
    }
    
    # Test with minimal headers
    minimal_headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=minimal_headers,
                json=simple_payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                text = await response.text()
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    data = json.loads(text)
                    content = data['choices'][0]['message']['content']
                    print(f"✅ Simple chat works: {content}")
                else:
                    print(f"❌ Chat failed: {text}")
                    
                    # Try with additional headers
                    print("\n🔍 Step 3: Testing with OpenRouter-specific headers...")
                    
                    openrouter_headers = {
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json',
                        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
                        'X-Title': 'ThreatGPT'
                    }
                    
                    async with session.post(
                        'https://openrouter.ai/api/v1/chat/completions',
                        headers=openrouter_headers,
                        json=simple_payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response2:
                        text2 = await response2.text()
                        print(f"Status with OR headers: {response2.status}")
                        
                        if response2.status == 200:
                            data2 = json.loads(text2)
                            content2 = data2['choices'][0]['message']['content']
                            print(f"✅ With OR headers works: {content2}")
                        else:
                            print(f"❌ Still failed: {text2}")
                            
                            # Try completely different model
                            print("\n🔍 Step 4: Testing free model...")
                            
                            free_payload = {
                                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                                'messages': [
                                    {'role': 'user', 'content': 'Hello'}
                                ],
                                'max_tokens': 10
                            }
                            
                            async with session.post(
                                'https://openrouter.ai/api/v1/chat/completions',
                                headers=openrouter_headers,
                                json=free_payload,
                                timeout=aiohttp.ClientTimeout(total=30)
                            ) as response3:
                                text3 = await response3.text()
                                print(f"Free model status: {response3.status}")
                                
                                if response3.status == 200:
                                    data3 = json.loads(text3)
                                    content3 = data3['choices'][0]['message']['content']
                                    print(f"✅ Free model works: {content3}")
                                else:
                                    print(f"❌ Free model failed: {text3}")
                    
    except Exception as e:
        print(f"❌ Chat completion error: {e}")

if __name__ == "__main__":
    asyncio.run(test_step_by_step())