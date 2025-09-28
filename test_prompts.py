#!/usr/bin/env python3
"""Test script to verify the new prompt generation methods."""

import asyncio
from src.threatgpt.core.simulator import ThreatSimulator
from src.threatgpt.core.models import ThreatScenario

async def test_prompt_generation():
    # Create scenario
    scenario = ThreatScenario(
        name='Test SMS Phishing',
        description='Test scenario for SMS phishing',
        threat_type='sms_phishing'
    )
    
    # Create simulator (without LLM to just test prompts)
    simulator = ThreatSimulator(llm_provider=None)
    
    # Test different prompt generation methods
    print("Testing prompt generation methods...")
    
    # Test reconnaissance prompt
    recon_prompt = simulator._create_scenario_generation_prompt(scenario, "reconnaissance", "Information gathering phase")
    print(f"\n--- RECONNAISSANCE PROMPT ---")
    print(recon_prompt[:500] + "..." if len(recon_prompt) > 500 else recon_prompt)
    
    # Test attack planning prompt
    attack_prompt = simulator._create_scenario_generation_prompt(scenario, "attack_planning", "Attack execution phase")
    print(f"\n--- ATTACK PLANNING PROMPT ---")
    print(attack_prompt[:500] + "..." if len(attack_prompt) > 500 else attack_prompt)
    
    # Test SMS phishing specific prompt
    sms_prompt = simulator._create_phishing_sample_prompt(scenario, "Test scenario context", "sms_generation")
    print(f"\n--- SMS PHISHING PROMPT ---")
    print(sms_prompt[:500] + "..." if len(sms_prompt) > 500 else sms_prompt)

if __name__ == "__main__":
    asyncio.run(test_prompt_generation())