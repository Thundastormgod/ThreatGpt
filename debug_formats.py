#!/usr/bin/env python3
"""Test different OpenRouter request formats to match web UI"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_different_formats():
    """Test different request formats that might match web UI"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return
    
    print(f"✅ Testing different request formats with API key: {api_key[:20]}...")
    
    # Test 1: Minimal headers (like Postman/curl)
    print("\n🧪 Test 1: Minimal headers")
    headers1 = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test 2: Standard headers with User-Agent
    print("\n🧪 Test 2: Standard headers with User-Agent")
    headers2 = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'User-Agent': 'ThreatGPT/1.0'
    }
    
    # Test 3: Web UI style headers
    print("\n🧪 Test 3: Web UI style headers")
    headers3 = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://openrouter.ai/',
        'X-Title': 'ThreatGPT',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Test 4: Different model name formats
    print("\n🧪 Test 4: Different Qwen model formats")
    qwen_variants = [
        'qwen/qwen3-vl-235b-a22b-thinking',
        'qwen/qwen-2.5-72b-instruct',
        'qwen/qwq-32b-preview',  # Another possible Qwen model
        'anthropic/claude-3-haiku-20240307'  # Fallback
    ]
    
    headers_list = [headers1, headers2, headers3] 
    
    for i, headers in enumerate(headers_list, 1):
        print(f"\n--- Testing header set {i} ---")
        
        for model in qwen_variants:
            print(f"  Trying model: {model}")
            
            payload = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': 'Hello, respond with just "Working!"'}
                ],
                'max_tokens': 20,
                'temperature': 0.1
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        'https://openrouter.ai/api/v1/chat/completions',
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            content = data['choices'][0]['message']['content']
                            print(f"  ✅ SUCCESS! Model: {model}")
                            print(f"  Response: {content}")
                            print(f"  Headers that worked: {list(headers.keys())}")
                            return model, headers
                        else:
                            text = await response.text()
                            error_data = json.loads(text) if text.startswith('{') else {'error': text}
                            error_msg = error_data.get('error', {}).get('message', text)
                            print(f"  ❌ {response.status}: {error_msg}")
                            
            except Exception as e:
                print(f"  ❌ Error: {e}")
            
            # Small delay between requests
            await asyncio.sleep(0.5)
    
    print("\n❌ No combination worked")
    
    # Test 5: Check account info endpoint
    print("\n🧪 Test 5: Check account info")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://openrouter.ai/api/v1/auth/key',
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                
                text = await response.text()
                print(f"Account info status: {response.status}")
                
                if response.status == 200:
                    data = json.loads(text)
                    print(f"Account data: {data}")
                else:
                    print(f"Account error: {text}")
                    
    except Exception as e:
        print(f"Account check error: {e}")
    
    return None, None

if __name__ == "__main__":
    result = asyncio.run(test_different_formats())
    
    if result[0]:  # If we found a working combination
        model, headers = result
        print(f"\n🎉 Working combination found!")
        print(f"Model: {model}")
        print(f"Headers: {headers}")
        
        # Save the working configuration
        with open('working_openrouter_config.json', 'w') as f:
            json.dump({
                'model': model,
                'headers': headers,
                'api_endpoint': 'https://openrouter.ai/api/v1/chat/completions'
            }, f, indent=2)
        
        print("✅ Saved working config to working_openrouter_config.json")
    else:
        print(f"\n💡 Next debugging steps:")
        print("1. In OpenRouter web UI, open browser DevTools (F12)")
        print("2. Go to Network tab") 
        print("3. Make a request with the Qwen model")
        print("4. Right-click the request → Copy → Copy as cURL")
        print("5. Check the exact headers and URL used")
        print("6. Compare with our test requests above")