#!/usr/bin/env python3
"""Test auto save with the problematic simulation data."""

import json
from src.threatgpt.utils.auto_content_saver import save_content_automatically

# Load the simulation that had the error
simulation_file = r"c:\Users\MY PC\OneDrive\Documents\ThreatGpt\logs\simulations\successful\20250928_104633_84ec1a91-b6ed-4aa8-b5b3-c10fc4e4ade5.json"

with open(simulation_file, 'r', encoding='utf-8') as f:
    simulation_data = json.load(f)

print("🔍 Testing auto content save with problematic data...")
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