#!/usr/bin/env python3
"""Debug the AI content detection logic."""

import json
from src.threatgpt.utils.auto_content_saver import AutoContentSaver

# Load the simulation data
simulation_file = r"c:\Users\MY PC\OneDrive\Documents\ThreatGpt\logs\simulations\successful\20250928_091605_e8e37c90-c6f1-450c-bfb6-dc9a7cc754ff.json"

with open(simulation_file, 'r', encoding='utf-8') as f:
    simulation_data = json.load(f)

saver = AutoContentSaver()

print("🔍 Testing AI content detection logic...")

for i, content_item in enumerate(simulation_data.get('generated_content', [])):
    content = content_item.get('content', '')
    provider_name = content_item.get('provider_info', {}).get('name', 'unknown')
    
    print(f"\n--- Content Item {i} ---")
    print(f"Provider: {provider_name}")
    print(f"Length: {len(content)} characters")
    
    # Test the detection logic step by step
    appears_real = saver._appears_to_be_real_ai_content(content)
    print(f"Appears to be real AI: {appears_real}")
    
    # Check length
    length_ok = len(content) >= 150
    print(f"Length check (>= 150): {length_ok}")
    
    # Check for fallback indicators
    content_lower = content.lower()
    fallback_indicators = [
        "Content generation unavailable",
        "This is a simulated response",
        "Fallback content",
        "Unable to generate",
        "Error generating content",
        "[FALLBACK]",
        "Mock response"
    ]
    
    has_fallback = any(indicator.lower() in content_lower for indicator in fallback_indicators)
    print(f"Has fallback indicators: {has_fallback}")
    
    # Check AI indicators
    ai_indicators = [
        "subject:",  # Email format
        "dear ",     # Formal address
        "from:",     # Email header
        "hello",     # Greeting
        "urgent",    # Common phishing words
        "please",    # Polite language
        "thank you", # Courtesy
        "attached",  # Email context
    ]
    
    indicator_count = sum(1 for indicator in ai_indicators if indicator in content_lower)
    print(f"AI indicator count: {indicator_count} (need >= 2)")
    
    print(f"Found AI indicators: {[indicator for indicator in ai_indicators if indicator in content_lower]}")
    
    # Show first 300 characters
    print(f"First 300 chars:\n{content[:300]}...")