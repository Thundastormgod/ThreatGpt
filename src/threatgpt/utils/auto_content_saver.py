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
        
        # Extract data from SimulationOutput format
        simulation_id = simulation_data.get("simulation_id", "unknown") 
        scenario_metadata = simulation_data.get("scenario", {})
        scenario_name = scenario_metadata.get("name", "Unknown Scenario")
        threat_type = scenario_metadata.get("threat_type", "general")
        
        # Handle created_at - it might be a datetime object or string
        created_at_raw = simulation_data.get("created_at", datetime.now())
        if isinstance(created_at_raw, datetime):
            created_at = created_at_raw.isoformat()
        else:
            created_at = str(created_at_raw)
        
        # Handle both old format and new ContentGeneration format
        generated_content = simulation_data.get("generated_content", [])
        
        for i, content_item in enumerate(generated_content):
            # Handle new ContentGeneration format
            if isinstance(content_item, dict):
                content = content_item.get("content", "")
                content_type = content_item.get("content_type", "unknown")
                provider_info = content_item.get("provider_info", {})
                provider_name = provider_info.get("name", "unknown") if provider_info else "unknown"
                
                # Handle generated_at - it might be a datetime object or string
                generated_at_raw = content_item.get("generated_at", created_at)
                if isinstance(generated_at_raw, datetime):
                    generated_at = generated_at_raw.isoformat()
                else:
                    generated_at = str(generated_at_raw)
            else:
                # Handle legacy format
                content = str(content_item) if content_item else ""
                content_type = "unknown"
                provider_name = "unknown"
                generated_at = created_at
            
            # Skip empty, placeholder, or fallback content
            if not content or "Content generation unavailable" in content or len(content) < 100:
                continue
                
            # Skip obvious fallback content
            if "This is a simulated response" in content or "Fallback content" in content:
                continue
            
            # Only save if it appears to be real AI content
            if self._appears_to_be_real_ai_content(content):
                filename = self.save_content_item(
                    content=content,
                    scenario_name=scenario_name,
                    threat_type=threat_type,
                    simulation_id=simulation_id,
                    created_at=generated_at,
                    content_type=content_type,
                    item_index=i,
                    provider_name=provider_name
                )
                
                if filename:
                    saved_files.append(str(filename))
        
        return saved_files
    
    def _appears_to_be_real_ai_content(self, content: str) -> bool:
        """Check if content appears to be real AI-generated content."""
        # Length check - real AI content is usually substantial
        if len(content) < 150:
            return False
        
        # Check for fallback indicators
        fallback_indicators = [
            "Content generation unavailable",
            "This is a simulated response",
            "Fallback content",
            "Unable to generate",
            "Error generating content",
            "[FALLBACK]",
            "Mock response",
            "placeholder response",
            "content not available"
        ]
        
        content_lower = content.lower()
        for indicator in fallback_indicators:
            if indicator.lower() in content_lower:
                return False
        
        # Check for structured, educational AI content characteristics
        ai_indicators = [
            # Email/communication patterns
            "subject:", "dear ", "from:", "to:", "hello", "thank you", "please",
            # Educational/training content patterns  
            "## ", "### ", "**", "*", "scenario", "training", "simulation", "educational",
            "overview", "example", "analysis", "recommendations", "defensive", "security",
            # Structured content patterns
            "stage", "step", "phase", "technique", "tactic", "methodology", "approach",
            # Professional writing patterns
            "however", "therefore", "furthermore", "additionally", "consequently", "meanwhile",
            # Technical/cybersecurity content
            "threat", "attack", "vulnerability", "risk", "compromise", "breach", "exploit"
        ]
        
        indicator_count = sum(1 for indicator in ai_indicators if indicator in content_lower)
        
        # More lenient threshold - substantial structured content indicates real AI
        has_structure = any(marker in content for marker in ["## ", "### ", "**", "---", "```"])
        has_substance = len(content) > 1000  # Substantial content
        
        return (indicator_count >= 3) or (has_structure and has_substance)

    def save_content_item(self, content: str, scenario_name: str, threat_type: str,
                         simulation_id: str, created_at: str, content_type: str, 
                         item_index: int, provider_name: str = "unknown") -> Path:
        """Save individual content item."""
        
        # Clean scenario name for filename
        clean_scenario = re.sub(r'[<>:"/\\|?*]', '_', scenario_name)
        
        # Extract date for filename - handle both string and datetime objects
        if isinstance(created_at, datetime):
            timestamp = created_at.strftime("%Y-%m-%d")
        elif 'T' in str(created_at):
            timestamp = str(created_at).split('T')[0] 
        else:
            timestamp = str(created_at)[:10]
        
        # Determine folder and category
        folder, category = self.categorize_content(content, threat_type)
        filename = f"{timestamp}_{clean_scenario}_{simulation_id[:8]}_{item_index:02d}.md"
        
        file_path = self.content_dir / folder / filename
        
        # Create markdown content
        md_content = self.create_markdown_content(
            content, scenario_name, threat_type, simulation_id, created_at, content_type, category, provider_name
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Update content index
        self.update_content_index()
        
        return file_path
    
    def categorize_content(self, content: str, threat_type: str) -> tuple:
        """Categorize content based on its type and threat category."""
        content_lower = content.lower()
        
        # Prioritize actual scenario samples over training materials
        
        # Phone/Voice-based attacks
        if (threat_type.lower() in ["social_engineering", "vishing"] or 
            ("phone" in content_lower and ("script" in content_lower or "call" in content_lower or "conversation" in content_lower))):
            return "phone_scripts", "Phone Scripts"
        
        # Email-based attacks (phishing, BEC, spear-phishing)
        elif (threat_type.lower() in ["phishing", "spear_phishing", "bec", "business_email_compromise"] or
              ("email" in content_lower and ("subject:" in content_lower or "from:" in content_lower or "to:" in content_lower))):
            return "email_templates", "Email Templates"
        
        # SMS/Text-based attacks
        elif (threat_type.lower() in ["sms_phishing", "smishing"] or
              ("sms" in content_lower or "text message" in content_lower or "mobile" in content_lower)):
            return "scenarios", "SMS/Mobile Scenarios"
        
        # Attack planning and reconnaissance 
        elif ("reconnaissance" in content_lower or "attack plan" in content_lower or 
              "osint" in content_lower or "target profiling" in content_lower or
              "infrastructure setup" in content_lower):
            return "scenarios", "Attack Planning"
        
        # Generic threat scenarios
        elif any(keyword in content_lower for keyword in [
            "threat scenario", "attack method", "exploitation", "payload", 
            "social engineering", "pretext", "lure", "campaign"
        ]):
            return "scenarios", "Threat Scenarios"
        
        # Training/Educational content (fallback for educational materials)
        elif ("training" in content_lower or "awareness" in content_lower or 
              "educational" in content_lower or "simulation" in content_lower):
            return "training_materials", "Training Materials"
        
        # Analysis and reports
        elif ("analysis" in content_lower or "report" in content_lower or 
              "assessment" in content_lower or "findings" in content_lower):
            return "reports", "Analysis Reports"
        
        # Default categorization based on threat type
        else:
            if threat_type.lower() in ["phishing", "spear_phishing", "bec"]:
                return "email_templates", "Email Templates"
            elif threat_type.lower() in ["social_engineering", "vishing"]:
                return "phone_scripts", "Phone Scripts"
            elif threat_type.lower() in ["sms_phishing", "smishing"]:
                return "scenarios", "SMS Scenarios"
            else:
                return "scenarios", "General Scenarios"
    
    def update_content_index(self) -> None:
        """Update the content index with current statistics."""
        try:
            # Count files in each directory
            statistics = {
                "total_files": 0,
                "content_items": 0,
                "scenarios": 0,
                "phone_scripts": 0,
                "email_templates": 0,
                "training_materials": 0,
                "reports": 0
            }
            
            # Count files in each subdirectory
            for folder in ["scenarios", "phone_scripts", "email_templates", "training_materials", "reports"]:
                folder_path = self.content_dir / folder
                if folder_path.exists():
                    file_count = len(list(folder_path.glob("*.md")))
                    statistics[folder] = file_count
                    statistics["total_files"] += file_count
                    statistics["content_items"] += file_count
            
            # Create updated index
            index_data = {
                "extraction_timestamp": datetime.now().isoformat(),
                "statistics": statistics,
                "folders": {
                    "scenarios": "General threat scenarios and attack walkthroughs",
                    "phone_scripts": "Social engineering phone call scripts",
                    "email_templates": "Phishing and spear-phishing email examples",
                    "training_materials": "Security awareness training content",
                    "reports": "Analysis and summary reports"
                }
            }
            
            # Save updated index
            index_file = self.content_dir / "content_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2)
                
        except Exception as e:
            # Don't fail the whole operation if index update fails
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to update content index: {e}")
    
    def create_markdown_content(self, content: str, scenario_name: str, threat_type: str,
                              simulation_id: str, created_at: str, content_type: str, 
                              category: str, provider_name: str = "unknown") -> str:
        """Create formatted markdown content."""
        
        # Add real AI indicator emoji if it's from a real provider
        ai_indicator = "🤖 **Real AI Generated**" if provider_name != "fallback" else "🔄 Fallback Content"
        
        return f"""# {scenario_name}

## Metadata
- **Category**: {category}
- **Threat Type**: {threat_type}
- **Content Type**: {content_type}
- **AI Provider**: {provider_name}
- **Content Source**: {ai_indicator}
- **Simulation ID**: {simulation_id}
- **Generated**: {created_at}
- **Auto-Saved**: {datetime.now().isoformat()}

---

## Generated Content

{content}

---

*This content was automatically saved by ThreatGPT for educational cybersecurity training purposes.*
*Real AI content is marked with 🤖 to distinguish from fallback content.*
"""

# Global instance for easy access
auto_saver = AutoContentSaver()

def save_content_automatically(simulation_data: Dict[str, Any]) -> List[str]:
    """Convenience function to save content automatically."""
    return auto_saver.save_simulation_content(simulation_data)