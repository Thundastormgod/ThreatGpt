#!/usr/bin/env python3
"""Debug script to test auto content saving functionality."""

import json
from src.threatgpt.utils.auto_content_saver import save_content_automatically

# Load the most recent simulation result
simulation_file = r"c:\Users\MY PC\OneDrive\Documents\ThreatGpt\logs\simulations\successful\20250928_091605_e8e37c90-c6f1-450c-bfb6-dc9a7cc754ff.json"

with open(simulation_file, 'r', encoding='utf-8') as f:
    simulation_data = json.load(f)

print("🔍 Testing auto content save functionality...")
print(f"📄 Simulation ID: {simulation_data.get('simulation_id', 'Unknown')}")
print(f"📝 Generated content items: {len(simulation_data.get('generated_content', []))}")

# Test the auto-save function
try:
    saved_files = save_content_automatically(simulation_data)
    print(f"✅ Auto-save result: {len(saved_files)} files saved")
    for file_path in saved_files:
        print(f"   → {file_path}")
except Exception as e:
    print(f"❌ Auto-save error: {e}")
    import traceback
    traceback.print_exc()

# Also check the content to see if it meets the criteria
print("\n🔍 Analyzing generated content:")
for i, content_item in enumerate(simulation_data.get('generated_content', [])):
    content = content_item.get('content', '')
    print(f"Item {i}:")
    print(f"  Length: {len(content)} characters")
    print(f"  Provider: {content_item.get('provider_info', {}).get('name', 'unknown')}")
    print(f"  First 100 chars: {content[:100]}...")
    print()