#!/usr/bin/env python3
"""Test script for OpenRouter API"""

from dotenv import load_dotenv
import httpx
import os
import json

# Load environment variables
load_dotenv()

def test_openrouter_api():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test models endpoint
    print("\n🔍 Testing models endpoint...")
    try:
        response = httpx.get("https://openrouter.ai/api/v1/models", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"Found {len(models.get('data', []))} models")
            for model in models.get('data', [])[:3]:
                print(f"  - {model.get('id', 'Unknown')}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
    
    # Test chat completion
    print("\n🔍 Testing chat completion...")
    try:
        data = {
            "model": "anthropic/claude-3-haiku-20240307",
            "messages": [
                {"role": "user", "content": "Say hello in one word"}
            ],
            "max_tokens": 10
        }
        
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30.0
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ Response: {content}")
        else:
            print(f"❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Chat completion error: {e}")

if __name__ == "__main__":
    test_openrouter_api()