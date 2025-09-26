#!/usr/bin/env python3
"""Auto Content Saver - Automatically save AI-generated content during simulations."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import re

class AutoContentSaver:
    """Automatically save and organize AI-generated content."""
    
    def __init__(self):
        self.content_dir = Path("generated_content")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure all content directories exist."""
        directories = [
            "scenarios",
            "phone_scripts", 
            "email_templates",
            "training_materials",
            "reports"
        ]
        
        for directory in directories:
            (self.content_dir / directory).mkdir(parents=True, exist_ok=True)
    
    def save_simulation_content(self, simulation_data: Dict[str, Any]) -> List[str]:
        """Save content from a simulation immediately after generation."""
        saved_files = []
        
        simulation_id = simulation_data.get("simulation_id", "unknown")
        scenario_name = simulation_data.get("scenario", {}).get("name", "Unknown Scenario")
        threat_type = simulation_data.get("scenario", {}).get("threat_type", "general")
        created_at = simulation_data.get("created_at", datetime.now().isoformat())
        
        generated_content = simulation_data.get("generated_content", [])
        
        for i, content_item in enumerate(generated_content):
            content = content_item.get("content", "")
            content_type = content_item.get("content_type", "unknown")
            
            # Skip empty or placeholder content
            if not content or "Content generation unavailable" in content or len(content) < 100:
                continue
            
            filename = self.save_content_item(
                content=content,
                scenario_name=scenario_name,
                threat_type=threat_type,
                simulation_id=simulation_id,
                created_at=created_at,
                content_type=content_type,
                item_index=i
            )
            
            if filename:
                saved_files.append(str(filename))
        
        return saved_files
    
    def save_content_item(self, content: str, scenario_name: str, threat_type: str,
                         simulation_id: str, created_at: str, content_type: str, item_index: int) -> Path:
        """Save individual content item."""
        
        # Clean scenario name for filename
        clean_scenario = re.sub(r'[<>:"/\\|?*]', '_', scenario_name)
        timestamp = created_at.split('T')[0] if 'T' in created_at else created_at[:10]
        
        # Determine folder and category
        folder, category = self.categorize_content(content, threat_type)
        filename = f"{timestamp}_{clean_scenario}_{simulation_id[:8]}_{item_index:02d}.md"
        
        file_path = self.content_dir / folder / filename
        
        # Create markdown content
        md_content = self.create_markdown_content(
            content, scenario_name, threat_type, simulation_id, created_at, content_type, category
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return file_path
    
    def categorize_content(self, content: str, threat_type: str) -> tuple:
        """Categorize content based on its type."""
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
        """Create formatted markdown content."""
        
        return f"""# {scenario_name}

## Metadata
- **Category**: {category}
- **Threat Type**: {threat_type}
- **Content Type**: {content_type}
- **Simulation ID**: {simulation_id}
- **Generated**: {created_at}
- **Auto-Saved**: {datetime.now().isoformat()}

---

## Generated Content

{content}

---

*This content was automatically saved by ThreatGPT for educational cybersecurity training purposes.*
"""

# Global instance for easy access
auto_saver = AutoContentSaver()

def save_content_automatically(simulation_data: Dict[str, Any]) -> List[str]:
    """Convenience function to save content automatically."""
    return auto_saver.save_simulation_content(simulation_data)