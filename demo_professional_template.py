#!/usr/bin/env python3
"""
Demo script for ThreatGPT Professional Template Creation.
Demonstrates automated template creation without user interaction.
"""

from pathlib import Path
from datetime import datetime
import yaml

from src.threatgpt.core.template_manager_pro import TemplateCreationWizard


def create_demo_template():
    """Create a demonstration template programmatically."""
    
    print("🎯 ThreatGPT Professional Template Creation Demo")
    print("=" * 50)
    
    # Initialize wizard
    templates_dir = Path("templates")
    wizard = TemplateCreationWizard(templates_dir)
    
    # Pre-populate template data (simulating wizard interaction)
    wizard.current_template = {
        "metadata": {
            "name": "Professional Demo: Advanced Phishing Campaign",
            "description": "Demonstration of professional template creation with multi-vector attack simulation targeting financial executives",
            "author": "ThreatGPT Professional System",
            "version": "1.0.0",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "tags": ["demo", "phishing", "executive", "financial", "multi-vector"],
            "references": [
                "https://attack.mitre.org/techniques/T1566/001/",
                "https://www.sans.org/white-papers/executive-phishing/"
            ]
        },
        
        "threat_type": "spear_phishing",
        "delivery_vector": "email",
        
        "target_profile": {
            "role": "Chief Financial Officer",
            "seniority": "executive",
            "department": "Finance",
            "technical_level": "moderate",
            "industry": "financial_services", 
            "company_size": "large",
            "typical_working_hours": "8:00-18:00",
            "communication_style": "formal_professional",
            "security_awareness_level": 7,
            "interests": ["financial_reporting", "compliance", "risk_management"],
            "social_media_presence": {
                "linkedin": "active_professional",
                "twitter": "minimal"
            }
        },
        
        "behavioral_pattern": {
            "mitre_attack_techniques": ["T1566.001", "T1566.002", "T1598.003"],
            "mitre_attack_tactics": ["Initial Access", "Credential Access"],
            "psychological_triggers": ["authority", "urgency", "fear"],
            "social_engineering_tactics": ["pretexting", "impersonation", "authority_abuse"],
            "technical_methods": ["email_spoofing", "domain_typosquatting"],
            "evasion_techniques": ["sandbox_evasion", "reputation_exploitation"]
        },
        
        "difficulty_level": 8,
        "estimated_duration": 45,
        
        "simulation_parameters": {
            "max_iterations": 4,
            "max_duration_minutes": 90,
            "escalation_enabled": True,
            "response_adaptation": True,
            "time_pressure_simulation": True,
            "multi_stage_attack": True,
            "persistence_simulation": False,
            "language": "en",
            "tone": "urgent_professional",
            "urgency_level": 8,
            "compliance_mode": True,
            "content_filtering": True,
            "audit_logging": True
        },
        
        "custom_parameters": {
            "demo_mode": True,
            "creation_method": "automated",
            "validation_notes": "Created via professional template system demo"
        }
    }
    
    print("✨ Template data prepared")
    print(f"📝 Name: {wizard.current_template['metadata']['name']}")
    print(f"🎯 Threat Type: {wizard.current_template['threat_type']}")
    print(f"📊 Difficulty: {wizard.current_template['difficulty_level']}/10")
    
    # Validate template
    print("\n🔍 Validating template...")
    try:
        from src.threatgpt.config.models import ThreatScenario
        from pydantic import ValidationError
        
        validated_scenario = ThreatScenario.model_validate(wizard.current_template)
        print("✅ Template validation successful!")
        
        # Save template
        safe_name = "professional_demo_advanced_phishing"
        filename = f"{safe_name}.yaml"
        file_path = templates_dir / filename
        
        templates_dir.mkdir(exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# ThreatGPT Professional Template - Demo Creation\n")
            f.write(f"# Generated via Professional Template System on {datetime.utcnow().isoformat()}Z\n")
            f.write("# This template demonstrates the full capabilities of the professional creation system\n\n")
            yaml.dump(wizard.current_template, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Template saved: {file_path}")
        
        # Display summary
        print(f"\n📊 Professional Template Creation Summary:")
        print(f"   📁 File: {filename}")
        print(f"   🎯 Threat Type: {validated_scenario.threat_type}")
        print(f"   📧 Delivery: {validated_scenario.delivery_vector}")
        print(f"   👤 Target: {validated_scenario.target_profile.role}")
        print(f"   🏢 Industry: {validated_scenario.target_profile.industry}")
        print(f"   📊 Difficulty: {validated_scenario.difficulty_level}/10")
        print(f"   ⏱️ Duration: {validated_scenario.estimated_duration} minutes")
        print(f"   🔐 MITRE Techniques: {', '.join(validated_scenario.behavioral_pattern.mitre_attack_techniques)}")
        
        return file_path
        
    except ValidationError as e:
        print("❌ Template validation failed:")
        for error in e.errors():
            print(f"  - {error['loc'][0] if error['loc'] else 'root'}: {error['msg']}")
        return None
    except Exception as e:
        print(f"❌ Error creating template: {e}")
        return None


if __name__ == "__main__":
    result = create_demo_template()
    if result:
        print(f"\n🎉 Professional template creation demo completed successfully!")
        print(f"🚀 The ThreatGPT Professional Template Management System is fully operational!")
    else:
        print(f"\n❌ Demo failed. Please check the error messages above.")