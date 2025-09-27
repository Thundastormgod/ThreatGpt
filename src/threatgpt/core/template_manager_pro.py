"""Professional Template Management System for ThreatGPT.

This module provides comprehensive template creation, validation, and management
capabilities following professional software development standards.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from threatgpt.config.models import (
    ThreatScenario, 
    ThreatType, 
    DeliveryVector, 
    SeniorityLevel,
    TechnicalLevel,
    IndustryType,
    CompanySize,
    DifficultyLevel,
    ScenarioMetadata
)
from threatgpt.config.yaml_loader import YAMLConfigLoader

console = Console()


class TemplateCreationWizard:
    """Interactive wizard for creating professional threat scenario templates."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path("templates")
        self.loader = YAMLConfigLoader()
        self.current_template: Dict[str, Any] = {}
        
    def create_template_interactive(self) -> Optional[Path]:
        """Create a new template through interactive wizard."""
        
        console.print(Panel.fit(
            "[bold blue]ThreatGPT Template Creation Wizard[/bold blue]\n"
            "Create professional threat simulation scenarios",
            border_style="blue"
        ))
        
        try:
            # Step 1: Basic Information
            self._collect_metadata()
            
            # Step 2: Threat Configuration
            self._collect_threat_info()
            
            # Step 3: Target Profile
            self._collect_target_profile()
            
            # Step 4: Behavioral Patterns
            self._collect_behavioral_patterns()
            
            # Step 5: Simulation Parameters
            self._collect_simulation_parameters()
            
            # Step 6: Validation and Save
            return self._validate_and_save()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Template creation cancelled.[/yellow]")
            return None
        except Exception as e:
            console.print(f"\n[red]Error during template creation: {e}[/red]")
            return None
    
    def _collect_metadata(self):
        """Collect template metadata."""
        console.print("\n[bold cyan]📝 Step 1: Template Metadata[/bold cyan]")
        
        name = Prompt.ask("Template name", default="New Threat Scenario")
        description = Prompt.ask("Description", default="Description of the threat scenario")
        author = Prompt.ask("Author", default="ThreatGPT Team")
        version = Prompt.ask("Version", default="1.0.0")
        
        # Collect tags
        console.print("\n[dim]Enter tags (comma-separated):[/dim]")
        tags_input = Prompt.ask("Tags", default="phishing,training")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        self.current_template["metadata"] = {
            "name": name,
            "description": description,
            "author": author,
            "version": version,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "tags": tags,
            "references": []
        }
    
    def _collect_threat_info(self):
        """Collect threat type and delivery information."""
        console.print("\n[bold cyan]🎯 Step 2: Threat Configuration[/bold cyan]")
        
        # Display threat types
        threat_types = [(t.value, t.value.replace('_', ' ').title()) for t in ThreatType]
        table = Table(title="Available Threat Types")
        table.add_column("Value", style="cyan")
        table.add_column("Description", style="white")
        
        for value, desc in threat_types:
            table.add_row(value, desc)
        
        console.print(table)
        
        threat_type = Prompt.ask(
            "Threat type",
            choices=[t.value for t in ThreatType],
            default="phishing"
        )
        
        # Display delivery vectors
        vectors = [(v.value, v.value.replace('_', ' ').title()) for v in DeliveryVector]
        table = Table(title="Available Delivery Vectors")
        table.add_column("Value", style="cyan")
        table.add_column("Description", style="white")
        
        for value, desc in vectors:
            table.add_row(value, desc)
        
        console.print(table)
        
        delivery_vector = Prompt.ask(
            "Delivery vector",
            choices=[v.value for v in DeliveryVector],
            default="email"
        )
        
        self.current_template["threat_type"] = threat_type
        self.current_template["delivery_vector"] = delivery_vector
    
    def _collect_target_profile(self):
        """Collect target profile information."""
        console.print("\n[bold cyan]👤 Step 3: Target Profile[/bold cyan]")
        
        role = Prompt.ask("Target role", default="Manager")
        department = Prompt.ask("Department", default="IT")
        
        # Seniority selection
        seniority = Prompt.ask(
            "Seniority level",
            choices=[s.value for s in SeniorityLevel],
            default="mid"
        )
        
        # Technical level
        technical_level = Prompt.ask(
            "Technical level",
            choices=[t.value for t in TechnicalLevel],
            default="moderate"
        )
        
        # Industry
        industry = Prompt.ask(
            "Industry",
            choices=[i.value for i in IndustryType],
            default="technology"
        )
        
        # Company size
        company_size = Prompt.ask(
            "Company size",
            choices=[c.value for c in CompanySize],
            default="medium"
        )
        
        # Optional fields
        working_hours = Prompt.ask("Typical working hours", default="9:00-17:00")
        comm_style = Prompt.ask("Communication style", default="professional")
        
        security_awareness = int(Prompt.ask(
            "Security awareness level (1-10)", 
            default="5"
        ))
        
        self.current_template["target_profile"] = {
            "role": role,
            "seniority": seniority,
            "department": department,
            "technical_level": technical_level,
            "industry": industry,
            "company_size": company_size,
            "typical_working_hours": working_hours,
            "communication_style": comm_style,
            "security_awareness_level": security_awareness,
            "interests": [],
            "social_media_presence": {}
        }
    
    def _collect_behavioral_patterns(self):
        """Collect behavioral patterns and attack tactics."""
        console.print("\n[bold cyan]🎭 Step 4: Behavioral Patterns[/bold cyan]")
        
        # MITRE ATT&CK techniques
        console.print("\n[dim]Enter MITRE ATT&CK technique IDs (e.g., T1566.001):[/dim]")
        techniques_input = Prompt.ask("MITRE techniques (comma-separated)", default="T1566.001,T1566.002")
        mitre_techniques = [t.strip() for t in techniques_input.split(",") if t.strip()]
        
        # Psychological triggers
        console.print("\n[dim]Common triggers: authority, urgency, curiosity, fear, greed[/dim]")
        triggers_input = Prompt.ask("Psychological triggers", default="authority,urgency")
        triggers = [t.strip() for t in triggers_input.split(",") if t.strip()]
        
        # Social engineering tactics  
        console.print("\n[dim]Common tactics: pretexting, impersonation, baiting, quid_pro_quo[/dim]")
        tactics_input = Prompt.ask("Social engineering tactics", default="pretexting,impersonation")
        tactics = [t.strip() for t in tactics_input.split(",") if t.strip()]
        
        self.current_template["behavioral_pattern"] = {
            "mitre_attack_techniques": mitre_techniques,
            "mitre_attack_tactics": ["Initial Access", "Execution"],
            "psychological_triggers": triggers,
            "social_engineering_tactics": tactics,
            "technical_methods": [],
            "evasion_techniques": []
        }
    
    def _collect_simulation_parameters(self):
        """Collect simulation execution parameters."""
        console.print("\n[bold cyan]⚙️ Step 5: Simulation Parameters[/bold cyan]")
        
        # Difficulty and duration
        difficulty = int(Prompt.ask("Difficulty level (1-10)", default="5"))
        duration = int(Prompt.ask("Estimated duration (minutes)", default="30"))
        
        # Simulation controls
        max_iterations = int(Prompt.ask("Max iterations", default="3"))
        max_duration = int(Prompt.ask("Max duration (minutes)", default="60"))
        
        urgency = int(Prompt.ask("Urgency level (1-10)", default="5"))
        
        escalation = Confirm.ask("Enable escalation?", default=True)
        adaptation = Confirm.ask("Enable response adaptation?", default=True)
        
        self.current_template["difficulty_level"] = difficulty
        self.current_template["estimated_duration"] = duration
        
        self.current_template["simulation_parameters"] = {
            "max_iterations": max_iterations,
            "max_duration_minutes": max_duration,
            "escalation_enabled": escalation,
            "response_adaptation": adaptation,
            "time_pressure_simulation": False,
            "multi_stage_attack": False,
            "persistence_simulation": False,
            "language": "en",
            "tone": "professional",
            "urgency_level": urgency,
            "compliance_mode": True,
            "content_filtering": True,
            "audit_logging": True
        }
        
        # Custom parameters section
        self.current_template["custom_parameters"] = {}
    
    def _validate_and_save(self) -> Optional[Path]:
        """Validate template and save to file."""
        console.print("\n[bold cyan]✅ Step 6: Validation & Save[/bold cyan]")
        
        # Show template preview
        console.print("\n[bold]Template Preview:[/bold]")
        console.print(Panel(
            yaml.dump(self.current_template, default_flow_style=False, sort_keys=False),
            title="Generated Template",
            border_style="green"
        ))
        
        if not Confirm.ask("Save this template?", default=True):
            return None
        
        # Validate against schema
        try:
            validated_scenario = ThreatScenario.parse_obj(self.current_template)
            console.print("[green]✅ Template validation successful![/green]")
        except ValidationError as e:
            console.print(f"[red]❌ Validation failed:[/red]")
            for error in e.errors():
                console.print(f"  - {error['loc'][0] if error['loc'] else 'root'}: {error['msg']}")
            
            if not Confirm.ask("Save anyway (as draft)?", default=False):
                return None
        
        # Generate filename
        safe_name = self.current_template["metadata"]["name"].lower()
        safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in safe_name)
        filename = f"{safe_name}.yaml"
        
        # Check if file exists
        file_path = self.templates_dir / filename
        if file_path.exists():
            if not Confirm.ask(f"File {filename} exists. Overwrite?", default=False):
                filename = Prompt.ask("Enter new filename", default=f"{safe_name}_new.yaml")
                file_path = self.templates_dir / filename
        
        # Save file
        self.templates_dir.mkdir(exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# ThreatGPT Threat Scenario Template\n")
            f.write(f"# Generated on {datetime.utcnow().isoformat()}Z\n\n")
            yaml.dump(self.current_template, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"\n[green]✅ Template saved: {file_path}[/green]")
        return file_path


class TemplateManager:
    """Professional template management and validation system."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path("templates")
        self.loader = YAMLConfigLoader()
    
    def validate_all_templates(self) -> Dict[str, Any]:
        """Comprehensive validation of all templates."""
        results = {
            "valid": [],
            "invalid": [],
            "statistics": {
                "total": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "success_rate": 0.0
            }
        }
        
        if not self.templates_dir.exists():
            return results
        
        template_files = list(self.templates_dir.glob("*.yaml")) + list(self.templates_dir.glob("*.yml"))
        results["statistics"]["total"] = len(template_files)
        
        for template_file in template_files:
            try:
                # Use load_and_validate_scenario directly
                scenario = self.loader.load_and_validate_scenario(template_file)
                
                # Extract enum values properly
                threat_type_value = scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else str(scenario.threat_type)
                difficulty_value = scenario.difficulty_level.value if hasattr(scenario.difficulty_level, 'value') else scenario.difficulty_level
                
                results["valid"].append({
                    "file": template_file.name,
                    "name": scenario.metadata.name,
                    "threat_type": threat_type_value,
                    "difficulty": difficulty_value
                })
                results["statistics"]["valid_count"] += 1
                
            except Exception as e:
                results["invalid"].append({
                    "file": template_file.name,
                    "error": str(e)
                })
                results["statistics"]["invalid_count"] += 1
        
        if results["statistics"]["total"] > 0:
            results["statistics"]["success_rate"] = results["statistics"]["valid_count"] / results["statistics"]["total"]
        
        return results
    
    def fix_template_issues(self, template_file: Path) -> bool:
        """Attempt to automatically fix common template issues."""
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse YAML
            template_data = yaml.safe_load(content)
            
            # Common fixes
            fixes_applied = []
            
            # Fix threat_type issues
            if "threat_type" in template_data:
                original = template_data["threat_type"]
                fixed = self._fix_threat_type(original)
                if fixed != original:
                    template_data["threat_type"] = fixed
                    fixes_applied.append(f"threat_type: {original} -> {fixed}")
            
            # Fix delivery_vector issues  
            if "delivery_vector" in template_data:
                original = template_data["delivery_vector"]
                fixed = self._fix_delivery_vector(original)
                if fixed != original:
                    template_data["delivery_vector"] = fixed
                    fixes_applied.append(f"delivery_vector: {original} -> {fixed}")
            
            # Fix simulation parameters
            if "simulation_parameters" in template_data:
                sim_params = template_data["simulation_parameters"]
                if isinstance(sim_params.get("max_iterations"), str):
                    try:
                        sim_params["max_iterations"] = int(sim_params["max_iterations"])
                        fixes_applied.append("max_iterations: converted to int")
                    except ValueError:
                        sim_params["max_iterations"] = 3
                        fixes_applied.append("max_iterations: defaulted to 3")
                
                if isinstance(sim_params.get("max_duration_minutes"), str):
                    try:
                        sim_params["max_duration_minutes"] = int(sim_params["max_duration_minutes"])
                        fixes_applied.append("max_duration_minutes: converted to int")
                    except ValueError:
                        sim_params["max_duration_minutes"] = 60
                        fixes_applied.append("max_duration_minutes: defaulted to 60")
            
            # Remove extra fields that cause validation errors
            extra_fields = ["success_metrics", "compliance_controls", "post_simulation_analysis"]
            for field in extra_fields:
                if field in template_data:
                    del template_data[field]
                    fixes_applied.append(f"Removed extra field: {field}")
            
            if fixes_applied:
                # Create backup
                backup_path = template_file.with_suffix(f".backup_{int(datetime.now().timestamp())}.yaml")
                shutil.copy2(template_file, backup_path)
                
                # Save fixed version
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write("# ThreatGPT Threat Scenario Template (Auto-fixed)\n")
                    f.write(f"# Fixes applied: {', '.join(fixes_applied)}\n\n")
                    yaml.dump(template_data, f, default_flow_style=False, sort_keys=False)
                
                console.print(f"[green]✅ Fixed {template_file.name}:[/green]")
                for fix in fixes_applied:
                    console.print(f"  - {fix}")
                console.print(f"[dim]Backup saved: {backup_path.name}[/dim]")
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]❌ Failed to fix {template_file.name}: {e}[/red]")
            return False
    
    def _fix_threat_type(self, value: str) -> str:
        """Fix common threat_type issues."""
        mappings = {
            "hybrid_attack": "advanced_persistent_threat",
            "multi_vector": "advanced_persistent_threat",
            "healthcare_targeted_attack": "spear_phishing"
        }
        return mappings.get(value, value)
    
    def _fix_delivery_vector(self, value: str) -> str:
        """Fix common delivery_vector issues."""
        mappings = {
            "multi_channel": "email",
            "multi_vector": "email"
        }
        return mappings.get(value, value)
    
    def create_from_template(self, source_template: str, new_name: str) -> Path:
        """Create a new template by copying and modifying an existing one."""
        
        source_path = self.templates_dir / f"{source_template}.yaml"
        if not source_path.exists():
            source_path = self.templates_dir / source_template
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source template not found: {source_template}")
        
        # Load source template
        with open(source_path, 'r', encoding='utf-8') as f:
            template_data = yaml.safe_load(f)
        
        # Modify metadata
        template_data["metadata"]["name"] = new_name
        template_data["metadata"]["description"] = f"Customized version of {source_template}"
        template_data["metadata"]["version"] = "1.0.0"
        template_data["metadata"]["author"] = "Custom"
        template_data["metadata"]["created_at"] = datetime.utcnow().isoformat() + "Z"
        template_data["metadata"]["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        # Generate new filename
        safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in new_name.lower())
        new_path = self.templates_dir / f"{safe_name}.yaml"
        
        # Save new template
        with open(new_path, 'w', encoding='utf-8') as f:
            yaml.dump(template_data, f, default_flow_style=False, sort_keys=False)
        
        return new_path


def main():
    """CLI entry point for template management."""
    import sys
    
    if len(sys.argv) < 2:
        console.print("Usage: python -m template_manager <command>")
        console.print("Commands: create, validate, fix, copy")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        wizard = TemplateCreationWizard()
        result = wizard.create_template_interactive()
        if result:
            console.print(f"[green]Template created: {result}[/green]")
    
    elif command == "validate":
        manager = TemplateManager()
        results = manager.validate_all_templates()
        
        table = Table(title="Template Validation Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Details", style="green")
        
        for valid in results["valid"]:
            table.add_row(valid["file"], "✅ Valid", f"{valid['threat_type']} (Difficulty: {valid['difficulty']})")
        
        for invalid in results["invalid"]:
            table.add_row(invalid["file"], "❌ Invalid", invalid["error"][:50] + "...")
        
        console.print(table)
        console.print(f"\nSuccess Rate: {results['statistics']['success_rate']:.1%}")
    
    elif command == "fix":
        manager = TemplateManager()
        templates_dir = Path("templates")
        
        for template_file in templates_dir.glob("*.yaml"):
            manager.fix_template_issues(template_file)
    
    else:
        console.print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()