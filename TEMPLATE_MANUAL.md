# 📖 ThreatGPT Template Creation, Configuration & Validation Manual

## 📚 **Table of Contents**

1. [Introduction](#introduction)
2. [Template Creation](#template-creation)
3. [Configuration Files](#configuration-files)
4. [Validation System](#validation-system)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Features](#advanced-features)
8. [Reference](#reference)

---

## 🚀 **Introduction**

This manual provides comprehensive guidance for creating, configuring, and validating threat scenario templates in the ThreatGPT system. The ThreatGPT framework uses YAML-based templates with strict schema validation to ensure consistency and reliability in threat simulations.

### **System Overview**
- **Templates**: YAML files defining threat scenarios
- **Configuration**: System-wide settings for LLM providers and simulation parameters
- **Validation**: Multi-layer validation system ensuring template quality and consistency

---

## 🎯 **Template Creation**

### **1. Template Structure Overview**

Every ThreatGPT template follows a standardized structure with the following main sections:

```yaml
# Template Header (Comments)
metadata:          # Template information and versioning
threat_type:       # Type of threat (enum)
delivery_vector:   # How the attack is delivered (enum)
target_profile:    # Target demographic and characteristics
behavioral_pattern: # Attack tactics and techniques
difficulty_level:  # Simulation difficulty (1-10)
estimated_duration: # Expected duration in minutes
simulation_parameters: # Execution controls
custom_parameters: # Optional custom settings
```

### **2. Creating Templates - Method 1: Interactive Wizard**

The easiest way to create a new template is using the interactive wizard:

```bash
# Start the interactive template creation wizard
python -m src.threatgpt.cli.main templates create
```

**Wizard Steps:**
1. **Metadata Collection**: Name, description, author, version, tags
2. **Threat Configuration**: Threat type and delivery vector selection
3. **Target Profile**: Demographics and characteristics
4. **Behavioral Patterns**: MITRE ATT&CK techniques and tactics
5. **Simulation Parameters**: Difficulty, duration, and controls
6. **Validation & Save**: Schema validation and file creation

### **3. Creating Templates - Method 2: Clone Existing**

Clone and modify an existing template:

```bash
# Clone an existing template
python -m src.threatgpt.cli.main templates clone executive_phishing my_new_scenario

# View the cloned template
python -m src.threatgpt.cli.main templates show my_new_scenario --validate
```

### **4. Creating Templates - Method 3: Manual Creation**

Create a template file manually by following the complete structure:

```yaml
# ThreatGPT Threat Scenario Template
# Created: 2025-09-27T10:00:00Z

metadata:
  name: "My Custom Threat Scenario"
  description: "Detailed description of the threat scenario and its objectives"
  version: "1.0.0"
  author: "Your Name"
  created_at: "2025-09-27T10:00:00Z"
  updated_at: "2025-09-27T10:00:00Z"
  tags:
    - "phishing"
    - "executive"
    - "training"
  references:
    - "https://attack.mitre.org/techniques/T1566/001/"
    - "https://example.com/reference"

threat_type: "spear_phishing"  # Must be from valid enum
delivery_vector: "email"       # Must be from valid enum

target_profile:
  role: "Chief Executive Officer"
  seniority: "executive"           # Valid: entry, junior, mid, senior, lead, manager, director, vice_president, senior_vice_president, executive, c_level
  department: "Executive"
  technical_level: "moderate"     # Valid: basic, moderate, advanced, expert
  industry: "technology"          # Valid enum from IndustryType
  company_size: "large"          # Valid: startup, small, medium, large, enterprise
  typical_working_hours: "8:00-18:00"
  communication_style: "formal"
  security_awareness_level: 7    # 1-10 scale
  interests:
    - "business_strategy"
    - "market_analysis"
  social_media_presence:
    linkedin: "active"
    twitter: "moderate"

behavioral_pattern:
  mitre_attack_techniques:       # List of MITRE ATT&CK technique IDs
    - "T1566.001"
    - "T1566.002"
  mitre_attack_tactics:          # List of MITRE ATT&CK tactic names
    - "Initial Access"
    - "Execution"
  psychological_triggers:        # List of psychological manipulation techniques
    - "authority"
    - "urgency"
    - "fear"
  social_engineering_tactics:    # List of social engineering approaches
    - "pretexting"
    - "impersonation"
  technical_methods:            # List of technical approaches
    - "email_spoofing"
  evasion_techniques:           # List of security evasion methods
    - "reputation_exploitation"

difficulty_level: 8             # Integer 1-10
estimated_duration: 45          # Integer minutes

simulation_parameters:
  max_iterations: 3             # Integer
  max_duration_minutes: 90      # Integer
  escalation_enabled: true      # Boolean
  response_adaptation: true     # Boolean
  time_pressure_simulation: false  # Boolean
  multi_stage_attack: false    # Boolean
  persistence_simulation: false # Boolean
  language: "en"               # String
  tone: "professional"         # String
  urgency_level: 7             # Integer 1-10
  compliance_mode: true        # Boolean
  content_filtering: true      # Boolean
  audit_logging: true          # Boolean

custom_parameters: {}           # Optional custom settings
```

### **5. Template Sections Detailed**

#### **Metadata Section**
```yaml
metadata:
  name: "Human-readable scenario name (3-100 chars)"
  description: "Detailed scenario description (10-500 chars)"
  version: "Semantic version (e.g., 1.0.0)"
  author: "Template creator name (optional)"
  created_at: "ISO timestamp (auto-generated if missing)"
  updated_at: "ISO timestamp (auto-updated)"
  tags: ["array", "of", "categorization", "tags"]
  references: ["array", "of", "external", "reference", "urls"]
```

#### **Threat Type Enum Values**
```yaml
# Valid threat_type values:
- phishing
- spear_phishing
- malware
- ransomware
- social_engineering
- insider_threat
- advanced_persistent_threat
- credential_harvesting
- watering_hole
- supply_chain
- physical_security
- voice_phishing
- sms_phishing
```

#### **Delivery Vector Enum Values**
```yaml
# Valid delivery_vector values:
- email
- sms
- social_media
- phone_call
- usb_device
- network_intrusion
- physical_access
- web_application
- mobile_app
- qr_code
- messaging_app
- video_conference
```

#### **Target Profile Enums**
```yaml
# Seniority levels:
- entry, junior, mid, senior, lead
- manager, director, vice_president, senior_vice_president
- executive, c_level

# Technical levels:
- basic, moderate, advanced, expert

# Industries:
- technology, financial_services, healthcare, government
- education, retail, manufacturing, energy
- telecommunications, media, legal, consulting
- non_profit, startup, other

# Company sizes:
- startup, small, medium, large, enterprise
```

---

## ⚙️ **Configuration Files**

### **1. Main Configuration File (`config.yaml`)**

The primary configuration file controls system-wide settings:

```yaml
# Production Configuration for ThreatGPT

# LLM Provider Configuration
llm:
  default_provider: "openrouter"  # Primary provider
  
  openai:
    api_key: ""                   # Set via OPENAI_API_KEY env var
    model: "gpt-4o-mini"
    base_url: "https://api.openai.com/v1"
    max_tokens: 1000
    temperature: 0.7
    timeout_seconds: 60
    retry_attempts: 3
  
  anthropic:
    api_key: ""                   # Set via ANTHROPIC_API_KEY env var
    model: "claude-3-haiku-20240307"
    base_url: "https://api.anthropic.com"
    max_tokens: 1000
    temperature: 0.7
    timeout_seconds: 60
    retry_attempts: 3
  
  openrouter:
    api_key: ""                   # Set via OPENROUTER_API_KEY env var
    model: "anthropic/claude-3.5-sonnet"
    base_url: "https://openrouter.ai/api/v1"
    max_tokens: 1500
    temperature: 0.8
    timeout_seconds: 120
    retry_attempts: 3

# Simulation Configuration
simulation:
  default_output_format: "rich"    # rich, json, yaml
  log_level: "INFO"               # DEBUG, INFO, WARNING, ERROR
  enable_analytics: true          # Enable usage analytics
  cache_responses: false          # Cache LLM responses
  
  # Safety and Compliance
  content_filtering:
    enabled: true
    strict_mode: true
    blocked_keywords: []
  
  compliance:
    audit_logging: true
    data_retention_days: 90
    anonymize_logs: true

# Output Configuration
output:
  directory: "generated_content"   # Default output directory
  include_metadata: true          # Include generation metadata
  format_json: true              # Pretty-format JSON output
  
# Template Configuration
templates:
  directory: "templates"          # Template directory
  validate_on_load: true         # Validate templates on startup
  auto_backup: true              # Backup templates before modification
  
# Development Settings (only in dev environment)
development:
  debug_mode: false              # Enable debug output
  mock_llm: false               # Use mock LLM responses
  verbose_logging: false        # Extra detailed logging
```

### **2. Environment Variables**

Critical settings should be configured via environment variables:

```bash
# API Keys (required)
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key" 
export OPENROUTER_API_KEY="your-openrouter-api-key"

# Optional overrides
export THREATGPT_LOG_LEVEL="DEBUG"
export THREATGPT_OUTPUT_DIR="/custom/output/path"
export THREATGPT_CONFIG_FILE="/custom/config.yaml"
```

### **3. Configuration Hierarchy**

Settings are loaded in the following order (later overrides earlier):

1. **Default Configuration**: Built-in system defaults
2. **Main Config File**: `config.yaml` in project root
3. **User Config File**: `~/.threatgpt/config.yaml` (if exists)
4. **Environment Variables**: `THREATGPT_*` variables
5. **CLI Arguments**: Command-line parameter overrides

### **4. Creating Custom Configuration**

```yaml
# custom_config.yaml
llm:
  default_provider: "anthropic"
  anthropic:
    model: "claude-3-sonnet-20240229"
    temperature: 0.9
    max_tokens: 2000

simulation:
  default_output_format: "json"
  log_level: "DEBUG"

# Load with custom config
python -m src.threatgpt.cli.main --config custom_config.yaml simulate -s template.yaml
```

---

## 🛡️ **Validation System**

### **1. Validation Levels**

The ThreatGPT validation system operates at multiple levels:

#### **Level 1: YAML Syntax Validation**
- Checks for valid YAML format
- Identifies syntax errors with line numbers
- Validates UTF-8 encoding
- Ensures file readability

#### **Level 2: Schema Validation**
- Validates against Pydantic models
- Type checking (strings, integers, booleans)
- Enum value validation
- Required field verification
- Field format validation (timestamps, URLs)

#### **Level 3: Business Logic Validation**
- Cross-field dependencies
- Logical consistency checks
- MITRE ATT&CK technique format validation
- Value range verification

#### **Level 4: Security Validation**
- Content filtering for inappropriate material
- Safe YAML loading (prevents code execution)
- Input sanitization
- Path traversal protection

### **2. Validation Commands**

#### **Single Template Validation**
```bash
# Quick validation with results
python -m src.threatgpt.cli.main templates show my_template --validate

# Validate with YAML display
python -m src.threatgpt.cli.main templates show my_template --validate --show-yaml
```

#### **Professional Validation Suite**
```bash
# Comprehensive validation report
python -m src.threatgpt.cli.main templates validate-pro

# Validation with auto-fix
python -m src.threatgpt.cli.main templates validate-pro --auto-fix --backup
```

#### **Batch Validation**
```bash
# Validate all templates
python -m src.threatgpt.cli.main templates validate-all

# Generate validation report
python -m src.threatgpt.cli.main templates validate-all --output-dir reports/

# List templates with validation status
python -m src.threatgpt.cli.main templates list-all --validate
```

#### **Health Assessment**
```bash
# Ecosystem health check (100-point scoring)
python -m src.threatgpt.cli.main templates health

# Template statistics and distribution
python -m src.threatgpt.cli.main templates stats
```

### **3. Validation API Usage**

```python
from src.threatgpt.config.yaml_loader import YAMLConfigLoader
from pathlib import Path

# Initialize validator
loader = YAMLConfigLoader(strict_mode=True, schema_validation=True)

try:
    # Validate single template
    scenario = loader.load_and_validate_scenario("templates/my_template.yaml")
    print(f"✅ Valid: {scenario.metadata.name}")
    
    # Validate directory
    results = loader.validate_config_directory("templates/")
    print(f"Success Rate: {results['valid_files']}/{results['total_files']}")
    
except Exception as e:
    print(f"❌ Validation Error: {e}")
```

### **4. Common Validation Errors & Solutions**

#### **Error: Invalid Enum Value**
```yaml
# ❌ Invalid
threat_type: "custom_attack"

# ✅ Valid
threat_type: "spear_phishing"
```

#### **Error: Missing Required Field**
```yaml
# ❌ Missing difficulty_level
metadata:
  name: "Test Scenario"

# ✅ Complete
metadata:
  name: "Test Scenario"
  description: "Test description"
  version: "1.0.0"
difficulty_level: 5
estimated_duration: 30
```

#### **Error: Type Mismatch**
```yaml
# ❌ String instead of integer
simulation_parameters:
  max_iterations: "3"

# ✅ Correct type
simulation_parameters:
  max_iterations: 3
```

#### **Error: Invalid MITRE Format**
```yaml
# ❌ Invalid technique ID
behavioral_pattern:
  mitre_attack_techniques:
    - "T1566"

# ✅ Valid format
behavioral_pattern:
  mitre_attack_techniques:
    - "T1566.001"
```

### **5. Auto-Fix Capabilities**

The system can automatically fix common issues:

#### **Automatic Fixes Applied:**
- **Enum Mapping**: Maps invalid values to valid enums
- **Type Conversion**: Converts strings to appropriate types
- **Field Addition**: Adds missing required fields with defaults
- **Format Standardization**: Normalizes timestamps and booleans
- **Field Removal**: Removes unsupported/deprecated fields

#### **Running Auto-Fix:**
```bash
# Auto-fix with backup
python -m src.threatgpt.cli.main templates validate-pro --auto-fix --backup

# Standalone auto-fixer
python fix_templates.py
```

#### **Safety Features:**
- 🔒 **Automatic Backups**: Original files preserved
- 📝 **Change Documentation**: All fixes logged in file headers
- ⚡ **Validation Pre-check**: Only valid fixes applied
- 🎯 **Selective Fixing**: Only problematic fields modified

---

## 🌟 **Best Practices**

### **1. Template Development Workflow**

#### **Step 1: Start with Existing Template**
```bash
# Clone a similar, working template
python -m src.threatgpt.cli.main templates clone executive_phishing my_new_scenario
```

#### **Step 2: Customize Metadata**
- Update name, description, and version
- Add appropriate tags for categorization
- Include relevant references

#### **Step 3: Modify Core Settings**
- Select appropriate threat_type and delivery_vector
- Adjust difficulty_level based on target audience
- Set realistic estimated_duration

#### **Step 4: Validate Early and Often**
```bash
# Validate during development
python -m src.threatgpt.cli.main templates show my_new_scenario --validate
```

#### **Step 5: Test Simulation**
```bash
# Test the template with simulation
python -m src.threatgpt.cli.main simulate -s my_new_scenario.yaml
```

### **2. Version Control Best Practices**

#### **Template Versioning**
- Use semantic versioning (major.minor.patch)
- Increment patch for bug fixes
- Increment minor for new features
- Increment major for breaking changes

#### **Git Workflow**
```bash
# Before committing templates
python -m src.threatgpt.cli.main templates validate-pro --auto-fix

# Commit with descriptive message
git add templates/my_template.yaml
git commit -m "feat: add executive phishing scenario v1.2.0"
```

### **3. Quality Standards**

#### **Maintain High Quality**
- Target 85%+ validation success rate
- Ensure diverse threat type coverage
- Include comprehensive MITRE ATT&CK mappings
- Provide detailed descriptions and references

#### **Regular Health Checks**
```bash
# Weekly ecosystem health assessment
python -m src.threatgpt.cli.main templates health
```

### **4. Security Considerations**

#### **Content Guidelines**
- Avoid explicit harmful content
- Use professional, educational language
- Focus on security awareness training
- Include compliance and ethical considerations

#### **Data Handling**
- Don't include real personal information
- Use fictional company names and personas
- Anonymize any real-world references
- Ensure GDPR/privacy compliance

### **5. Documentation Standards**

#### **Template Documentation**
- Include clear, descriptive names
- Provide detailed scenario descriptions
- Document all custom parameters
- Reference relevant standards and frameworks

#### **Change Documentation**
- Update metadata.updated_at for all changes
- Document fixes in file headers
- Maintain changelog for major revisions
- Track validation improvements

---

## 🔧 **Troubleshooting**

### **1. Common Issues**

#### **Template Not Loading**
```bash
# Check file syntax
python -m src.threatgpt.cli.main templates show my_template --show-yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('templates/my_template.yaml'))"
```

#### **Validation Failures**
```bash
# Get detailed error information
python -m src.threatgpt.cli.main templates validate-pro

# Check specific template
python -m src.threatgpt.cli.main templates show my_template --validate
```

#### **Configuration Issues**
```bash
# Test configuration loading
python -c "from src.threatgpt.config.yaml_loader import load_config; print(load_config('config.yaml'))"

# Check environment variables
echo $OPENROUTER_API_KEY
```

#### **🔥 File Path Issues (Common Problem)**

**Problem**: `Configuration file not found: my_template.yaml`

This misleading error occurs when using incorrect file paths with the simulate command.

**❌ Wrong (causes "configuration not found" error):**
```bash
python -m src.threatgpt.cli.main simulate -s test_scenario.yaml
```

**✅ Correct (works properly):**
```bash
python -m src.threatgpt.cli.main simulate -s templates/test_scenario.yaml
```

**Root Cause**: Different commands have different path resolution:
- **Template commands** automatically look in `templates/` directory:
  ```bash
  # These work with just the filename
  python -m src.threatgpt.cli.main templates show test_scenario --validate
  python -m src.threatgpt.cli.main templates clone executive_phishing my_template
  ```

- **Simulation commands** require full path from project root:
  ```bash
  # These need the templates/ prefix
  python -m src.threatgpt.cli.main simulate -s templates/test_scenario.yaml
  python -m src.threatgpt.cli.main simulate -s templates/my_template.yaml --dry-run
  ```

**Quick Fixes**:
```bash
# Option 1: Use full path (recommended)
python -m src.threatgpt.cli.main simulate -s templates/my_template.yaml

# Option 2: Navigate to templates directory first
cd templates
python -m src.threatgpt.cli.main simulate -s my_template.yaml

# Option 3: Use absolute path
python -m src.threatgpt.cli.main simulate -s "C:\full\path\to\templates\my_template.yaml"
```

**Testing & Verification**:
```bash
# Always test with dry-run first
python -m src.threatgpt.cli.main simulate -s templates/my_template.yaml --dry-run

# Validate template separately
python -m src.threatgpt.cli.main templates show my_template --validate

# Check if template exists
ls templates/my_template.yaml  # Linux/Mac
dir templates\my_template.yaml # Windows
```

**Pro Tips**:
- ✅ Always use `--dry-run` first to test file path resolution
- ✅ Use tab completion in shell for accurate file paths  
- ✅ Check current directory: `pwd` (Linux/Mac) or `cd` (Windows)
- ✅ Use forward slashes `/` even on Windows for consistency

### **2. Debug Mode**

Enable debug mode for detailed troubleshooting:

```bash
# Environment variable
export THREATGPT_LOG_LEVEL=DEBUG

# Configuration file
development:
  debug_mode: true
  verbose_logging: true
```

### **3. Validation Recovery**

#### **Fix Corrupted Templates**
```bash
# Attempt automatic recovery
python -m src.threatgpt.cli.main templates validate-pro --auto-fix --backup

# Manual recovery from backup
cp templates/my_template.backup.yaml templates/my_template.yaml
```

#### **Reset to Known Good State**
```bash
# Restore from git
git checkout HEAD -- templates/

# Validate restored templates
python -m src.threatgpt.cli.main templates validate-pro
```

### **4. Performance Issues**

#### **Large Template Libraries**
```bash
# Validate specific directories only
python -m src.threatgpt.cli.main templates validate-all --directory specific_folder/

# Use parallel validation (if implemented)
python -m src.threatgpt.cli.main templates validate-pro --parallel
```

---

## 🚀 **Advanced Features**

### **1. Custom Validation Rules**

Extend validation with custom rules:

```python
from src.threatgpt.config.yaml_loader import YAMLConfigLoader

class CustomValidator(YAMLConfigLoader):
    def validate_custom_rules(self, config):
        # Add custom business logic validation
        if config.get('threat_type') == 'phishing':
            if 'email' not in config.get('delivery_vector'):
                raise ValueError("Phishing attacks should use email delivery")
        
        return super().validate_threat_scenario(config)
```

### **2. Template Inheritance**

Create template hierarchies:

```yaml
# base_phishing.yaml
metadata:
  template_type: "base"
threat_type: "phishing"
delivery_vector: "email"
# ... common fields

# executive_phishing.yaml  
metadata:
  inherits_from: "base_phishing"
  name: "Executive Phishing"
target_profile:
  seniority: "executive"
# ... specific overrides
```

### **3. Dynamic Templates**

Templates with conditional logic:

```yaml
# Use template variables for customization
metadata:
  name: "{{COMPANY_NAME}} Phishing Simulation"
  
target_profile:
  industry: "{{TARGET_INDUSTRY}}"
  company_size: "{{COMPANY_SIZE}}"
  
# Variables resolved at runtime
```

### **4. Integration Hooks**

#### **Pre-validation Hooks**
```python
def pre_validation_hook(template_path, config):
    """Called before validation"""
    # Add preprocessing logic
    return config

def post_validation_hook(template_path, scenario):
    """Called after successful validation"""
    # Add post-processing logic
    return scenario
```

#### **CI/CD Integration**
```bash
# .github/workflows/template-validation.yml
name: Template Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Templates
        run: |
          python -m src.threatgpt.cli.main templates validate-pro
          python -m src.threatgpt.cli.main templates health
```

---

## 📖 **Reference**

### **1. Command Reference**

#### **Template Commands**
```bash
# Creation
templates create                    # Interactive wizard
templates clone <source> <name>     # Clone existing template

# Validation  
templates show <name> [--validate] [--show-yaml]  # View template
templates validate-pro [--auto-fix] [--backup]    # Professional validation
templates validate-all [--output-dir <dir>]       # Batch validation
templates list-all [--validate] [--format <fmt>]  # List with validation

# Analytics
templates health                    # Ecosystem health (100-point score)
templates stats                     # Statistics and distribution

# Management
templates copy <source> <dest>      # Copy template (legacy)
```

#### **Configuration Commands**
```bash
# Simulation
simulate -s <template> [--config <file>] [--output-dir <dir>]
simulate --list-providers          # List available LLM providers
simulate --test-config            # Test configuration

# System
logs validate [--file <path>] [--directory <dir>]  # Log validation
status                            # System status
```

### **2. Schema Reference**

Complete schema definitions are available in:
- `src/threatgpt/config/models.py` - Pydantic model definitions
- `PROFESSIONAL_TEMPLATE_SYSTEM.md` - System overview
- `TEMPLATE_VALIDATION_GUIDE.md` - Validation details

### **3. File Structure**

```
ThreatGPT/
├── config.yaml                    # Main configuration
├── templates/                     # Template directory
│   ├── executive_phishing.yaml
│   ├── finance_bec.yaml
│   └── ...
├── src/threatgpt/
│   ├── config/
│   │   ├── models.py              # Schema definitions
│   │   └── yaml_loader.py         # Validation engine
│   └── cli/
│       ├── templates.py           # Template management CLI
│       └── ...
├── generated_content/             # Simulation outputs
├── logs/                         # System logs
└── docs/                         # Documentation
```

### **4. Environment Setup**

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENROUTER_API_KEY="your-api-key"

# Verify installation
python -m src.threatgpt.cli.main templates health
```

### **5. Support Resources**

- **Documentation**: `PROFESSIONAL_TEMPLATE_SYSTEM.md`
- **Validation Guide**: `TEMPLATE_VALIDATION_GUIDE.md`
- **Example Templates**: `templates/` directory
- **Schema Definitions**: `src/threatgpt/config/models.py`
- **CLI Help**: `python -m src.threatgpt.cli.main --help`

---

## 🎯 **Summary**

This manual provides comprehensive guidance for:

✅ **Creating Templates**: Interactive wizard, cloning, and manual creation  
✅ **Configuration Management**: System settings, environment variables, and hierarchies  
✅ **Validation System**: Multi-layer validation with auto-fix capabilities  
✅ **Best Practices**: Development workflow, quality standards, and security  
✅ **Troubleshooting**: Common issues, debug mode, and recovery procedures  
✅ **Advanced Features**: Custom validation, inheritance, and CI/CD integration  

The ThreatGPT system maintains an **81.8% validation success rate** with professional-grade tooling that ensures template quality while providing powerful development capabilities.

---

*ThreatGPT Template Creation, Configuration & Validation Manual - Professional Standards Maintained* 📖