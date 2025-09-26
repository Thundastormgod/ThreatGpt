#!/usr/bin/env python3
"""Content Extraction Tool - Extract AI-generated content from simulation logs and organize it."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re

class ContentExtractor:
    """Extract and organize AI-generated content from simulation logs."""
    
    def __init__(self):
        self.base_path = Path("generated_content")
        self.logs_path = Path("logs/simulations/successful")
        self.content_stats = {
            "total_files": 0,
            "content_items": 0,
            "scenarios": 0,
            "phone_scripts": 0,
            "email_templates": 0,
            "training_materials": 0
        }
    
    def extract_all_content(self):
        """Extract content from all simulation log files."""
        print("🔍 EXTRACTING AI-GENERATED CONTENT FROM LOGS")
        print("=" * 60)
        
        if not self.logs_path.exists():
            print("❌ No simulation logs found!")
            return
        
        # Find all JSON log files
        log_files = list(self.logs_path.glob("*.json"))
        log_files = [f for f in log_files if not f.name.endswith('.meta.json')]
        
        print(f"Found {len(log_files)} simulation log files")
        
        for log_file in log_files:
            try:
                self.extract_from_file(log_file)
                self.content_stats["total_files"] += 1
            except Exception as e:
                print(f"❌ Error processing {log_file.name}: {str(e)}")
        
        self.save_index()
        self.print_summary()
    
    def extract_from_file(self, log_file: Path):
        """Extract content from a single log file."""
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        simulation_id = data.get("simulation_id", "unknown")
        scenario_name = data.get("scenario", {}).get("name", "Unknown Scenario")
        created_at = data.get("created_at", "")
        threat_type = data.get("scenario", {}).get("threat_type", "general")
        
        print(f"\n📄 Processing: {scenario_name} ({simulation_id[:8]}...)")
        
        # Extract generated content
        generated_content = data.get("generated_content", [])
        
        for i, content_item in enumerate(generated_content):
            content = content_item.get("content", "")
            content_type = content_item.get("content_type", "unknown")
            
            # Skip empty or placeholder content
            if not content or "Content generation unavailable" in content or len(content) < 100:
                continue
            
            # Determine content category and save appropriately
            self.save_content_item(
                content=content,
                scenario_name=scenario_name,
                threat_type=threat_type,
                simulation_id=simulation_id,
                created_at=created_at,
                content_type=content_type,
                item_index=i
            )
            
            self.content_stats["content_items"] += 1
    
    def save_content_item(self, content: str, scenario_name: str, threat_type: str, 
                         simulation_id: str, created_at: str, content_type: str, item_index: int):
        """Save individual content item to appropriate folder."""
        
        # Clean scenario name for filename
        clean_scenario = re.sub(r'[<>:"/\\|?*]', '_', scenario_name)
        timestamp = created_at.split('T')[0] if 'T' in created_at else created_at[:10]
        
        # Determine folder and filename based on content analysis
        folder, category = self.categorize_content(content, threat_type)
        filename = f"{timestamp}_{clean_scenario}_{simulation_id[:8]}_{item_index:02d}.md"
        
        file_path = self.base_path / folder / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create markdown file with metadata
        md_content = self.create_markdown_content(
            content, scenario_name, threat_type, simulation_id, created_at, content_type, category
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"  ✅ Saved {category}: {filename}")
        self.content_stats[category.lower().replace(' ', '_')] += 1
    
    def categorize_content(self, content: str, threat_type: str) -> tuple:
        """Categorize content based on its type and content."""
        content_lower = content.lower()
        
        if "phone" in content_lower and ("script" in content_lower or "call" in content_lower):
            return "phone_scripts", "Phone Scripts"
        elif "email" in content_lower and ("subject:" in content_lower or "from:" in content_lower):
            return "email_templates", "Email Templates"
        elif "training" in content_lower or "awareness" in content_lower or "educational" in content_lower:
            return "training_materials", "Training Materials"
        elif threat_type in ["spear_phishing", "phishing"]:
            return "email_templates", "Email Templates"
        elif threat_type in ["social_engineering"] and "phone" in content_lower:
            return "phone_scripts", "Phone Scripts"
        else:
            return "scenarios", "Scenarios"
    
    def create_markdown_content(self, content: str, scenario_name: str, threat_type: str,
                              simulation_id: str, created_at: str, content_type: str, category: str) -> str:
        """Create formatted markdown content with metadata."""
        
        return f"""# {scenario_name}

## Metadata
- **Category**: {category}
- **Threat Type**: {threat_type}
- **Content Type**: {content_type}
- **Simulation ID**: {simulation_id}
- **Generated**: {created_at}
- **Extracted**: {datetime.now().isoformat()}

---

## Generated Content

{content}

---

*This content was generated by ThreatGPT for educational cybersecurity training purposes.*
"""
    
    def save_index(self):
        """Save content index for easy browsing."""
        index_data = {
            "extraction_timestamp": datetime.now().isoformat(),
            "statistics": self.content_stats,
            "folders": {
                "scenarios": "General threat scenarios and attack walkthroughs",
                "phone_scripts": "Social engineering phone call scripts",
                "email_templates": "Phishing and spear-phishing email examples",
                "training_materials": "Security awareness training content",
                "reports": "Analysis and summary reports"
            }
        }
        
        index_file = self.base_path / "content_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        # Also create a README
        readme_content = f"""# ThreatGPT Generated Content

This folder contains AI-generated cybersecurity training content organized by category.

## Statistics
- **Total Simulations Processed**: {self.content_stats['total_files']}
- **Content Items Extracted**: {self.content_stats['content_items']}

## Folder Structure

### 📞 phone_scripts/
Social engineering phone call scripts for training purposes.
- IT help desk impersonation calls
- Executive impersonation scenarios
- Technical support scams

### 📧 email_templates/
Phishing and spear-phishing email examples.
- Executive spear-phishing campaigns
- Business email compromise (BEC) templates
- Credential harvesting emails

### 🎯 scenarios/
Complete threat scenarios and attack walkthroughs.
- Multi-stage attack scenarios
- Reconnaissance and planning phases
- Post-exploitation activities

### 📚 training_materials/
Security awareness training content.
- Warning signs and red flags
- Defensive procedures
- Incident response guides

### 📊 reports/
Analysis reports and summaries.
- Threat landscape analysis
- Training effectiveness reports
- Security recommendations

## Usage

All content is saved in Markdown format with metadata headers for easy reading and integration into training programs.

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_file = self.base_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def print_summary(self):
        """Print extraction summary."""
        print(f"\n📊 CONTENT EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"✅ Processed {self.content_stats['total_files']} simulation files")
        print(f"📝 Extracted {self.content_stats['content_items']} content items")
        print(f"📞 Phone Scripts: {self.content_stats['phone_scripts']}")
        print(f"📧 Email Templates: {self.content_stats['email_templates']}")
        print(f"🎯 Scenarios: {self.content_stats['scenarios']}")
        print(f"📚 Training Materials: {self.content_stats['training_materials']}")
        print(f"\n💾 Content saved to: generated_content/")
        print(f"📋 Browse index: generated_content/README.md")

def main():
    """Run content extraction."""
    extractor = ContentExtractor()
    extractor.extract_all_content()

if __name__ == "__main__":
    main()