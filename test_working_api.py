#!/usr/bin/env python3
"""Test the working API key with full response"""

import requests
import json

def test_working_key():
    """Test the working API key and get full response"""
    
    api_key = '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'
    print(f"✅ Testing WORKING API key: {api_key[:25]}...")
    
    # Test with Qwen model
    print(f"\n🎯 Testing qwen/qwen3-vl-235b-a22b-thinking...")
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/threatgpt/threatgpt", 
                "X-Title": "ThreatGPT",
            },
            data=json.dumps({
                "model": "qwen/qwen3-vl-235b-a22b-thinking",
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello! Please respond with 'OpenRouter API is now working!'"
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
            print(f"Model used: {data.get('model', 'Unknown')}")
            
            # Now test with ThreatGPT threat simulation
            print(f"\n🚀 Testing threat simulation generation...")
            return test_threat_content(api_key)
            
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_threat_content(api_key: str):
    """Test threat simulation content generation"""
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/threatgpt/threatgpt",
                "X-Title": "ThreatGPT",
            },
            data=json.dumps({
                "model": "qwen/qwen3-vl-235b-a22b-thinking",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are ThreatGPT, specialized in cybersecurity education. Generate educational threat simulation content for security awareness training.

Focus on:
- Educational content only (no actual attack instructions)
- Detection and prevention strategies
- Warning signs and indicators of compromise
- Defensive recommendations"""
                    },
                    {
                        "role": "user", 
                        "content": """Generate educational content for IT Help Desk Impersonation attack simulation.

Target: Marketing Coordinator
Attack: Phone-based social engineering
Goal: Security awareness training

Include:
1. Attack techniques used
2. Warning signs to recognize
3. Verification procedures
4. Defensive measures

Make it educational and defense-focused."""
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.7
            })
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            print(f"✅ THREAT SIMULATION SUCCESS!")
            print(f"Generated {len(content)} characters")
            print(f"\nContent:\n{'-'*60}")
            print(content)
            print(f"{'-'*60}")
            
            return True
            
        else:
            print(f"❌ Threat simulation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_working_key()
    
    if success:
        print(f"\n🎉 OPENROUTER INTEGRATION WORKING!")
        print("✅ API calls successful")
        print("✅ Qwen model responding") 
        print("✅ Threat simulation content generated")
        print(f"\n🚀 READY FOR NEXT PHASE - Full ThreatGPT simulation!")
    else:
        print(f"\n❌ Still having issues")