#!/usr/bin/env python3
"""Test the free Grok model specifically"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_grok_free():
    """Test the free Grok model"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return
    
    print(f"✅ Testing free Grok model with API key: {api_key[:20]}...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
        'X-Title': 'ThreatGPT'
    }
    
    # Test the free Grok model
    payload = {
        'model': 'x-ai/grok-4-fast:free',
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, please respond with just "Hello from Grok!"'
            }
        ],
        'max_tokens': 50,
        'temperature': 0.1
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print("🔄 Making request to Grok...")
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                text = await response.text()
                print(f"Response status: {response.status}")
                print(f"Response length: {len(text)} chars")
                
                if response.status == 200:
                    data = json.loads(text)
                    print("✅ SUCCESS with Grok!")
                    print(f"Model: {data.get('model', 'N/A')}")
                    
                    if 'choices' in data and data['choices']:
                        content = data['choices'][0]['message']['content']
                        print(f"Response: {content}")
                        
                        # If Grok works, test it with ThreatGPT content
                        await test_grok_with_threatgpt_prompt()
                        
                    return True
                    
                else:
                    print(f"❌ Failed: {text}")
                    
                    # Try without the :free suffix
                    print("\n🔄 Trying without :free suffix...")
                    payload['model'] = 'x-ai/grok-4-fast'
                    
                    async with session.post(
                        'https://openrouter.ai/api/v1/chat/completions',
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as response2:
                        
                        text2 = await response2.text()
                        print(f"Status without suffix: {response2.status}")
                        
                        if response2.status == 200:
                            data2 = json.loads(text2)
                            print("✅ SUCCESS without :free suffix!")
                            content2 = data2['choices'][0]['message']['content']
                            print(f"Response: {content2}")
                            return True
                        else:
                            print(f"❌ Also failed: {text2}")
                    
                    return False
                    
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

async def test_grok_with_threatgpt_prompt():
    """Test Grok with actual ThreatGPT prompt"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
        'X-Title': 'ThreatGPT'
    }
    
    # ThreatGPT-style prompt
    payload = {
        'model': 'x-ai/grok-4-fast:free',
        'messages': [
            {
                'role': 'system',
                'content': 'You are ThreatGPT, a cybersecurity education assistant. Generate educational content about security threats for training purposes.'
            },
            {
                'role': 'user',
                'content': 'Generate educational content about email phishing detection techniques for security awareness training. Focus on defensive measures.'
            }
        ],
        'max_tokens': 300,
        'temperature': 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print("\n🧪 Testing Grok with ThreatGPT prompt...")
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    print("✅ ThreatGPT-style prompt works!")
                    print(f"Content length: {len(content)} chars")
                    print(f"Preview: {content[:200]}...")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ ThreatGPT prompt failed: {text}")
                    return False
                    
    except Exception as e:
        print(f"❌ ThreatGPT prompt error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_grok_free())
    if success:
        print("\n🎉 Found working model: x-ai/grok-4-fast:free")
        print("This can be used for ThreatGPT simulations!")
    else:
        print("\n❌ Grok model also failed")
        print("The OpenRouter account may need billing setup or verification")