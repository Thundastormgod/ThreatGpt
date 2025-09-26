#!/usr/bin/env python3
"""Comprehensive ThreatGPT Infrastructure Audit Script"""

import os
import sys
import json
import asyncio
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
try:
    from threatgpt.llm.manager import LLMManager
    from threatgpt.config.yaml_loader import YAMLConfigLoader
    from threatgpt.utils.logging import get_logger
except ImportError as e:
    print(f"Import warning: {e}")
    LLMManager = None
    YAMLConfigLoader = None
    get_logger = None

class InfrastructureAuditor:
    """Comprehensive infrastructure audit for ThreatGPT."""
    
    def __init__(self):
        load_dotenv()
        self.logger = get_logger(__name__)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
            "recommendations": []
        }
    
    def log_check(self, check_name: str, status: str, details: str, issue: str = None):
        """Log a check result."""
        self.results["checks"][check_name] = {
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if issue:
            self.results["issues"].append(f"{check_name}: {issue}")
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {check_name}: {details}")
    
    def check_environment_variables(self):
        """Check all required environment variables."""
        print("\n🔧 CHECKING ENVIRONMENT VARIABLES")
        print("-" * 50)
        
        required_vars = [
            "OPENROUTER_API_KEY",
            "THREATGPT_CONFIG_PATH", 
            "THREATGPT_LOG_LEVEL",
            "THREATGPT_SAFETY_MODE"
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                masked_value = value[:20] + "..." if len(value) > 20 else value
                self.log_check(f"ENV_{var}", "PASS", f"Set to: {masked_value}")
            else:
                self.log_check(f"ENV_{var}", "WARN", "Not set", f"Missing environment variable: {var}")
    
    def check_directory_structure(self):
        """Check required directories exist."""
        print("\n📁 CHECKING DIRECTORY STRUCTURE")
        print("-" * 50)
        
        required_dirs = [
            "src/threatgpt",
            "templates",
            "logs",
            "logs/simulations",
            "logs/simulations/successful",
            "logs/simulations/failed",
            "config",
            "data"
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists():
                self.log_check(f"DIR_{dir_path.replace('/', '_')}", "PASS", f"Exists with {len(list(path.iterdir()))} items")
            else:
                self.log_check(f"DIR_{dir_path.replace('/', '_')}", "FAIL", "Missing", f"Required directory missing: {dir_path}")
    
    def check_template_files(self):
        """Check scenario template files."""
        print("\n📝 CHECKING TEMPLATE FILES")
        print("-" * 50)
        
        templates_dir = Path("templates")
        if not templates_dir.exists():
            self.log_check("TEMPLATES", "FAIL", "Templates directory missing", "No templates directory found")
            return
        
        template_files = list(templates_dir.glob("*.yaml"))
        if template_files:
            self.log_check("TEMPLATES", "PASS", f"Found {len(template_files)} template files")
            
            # Test loading each template
            for template_file in template_files:
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if len(content) > 100:  # Basic content check
                        self.log_check(f"TEMPLATE_{template_file.stem}", "PASS", f"Valid ({len(content)} chars)")
                    else:
                        self.log_check(f"TEMPLATE_{template_file.stem}", "WARN", "Very short content")
                except Exception as e:
                    self.log_check(f"TEMPLATE_{template_file.stem}", "FAIL", f"Load error: {str(e)}")
        else:
            self.log_check("TEMPLATES", "FAIL", "No template files found", "No .yaml template files in templates directory")
    
    async def check_llm_integration(self):
        """Check LLM provider integration."""
        print("\n🤖 CHECKING LLM INTEGRATION")
        print("-" * 50)
        
        try:
            config = {
                'openrouter': {
                    'api_key': os.getenv('OPENROUTER_API_KEY'),
                    'model': 'qwen/qwen3-vl-235b-a22b-thinking'
                }
            }
            
            if not config['openrouter']['api_key']:
                self.log_check("LLM_CONFIG", "FAIL", "No OpenRouter API key", "OpenRouter API key not configured")
                return
            
            llm_manager = LLMManager(config=config)
            providers = llm_manager.get_available_providers()
            
            if 'openrouter' in providers:
                self.log_check("LLM_PROVIDER", "PASS", f"OpenRouter available, providers: {providers}")
                
                # Test basic generation
                try:
                    result = await llm_manager.generate_content(
                        "Test connection. Respond with 'Connection successful'",
                        max_tokens=50,
                        temperature=0.1
                    )
                    
                    if result and result.content:
                        content_length = len(result.content)
                        self.log_check("LLM_GENERATION", "PASS", f"Generated {content_length} chars: {result.content[:50]}...")
                    else:
                        self.log_check("LLM_GENERATION", "FAIL", "No content generated", "LLM generation returned empty result")
                        
                except Exception as e:
                    self.log_check("LLM_GENERATION", "FAIL", f"Generation error: {str(e)}", f"LLM generation failed: {str(e)}")
            else:
                self.log_check("LLM_PROVIDER", "FAIL", f"OpenRouter not available, providers: {providers}", "OpenRouter provider not initialized")
                
        except Exception as e:
            self.log_check("LLM_INTEGRATION", "FAIL", f"Integration error: {str(e)}", f"LLM integration failed: {str(e)}")
    
    def check_cli_commands(self):
        """Check CLI command availability."""
        print("\n💻 CHECKING CLI COMMANDS")
        print("-" * 50)
        
        import subprocess
        
        cli_commands = [
            ("threatgpt --help", "Basic CLI help"),
            ("threatgpt simulate --help", "Simulate command help"),
            ("threatgpt config --help", "Config command help")
        ]
        
        for cmd, description in cli_commands:
            try:
                result = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.log_check(f"CLI_{cmd.split()[1]}", "PASS", f"{description} - working")
                else:
                    self.log_check(f"CLI_{cmd.split()[1]}", "WARN", f"{description} - exit code {result.returncode}")
                    
            except subprocess.TimeoutExpired:
                self.log_check(f"CLI_{cmd.split()[1]}", "WARN", f"{description} - timeout")
            except Exception as e:
                self.log_check(f"CLI_{cmd.split()[1]}", "FAIL", f"{description} - error: {str(e)}")
    
    def check_logging_system(self):
        """Check logging system configuration."""
        print("\n📊 CHECKING LOGGING SYSTEM")
        print("-" * 50)
        
        try:
            # Test log directory creation
            log_dirs = [
                "logs",
                "logs/simulations", 
                "logs/simulations/successful",
                "logs/simulations/failed"
            ]
            
            for log_dir in log_dirs:
                path = Path(log_dir)
                path.mkdir(parents=True, exist_ok=True)
                if path.exists():
                    self.log_check(f"LOG_DIR_{log_dir.replace('/', '_')}", "PASS", "Directory created/exists")
                else:
                    self.log_check(f"LOG_DIR_{log_dir.replace('/', '_')}", "FAIL", "Failed to create directory")
            
            # Test log file writing
            test_log_file = Path("logs/infrastructure_audit.json")
            test_data = {"test": "audit", "timestamp": datetime.now().isoformat()}
            
            with open(test_log_file, 'w') as f:
                json.dump(test_data, f, indent=2)
            
            if test_log_file.exists():
                self.log_check("LOG_WRITING", "PASS", f"Test log written to {test_log_file}")
            else:
                self.log_check("LOG_WRITING", "FAIL", "Failed to write test log file")
                
        except Exception as e:
            self.log_check("LOGGING_SYSTEM", "FAIL", f"Logging system error: {str(e)}")
    
    async def check_end_to_end_simulation(self):
        """Perform a quick end-to-end simulation test."""
        print("\n🎯 CHECKING END-TO-END SIMULATION")
        print("-" * 50)
        
        try:
            # Find a simple template
            templates_dir = Path("templates")
            template_files = list(templates_dir.glob("*.yaml"))
            
            if not template_files:
                self.log_check("E2E_SIMULATION", "FAIL", "No templates available for testing")
                return
            
            # Use IT help desk template if available
            test_template = None
            for template in template_files:
                if "it_helpdesk" in template.name.lower():
                    test_template = template
                    break
            
            if not test_template:
                test_template = template_files[0]  # Use first available
            
            self.log_check("E2E_TEMPLATE", "PASS", f"Using template: {test_template.name}")
            
            # Load scenario
            try:
                if YAMLConfigLoader:
                    loader = YAMLConfigLoader()
                    with open(test_template, 'r', encoding='utf-8') as f:
                        scenario_content = f.read()
                    self.log_check("E2E_SCENARIO_LOAD", "PASS", f"Template readable: {test_template.name}")
                else:
                    self.log_check("E2E_SCENARIO_LOAD", "WARN", "YAML loader not available")
            except Exception as e:
                self.log_check("E2E_SCENARIO_LOAD", "FAIL", f"Failed to load scenario: {str(e)}")
                return
            
            # Test LLM manager
            config = {
                'openrouter': {
                    'api_key': os.getenv('OPENROUTER_API_KEY'),
                    'model': 'qwen/qwen3-vl-235b-a22b-thinking'
                }
            }
            
            llm_manager = LLMManager(config=config)
            
            # Quick content generation test
            try:
                result = await llm_manager.generate_content(
                    "Generate a brief security training example (50 words max)",
                    scenario_type="threat_simulation_reconnaissance",
                    max_tokens=100,
                    temperature=0.5
                )
                
                if result and result.content:
                    self.log_check("E2E_CONTENT_GEN", "PASS", f"Generated {len(result.content)} chars")
                else:
                    self.log_check("E2E_CONTENT_GEN", "FAIL", "No content generated")
                    
            except Exception as e:
                self.log_check("E2E_CONTENT_GEN", "FAIL", f"Content generation failed: {str(e)}")
            
        except Exception as e:
            self.log_check("E2E_SIMULATION", "FAIL", f"End-to-end test failed: {str(e)}")
    
    def generate_recommendations(self):
        """Generate recommendations based on audit results."""
        print("\n💡 GENERATING RECOMMENDATIONS")
        print("-" * 50)
        
        failed_checks = [name for name, result in self.results["checks"].items() if result["status"] == "FAIL"]
        warning_checks = [name for name, result in self.results["checks"].items() if result["status"] == "WARN"]
        
        if failed_checks:
            self.results["recommendations"].append("🔧 Fix failed checks: " + ", ".join(failed_checks))
        
        if warning_checks:
            self.results["recommendations"].append("⚠️ Address warnings: " + ", ".join(warning_checks))
        
        # Specific recommendations
        if any("TIMEOUT" in issue for issue in self.results["issues"]):
            self.results["recommendations"].append("🕐 Implement timeout handling and retry logic for API calls")
        
        if any("ENV_" in check for check in failed_checks):
            self.results["recommendations"].append("🔐 Configure missing environment variables in .env file")
        
        if any("LLM_" in check for check in failed_checks):
            self.results["recommendations"].append("🤖 Fix LLM integration issues - check API key and network connectivity")
        
        if not self.results["recommendations"]:
            self.results["recommendations"].append("🎉 All systems operational - no immediate actions required")
        
        for rec in self.results["recommendations"]:
            print(rec)
    
    def save_audit_results(self):
        """Save audit results to file."""
        audit_file = Path("logs/infrastructure_audit.json")
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(audit_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Audit results saved to: {audit_file}")
    
    async def run_full_audit(self):
        """Run complete infrastructure audit."""
        print("🔍 THREATGPT INFRASTRUCTURE AUDIT")
        print("=" * 60)
        print(f"Timestamp: {self.results['timestamp']}")
        print("=" * 60)
        
        # Run all checks
        self.check_environment_variables()
        self.check_directory_structure()
        self.check_template_files()
        await self.check_llm_integration()
        self.check_cli_commands()
        self.check_logging_system()
        await self.check_end_to_end_simulation()
        
        # Generate summary
        self.generate_recommendations()
        self.save_audit_results()
        
        # Summary
        total_checks = len(self.results["checks"])
        passed_checks = len([r for r in self.results["checks"].values() if r["status"] == "PASS"])
        failed_checks = len([r for r in self.results["checks"].values() if r["status"] == "FAIL"])
        warning_checks = len([r for r in self.results["checks"].values() if r["status"] == "WARN"])
        
        print(f"\n📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed_checks}/{total_checks}")
        print(f"❌ Failed: {failed_checks}/{total_checks}")
        print(f"⚠️ Warnings: {warning_checks}/{total_checks}")
        print(f"🔧 Issues Found: {len(self.results['issues'])}")
        print(f"💡 Recommendations: {len(self.results['recommendations'])}")
        
        if failed_checks == 0:
            print(f"\n🎉 INFRASTRUCTURE STATUS: HEALTHY")
        elif failed_checks <= 2:
            print(f"\n⚠️ INFRASTRUCTURE STATUS: MINOR ISSUES")
        else:
            print(f"\n❌ INFRASTRUCTURE STATUS: NEEDS ATTENTION")

async def main():
    """Run infrastructure audit."""
    auditor = InfrastructureAuditor()
    await auditor.run_full_audit()

if __name__ == "__main__":
    asyncio.run(main())