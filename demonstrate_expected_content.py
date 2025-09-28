#!/usr/bin/env python3
"""Show expected content types from different scenario templates."""

import asyncio
import os
from dotenv import load_dotenv
from src.threatgpt.llm.manager import LLMManager

load_dotenv()

async def demonstrate_expected_content():
    """Show what kind of content should be generated for different templates."""
    
    print("DEMONSTRATING EXPECTED CONTENT FROM TEMPLATES")
    print("=" * 60)
    
    # Setup LLM manager with working config
    config = {
        'openrouter': {
            'api_key': os.getenv('OPENROUTER_API_KEY'),
            'model': 'qwen/qwen3-vl-235b-a22b-thinking'
        }
    }
    
    llm_manager = LLMManager(config=config)
    
    # Test scenarios based on template analysis
    scenarios = [
        {
            'name': 'IT Help Desk Impersonation - Phone Script',
            'prompt': '''Generate a realistic phone script for IT Help Desk Impersonation training.

Target: Marketing Coordinator (mid-level, basic technical skills)
Attack: Phone call impersonating IT support requesting password reset
Goal: Educational security awareness training

Include:
1. Opening conversation (professional, authoritative tone)
2. Information gathering questions
3. Urgency building techniques  
4. Red flags employees should notice
5. Proper response procedures

Make it educational with clear "WARNING SIGNS" sections.''',
            'expected_format': 'Phone script with dialogue, red flags, and defensive training'
        },
        
        {
            'name': 'Executive Phishing - Email Content',
            'prompt': '''Generate an educational phishing email example for C-level executive training.

Target: CEO (high awareness, formal communication style)
Attack: Board meeting document sharing pretext
Goal: Security awareness training

Include:
1. Realistic email header (From, Subject, Date)
2. Professional business language
3. Document sharing request with urgency
4. Social engineering tactics used
5. Indicators of phishing attempt
6. Recommended verification steps

Make it educational with clear security analysis.''',
            'expected_format': 'Email with headers, body, and security analysis'
        },
        
        {
            'name': 'BEC Finance Attack - Scenario Walkthrough',
            'prompt': '''Generate a Business Email Compromise scenario for finance team training.

Target: Finance Manager (experienced, handles wire transfers)
Attack: CEO impersonation requesting urgent payment
Goal: BEC awareness and prevention training

Include:
1. Attack timeline and stages
2. Social engineering techniques
3. Financial process exploitation
4. Warning signs and red flags
5. Verification procedures
6. Recovery steps if compromised

Make it educational with step-by-step analysis.''',
            'expected_format': 'Multi-stage attack scenario with defensive guidance'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nSCENARIO {i}: {scenario['name']}")
        print(f"Expected Format: {scenario['expected_format']}")
        print("-" * 50)
        
        try:
            result = await llm_manager.generate_content(
                prompt=scenario['prompt'],
                scenario_type="threat_simulation_reconnaissance",
                max_tokens=800,
                temperature=0.7
            )
            
            if result and result.content:
                print(f"Generated {len(result.content)} characters")
                print(f"Content Preview:")
                print(result.content[:400] + "..." if len(result.content) > 400 else result.content)
            else:
                print("No content generated")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(demonstrate_expected_content())