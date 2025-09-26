#!/usr/bin/env python3
"""Test the specific Qwen model that works in OpenRouter web UI"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_qwen_model():
    """Test the Qwen 3L 235B model specifically"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return False
    
    print(f"✅ Testing Qwen model with API key: {api_key[:20]}...")
    
    # Headers that match OpenRouter requirements
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
        'X-Title': 'ThreatGPT'
    }
    
    # Test the specific Qwen model you mentioned
    qwen_models_to_test = [
        'qwen/qwen3-vl-235b-a22b-thinking',
        'qwen/qwen-2.5-72b-instruct',
        'qwen/qwen-2-72b-instruct',
        'qwen/qwen-2.5-7b-instruct'
    ]
    
    for model in qwen_models_to_test:
        print(f"\n🧪 Testing model: {model}")
        
        # Simple test payload
        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': 'Hello! Please respond with "Hello from Qwen!"'
                }
            ],
            'max_tokens': 50,
            'temperature': 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    response_text = await response.text()
                    print(f"Status: {response.status}")
                    
                    if response.status == 200:
                        try:
                            data = json.loads(response_text)
                            print("✅ SUCCESS!")
                            print(f"Model: {data.get('model', 'N/A')}")
                            
                            if 'choices' in data and data['choices']:
                                content = data['choices'][0]['message']['content']
                                print(f"Response: {content}")
                                
                                # If successful, test with ThreatGPT content
                                success = await test_qwen_with_threatgpt(model, headers)
                                if success:
                                    return model  # Return working model
                                
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON decode error: {e}")
                            print(f"Raw response: {response_text[:200]}...")
                            
                    else:
                        print(f"❌ Error: {response_text}")
                        
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n❌ No Qwen models worked")
    return False

async def test_qwen_with_threatgpt(model: str, headers: dict):
    """Test the working Qwen model with ThreatGPT-style content"""
    
    print(f"\n🎯 Testing {model} with ThreatGPT prompt...")
    
    # ThreatGPT system prompt
    system_prompt = """You are ThreatGPT, an AI assistant specialized in cybersecurity education and training. 
Your role is to generate realistic but educational threat simulation content for security awareness training.

IMPORTANT GUIDELINES:
- Generate educational content only - never provide actual attack instructions
- Focus on detection, prevention, and defensive measures
- Use placeholder/example data for any sensitive information
- Emphasize learning objectives and security best practices
- Keep content appropriate for professional security training environments
- Include specific indicators of compromise (IoCs) when relevant

For IT help desk impersonation scenarios, focus on:
- Social engineering tactics that employees should recognize
- Red flags and warning signs of impersonation attempts
- Verification procedures and security protocols
- Defensive training and awareness strategies"""
    
    # User prompt for IT help desk scenario
    user_prompt = """Target: Marketing Coordinator in Technology industry
Scenario: IT Help Desk Impersonation Attack
Stage: Social Engineering Phone Call Analysis

Generate educational content about IT help desk impersonation attacks, focusing on:
1. Common social engineering tactics used in these attacks
2. Warning signs employees should recognize
3. Proper verification procedures
4. Defensive recommendations for organizations

Keep content educational and appropriate for security awareness training."""
    
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        'max_tokens': 800,
        'temperature': 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=90)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    
                    print("✅ ThreatGPT content generation successful!")
                    print(f"Content length: {len(content)} characters")
                    print(f"Preview:\n{content[:400]}...")
                    
                    # Check if it looks like good educational content
                    good_indicators = [
                        'social engineering', 'security awareness', 'verification',
                        'warning signs', 'defensive', 'training', 'education'
                    ]
                    
                    content_lower = content.lower()
                    matches = sum(1 for indicator in good_indicators if indicator in content_lower)
                    
                    print(f"\n📊 Content quality: {matches}/{len(good_indicators)} educational indicators found")
                    
                    if matches >= 4:
                        print("🎉 Content looks suitable for ThreatGPT!")
                        return True
                    else:
                        print("⚠️ Content might need improvement")
                        return True  # Still working, just needs tuning
                        
                else:
                    text = await response.text()
                    print(f"❌ ThreatGPT test failed: {response.status} - {text}")
                    return False
                    
    except Exception as e:
        print(f"❌ ThreatGPT test error: {e}")
        return False

if __name__ == "__main__":
    working_model = asyncio.run(test_qwen_model())
    
    if working_model:
        print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        print("\n📝 Next steps:")
        print("1. Update ThreatGPT configuration to use this model")
        print("2. Run full simulation test with IT help desk scenario")
        print("3. Verify complete logging workflow")
    else:
        print("\n💡 Troubleshooting suggestions:")
        print("1. Check if the exact model name in web UI matches API")
        print("2. Try copying the exact request from web UI network tab")
        print("3. Verify OpenRouter account has API access enabled")