"""Template fixing utility for ThreatGPT templates.

Automatically fixes common validation issues in templates while preserving functionality.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class TemplateFixer:
    """Fixes common template validation issues."""
    
    THREAT_TYPE_MAPPINGS = {
        "hybrid_attack": "advanced_persistent_threat",
        "multi_vector": "advanced_persistent_threat", 
        "healthcare_targeted_attack": "spear_phishing",
        "multi_channel": "phishing",
        "supply_chain": "advanced_persistent_threat"
    }
    
    DELIVERY_VECTOR_MAPPINGS = {
        "multi_channel": "email",
        "multi_vector": "email",
        "mixed": "email"
    }
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.fixes_applied = []
    
    def fix_all_templates(self) -> Dict[str, Any]:
        """Fix all templates in the directory."""
        results = {
            "fixed": [],
            "failed": [],
            "skipped": [],
            "total_fixes": 0
        }
        
        template_files = list(self.templates_dir.glob("*.yaml")) + list(self.templates_dir.glob("*.yml"))
        
        for template_file in template_files:
            try:
                fixes = self.fix_template(template_file)
                if fixes:
                    results["fixed"].append({
                        "file": template_file.name,
                        "fixes": fixes
                    })
                    results["total_fixes"] += len(fixes)
                else:
                    results["skipped"].append(template_file.name)
            except Exception as e:
                results["failed"].append({
                    "file": template_file.name,
                    "error": str(e)
                })
        
        return results
    
    def fix_template(self, template_file: Path) -> List[str]:
        """Fix a single template file."""
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            template_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise Exception(f"YAML parsing error: {e}")
        
        fixes = []
        
        # Fix threat_type
        if "threat_type" in template_data:
            original = template_data["threat_type"]
            if original in self.THREAT_TYPE_MAPPINGS:
                template_data["threat_type"] = self.THREAT_TYPE_MAPPINGS[original]
                fixes.append(f"threat_type: {original} → {self.THREAT_TYPE_MAPPINGS[original]}")
        
        # Fix delivery_vector
        if "delivery_vector" in template_data:
            original = template_data["delivery_vector"]
            if original in self.DELIVERY_VECTOR_MAPPINGS:
                template_data["delivery_vector"] = self.DELIVERY_VECTOR_MAPPINGS[original]
                fixes.append(f"delivery_vector: {original} → {self.DELIVERY_VECTOR_MAPPINGS[original]}")
        
        # Fix difficulty_level (ensure it's an integer)
        if "difficulty_level" in template_data:
            try:
                difficulty = template_data["difficulty_level"]
                if isinstance(difficulty, str):
                    template_data["difficulty_level"] = int(difficulty)
                    fixes.append("difficulty_level: converted string to integer")
            except (ValueError, TypeError):
                template_data["difficulty_level"] = 5
                fixes.append("difficulty_level: set default value of 5")
        
        # Fix estimated_duration
        if "estimated_duration" in template_data:
            try:
                duration = template_data["estimated_duration"]
                if isinstance(duration, str):
                    # Extract number from strings like "30 minutes", "1 hour"
                    import re
                    numbers = re.findall(r'\d+', duration)
                    if numbers:
                        template_data["estimated_duration"] = int(numbers[0])
                        fixes.append("estimated_duration: extracted number from string")
            except (ValueError, TypeError):
                template_data["estimated_duration"] = 30
                fixes.append("estimated_duration: set default value of 30")
        
        # Fix simulation_parameters
        if "simulation_parameters" in template_data:
            sim_params = template_data["simulation_parameters"]
            
            # Convert string numbers to integers
            for param in ["max_iterations", "max_duration_minutes", "urgency_level"]:
                if param in sim_params and isinstance(sim_params[param], str):
                    try:
                        sim_params[param] = int(sim_params[param])
                        fixes.append(f"simulation_parameters.{param}: converted to integer")
                    except ValueError:
                        defaults = {"max_iterations": 3, "max_duration_minutes": 60, "urgency_level": 5}
                        sim_params[param] = defaults.get(param, 1)
                        fixes.append(f"simulation_parameters.{param}: set default value")
            
            # Ensure boolean values are correct
            for param in ["escalation_enabled", "response_adaptation", "compliance_mode", "content_filtering", "audit_logging"]:
                if param in sim_params and isinstance(sim_params[param], str):
                    sim_params[param] = sim_params[param].lower() in ("true", "yes", "1", "on")
                    fixes.append(f"simulation_parameters.{param}: converted to boolean")
        
        # Remove unsupported fields that cause validation errors
        unsupported_fields = [
            "success_metrics", "compliance_controls", "post_simulation_analysis",
            "escalation_triggers", "adaptation_rules", "variable_definitions",
            "template_variables", "dynamic_content"
        ]
        
        for field in unsupported_fields:
            if field in template_data:
                del template_data[field]
                fixes.append(f"removed unsupported field: {field}")
        
        # Ensure required metadata fields exist
        if "metadata" not in template_data:
            template_data["metadata"] = {}
            fixes.append("added missing metadata section")
        
        metadata = template_data["metadata"]
        
        # Fix metadata fields
        required_metadata = {
            "name": template_file.stem.replace('_', ' ').title(),
            "description": "Threat scenario template",
            "version": "1.0.0",
            "author": "ThreatGPT",
            "tags": [],
            "references": []
        }
        
        for key, default_value in required_metadata.items():
            if key not in metadata:
                metadata[key] = default_value
                fixes.append(f"added missing metadata.{key}")
        
        # Add timestamps if missing
        if "created_at" not in metadata or "updated_at" not in metadata:
            from datetime import datetime
            timestamp = datetime.utcnow().isoformat() + "Z"
            if "created_at" not in metadata:
                metadata["created_at"] = timestamp
                fixes.append("added metadata.created_at")
            if "updated_at" not in metadata:
                metadata["updated_at"] = timestamp
                fixes.append("added metadata.updated_at")
        
        # Ensure target_profile has required structure
        if "target_profile" in template_data:
            target = template_data["target_profile"]
            
            # Fix seniority level
            if "seniority" in target and target["seniority"] not in ["junior", "mid", "senior", "executive"]:
                target["seniority"] = "mid"
                fixes.append("target_profile.seniority: set to valid value")
            
            # Fix technical level
            if "technical_level" in target and target["technical_level"] not in ["low", "moderate", "high", "expert"]:
                target["technical_level"] = "moderate"
                fixes.append("target_profile.technical_level: set to valid value")
            
            # Fix industry
            valid_industries = [
                "technology", "finance", "healthcare", "government", "education",
                "retail", "manufacturing", "energy", "telecommunications", "other"
            ]
            if "industry" in target and target["industry"] not in valid_industries:
                target["industry"] = "technology"
                fixes.append("target_profile.industry: set to valid value")
            
            # Fix company_size
            if "company_size" in target and target["company_size"] not in ["startup", "small", "medium", "large", "enterprise"]:
                target["company_size"] = "medium"
                fixes.append("target_profile.company_size: set to valid value")
        
        # Only save if fixes were applied
        if fixes:
            # Create backup
            backup_path = template_file.with_suffix(f".backup.{int(__import__('time').time())}.yaml")
            import shutil
            shutil.copy2(template_file, backup_path)
            
            # Save fixed version
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write("# ThreatGPT Threat Scenario Template\n")
                f.write(f"# Auto-fixed on {__import__('datetime').datetime.utcnow().isoformat()}Z\n")
                f.write(f"# Fixes applied: {', '.join(fixes)}\n\n")
                yaml.dump(template_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        return fixes


def main():
    """CLI entry point for template fixer."""
    console.print("[bold blue]🔧 ThreatGPT Template Auto-Fixer[/bold blue]")
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        console.print("[red]❌ Templates directory not found![/red]")
        return
    
    fixer = TemplateFixer(templates_dir)
    
    console.print("\n[cyan]Scanning and fixing templates...[/cyan]")
    results = fixer.fix_all_templates()
    
    # Display results
    console.print(f"\n[bold green]✅ Fixing completed![/bold green]")
    console.print(f"Fixed: {len(results['fixed'])} templates")
    console.print(f"Skipped: {len(results['skipped'])} templates (no fixes needed)")
    console.print(f"Failed: {len(results['failed'])} templates")
    console.print(f"Total fixes applied: {results['total_fixes']}")
    
    # Detailed results
    if results["fixed"]:
        table = Table(title="Fixed Templates", show_header=True)
        table.add_column("Template", style="cyan")
        table.add_column("Fixes Applied", style="green")
        
        for fixed in results["fixed"]:
            fixes_str = "\n".join([f"• {fix}" for fix in fixed["fixes"]])
            table.add_row(fixed["file"], fixes_str)
        
        console.print(f"\n{table}")
    
    if results["failed"]:
        console.print(f"\n[red]❌ Failed to fix:[/red]")
        for failed in results["failed"]:
            console.print(f"  • {failed['file']}: {failed['error']}")


if __name__ == "__main__":
    main()