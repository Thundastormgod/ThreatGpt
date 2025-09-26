#!/usr/bin/env python3
"""Test OpenRouter chat completions with detailed debugging."""

import requests
import json
import os

def test_openrouter_chat():
    api_key = os.getenv("OPENROUTER_API_KEY", "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")
    
    print("🧪 Testing OpenRouter Chat Completions API...")
    print(f"🔑 API Key: {api_key[:25]}...")
    
    # Test with the exact headers and payload the OpenRouter provider uses
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/threatgpt/threatgpt',
        'X-Title': 'ThreatGPT'
    }
    
    payload = {
        'model': 'qwen/qwen3-vl-235b-a22b-thinking',
        'messages': [
            {
                'role': 'system',
                'content': 'You are ThreatGPT, an AI assistant specialized in cybersecurity education.'
            },
            {
                'role': 'user', 
                'content': 'Generate a brief test response to confirm the API is working.'
            }
        ],
        'max_tokens': 100,
        'temperature': 0.7,
        'stream': False
    }
    
    print("📤 Making request to chat/completions...")
    print("🎯 Model:", payload['model'])
    print("📋 Headers:")
    for key, value in headers.items():
        if key == 'Authorization':
            print(f"   {key}: Bearer {value[7:32]}...")
        else:
            print(f"   {key}: {value}")
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📨 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"🎉 Generated: {len(data['choices'][0]['message']['content'])} characters")
            print(f"📝 Content: {data['choices'][0]['message']['content'][:200]}...")
            print(f"🤖 Model used: {data.get('model', 'unknown')}")
            if 'usage' in data:
                print(f"💰 Token usage: {data['usage']}")
        else:
            print("❌ FAILED!")
            print(f"💥 Error response: {response.text}")
            
            # Try to parse JSON error
            try:
                error_data = response.json()
                print(f"🔍 Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("🔍 Raw error text:", response.text)
                
    except Exception as e:
        print(f"💥 Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openrouter_chat()