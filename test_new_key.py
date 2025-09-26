#!/usr/bin/env python3
"""Test the updated OpenRouter API key with Qwen model"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_new_api_key():
    """Test the updated API key with focus on Qwen model"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return False
    
    print(f"✅ Testing NEW API key: {api_key[:20]}...")
    
    # Focus on your preferred Qwen model first
    models_to_test = [
        "qwen/qwen3-vl-235b-a22b-thinking",
        "qwen/qwen-2.5-72b-instruct",
        "openai/gpt-4o-mini"
    ]
    
    for model in models_to_test:
        print(f"\n🎯 Testing {model}...")
        
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
                            "content": "Hello! Please respond with 'API connection successful with Qwen!'"
                        }
                    ],
                    "max_tokens": 50,
                    "temperature": 0.1
                })
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                print(f"✅ SUCCESS! Response: {content}")
                print(f"Model used: {data.get('model', model)}")
                
                # Test with actual ThreatGPT prompt immediately
                print(f"\n🚀 Testing {model} with ThreatGPT threat simulation...")
                return test_threat_simulation(model, api_key)
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                error_msg = error_data.get('error', {}).get('message', error_data.get('error', 'Unknown'))
                print(f"❌ Error: {error_msg}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return False

def test_threat_simulation(model: str, api_key: str):
    """Test the working model with actual threat simulation content"""
    
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
                        "content": """You are ThreatGPT, an AI assistant specialized in cybersecurity education and training. Generate educational threat simulation content for security awareness training.

GUIDELINES:
- Generate educational content only - never actual attack instructions
- Focus on detection, prevention, and defensive measures  
- Include specific indicators of compromise (IoCs)
- Provide defensive recommendations
- Keep content appropriate for professional security training"""
                    },
                    {
                        "role": "user",
                        "content": """Generate educational content for an IT Help Desk Impersonation social engineering attack simulation.

Target: Marketing Coordinator in Technology industry
Attack Type: Phone-based social engineering impersonation
Focus: Security awareness training content

Generate a detailed analysis covering:
1. Attack techniques and social engineering tactics
2. Warning signs employees should recognize
3. Proper verification procedures
4. Defensive recommendations and training points

Make it educational and focused on defense/detection."""
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            })
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            print(f"✅ THREAT SIMULATION SUCCESS!")
            print(f"Generated {len(content)} characters of content")
            print(f"Content preview:\n{'-'*50}")
            print(content[:500] + "...")
            print(f"{'-'*50}")
            
            # Save the working model info
            config = {
                "working_model": model,
                "api_key_format": "Bearer token",
                "content_length": len(content),
                "status": "WORKING"
            }
            
            with open('working_model.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"\n🎉 OpenRouter integration WORKING with model: {model}")
            print("✅ Ready for full ThreatGPT simulation!")
            return True
            
        else:
            print(f"❌ Threat simulation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Threat simulation error: {e}")
        return False

if __name__ == "__main__":
    success = test_new_api_key()
    
    if success:
        print(f"\n🚀 READY FOR NEXT PHASE!")
        print("OpenRouter API calls are working and generating threat simulation content")
        print("You can now run full ThreatGPT simulations with the working model")
    else:
        print(f"\n❌ API calls still not working")
        print("Check OpenRouter dashboard for account status and billing setup")