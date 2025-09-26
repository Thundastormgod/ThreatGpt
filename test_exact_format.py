#!/usr/bin/env python3
"""Test OpenRouter using the exact format from documentation"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_openrouter_exact_format():
    """Test using the exact OpenRouter documentation format"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return False
    
    print(f"✅ Testing with exact OpenRouter format, API key: {api_key[:20]}...")
    
    # Test with your preferred Qwen model
    models_to_test = [
        "qwen/qwen3-vl-235b-a22b-thinking",
        "qwen/qwen-2.5-72b-instruct", 
        "openai/gpt-4o-mini",
        "anthropic/claude-3-haiku-20240307"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/threatgpt/threatgpt",
                    "X-Title": "ThreatGPT",
                },
                data=json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Hello! Please respond with just 'Hello from OpenRouter!'"
                        }
                    ],
                    "max_tokens": 50,
                    "temperature": 0.1
                })
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                print(f"✅ SUCCESS! Response: {content}")
                print(f"Model used: {data.get('model', 'Unknown')}")
                
                # Test with ThreatGPT content
                if test_threatgpt_content(model, api_key):
                    return model
                    
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                    print(f"❌ Error: {error_msg}")
                except:
                    print(f"❌ Error: {response.text}")
                    
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    return False

def test_threatgpt_content(model: str, api_key: str):
    """Test the working model with ThreatGPT content"""
    
    print(f"\n🎯 Testing {model} with ThreatGPT IT help desk scenario...")
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/threatgpt/threatgpt",
                "X-Title": "ThreatGPT",
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": """You are ThreatGPT, an AI assistant specialized in cybersecurity education and training. 
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
                    },
                    {
                        "role": "user",
                        "content": """Target: Marketing Coordinator in Technology industry
Scenario: IT Help Desk Impersonation Attack
Stage: Social Engineering Analysis

Generate educational content about IT help desk impersonation attacks for security awareness training, including:

1. **Common Attack Techniques**: How attackers impersonate IT staff
2. **Warning Signs**: Red flags employees should recognize
3. **Verification Procedures**: How to properly verify IT requests
4. **Defensive Recommendations**: Organizational security measures

Focus on educational value and defensive awareness. Use placeholder data and emphasize detection methods."""
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.7
            })
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            print("✅ ThreatGPT content generation successful!")
            print(f"Content length: {len(content)} chars")
            print(f"Content preview:\n{content[:400]}...")
            
            # Check content quality
            educational_keywords = [
                'security awareness', 'warning signs', 'verification', 
                'defensive', 'training', 'red flags', 'impersonation'
            ]
            
            content_lower = content.lower()
            keyword_matches = sum(1 for keyword in educational_keywords if keyword in content_lower)
            
            print(f"\n📊 Educational content quality: {keyword_matches}/{len(educational_keywords)} keywords found")
            
            if keyword_matches >= 4:
                print("🎉 Content quality is excellent for ThreatGPT!")
                return True
            else:
                print("⚠️ Content quality could be improved but model is working")
                return True
                
        else:
            print(f"❌ ThreatGPT test failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ThreatGPT test error: {e}")
        return False

if __name__ == "__main__":
    working_model = test_openrouter_exact_format()
    
    if working_model:
        print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        print(f"\n📝 Ready to configure ThreatGPT with this model!")
        
        # Save working configuration
        config = {
            "working_model": working_model,
            "api_format": "requests_with_json_dumps",
            "headers": {
                "Authorization": "Bearer <API_KEY>",
                "HTTP-Referer": "https://github.com/threatgpt/threatgpt",
                "X-Title": "ThreatGPT"
            },
            "endpoint": "https://openrouter.ai/api/v1/chat/completions"
        }
        
        with open('openrouter_working_config.json', 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✅ Saved working config to openrouter_working_config.json")
        
    else:
        print(f"\n❌ Still not working. Please check:")
        print("1. API key is correct and active")
        print("2. Account has billing/payment method set up")
        print("3. Account email is verified")
        print("4. Try generating a new API key in OpenRouter dashboard")