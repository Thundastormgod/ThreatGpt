# 🛡️ Template Validation Guide for ThreatGPT Team Members

## 📋 **Overview**

The ThreatGPT codebase implements a comprehensive multi-layer validation system for threat scenario templates and configurations. This guide explains how team members can validate their templates and configurations effectively.

## 🔍 **Validation Architecture**

### **1. Core Validation Components**

#### **🎯 YAMLConfigLoader (`src/threatgpt/config/yaml_loader.py`)**
- **Purpose**: Primary validation engine with comprehensive error handling
- **Features**: 
  - YAML syntax validation
  - Pydantic schema validation
  - Custom error formatting
  - Batch directory validation
  - Safe YAML loading with security protections

#### **🏗️ Pydantic Models (`src/threatgpt/config/models.py`)**
- **Purpose**: Strict schema definitions for type safety
- **Components**:
  - `ThreatScenario`: Main scenario model
  - `TargetProfile`: Target demographic validation
  - `BehavioralPattern`: Attack pattern validation
  - Enums for controlled vocabularies (ThreatType, DeliveryVector, etc.)

#### **🖥️ CLI Validation Tools (`src/threatgpt/cli/templates.py`)**
- **Purpose**: User-friendly validation commands
- **Features**: Professional validation, health monitoring, auto-fix capabilities

## 🚀 **Validation Methods for Team Members**

### **Method 1: Quick Individual Template Validation**

```bash
# Validate a single template with detailed output
python -m src.threatgpt.cli.main templates show <template_name> --validate

# Example:
python -m src.threatgpt.cli.main templates show executive_phishing --validate
```

**Output Example:**
```
✅ Template validation successful!

🎯 Executive Spear-Phishing Campaign
📝 Advanced spear-phishing attack targeting C-level executives
📄 File: executive_phishing.yaml

📊 Basic Information:
    Threat Type: Spear Phishing
    Delivery Vector: Email
    Difficulty Level: 8/10
    Estimated Duration: 45 minutes
```

### **Method 2: Professional Validation Suite**

```bash
# Comprehensive validation with professional reporting
python -m src.threatgpt.cli.main templates validate-pro

# With auto-fix capabilities
python -m src.threatgpt.cli.main templates validate-pro --auto-fix --backup
```

**Features:**
- ✅ **Success Rate Analysis**: Shows validation percentage (currently 81.8%)
- 📊 **Detailed Error Reports**: Specific field-level validation errors
- 🔧 **Auto-Fix Suggestions**: Intelligent template repair
- 📈 **Threat Type Distribution**: Coverage analysis

### **Method 3: Ecosystem Health Assessment**

```bash
# Overall template ecosystem health check
python -m src.threatgpt.cli.main templates health

# Template statistics and distribution
python -m src.threatgpt.cli.main templates stats
```

**Health Scoring (100-point system):**
- **Validation Success (40pts)**: Schema compliance rate
- **Template Diversity (30pts)**: Threat type coverage
- **Template Count (20pts)**: Library completeness 
- **Error-free Score (10pts)**: Critical error penalty

### **Method 4: Batch Directory Validation**

```bash
# List all templates with validation
python -m src.threatgpt.cli.main templates list-all --validate

# Comprehensive validation report with JSON output
python -m src.threatgpt.cli.main templates validate-all --output-dir reports/
```

### **Method 5: Programmatic Validation (Python API)**

```python
from src.threatgpt.config.yaml_loader import YAMLConfigLoader
from pathlib import Path

# Initialize validator
loader = YAMLConfigLoader(strict_mode=True)

# Validate single template
try:
    scenario = loader.load_and_validate_scenario("templates/my_template.yaml")
    print(f"✅ Valid: {scenario.metadata.name}")
except Exception as e:
    print(f"❌ Invalid: {e}")

# Validate entire directory
results = loader.validate_config_directory("templates/")
print(f"Success Rate: {results['valid_files']}/{results['total_files']}")
```

## ⚠️ **Common Validation Errors and Solutions**

### **1. Schema Validation Errors**

**Error:** `threat_type: Input should be 'phishing', 'spear_phishing', ...`

**Solution:**
```yaml
# ❌ Invalid
threat_type: "hybrid_attack"

# ✅ Valid  
threat_type: "spear_phishing"
```

**Available Values:**
- `phishing`, `spear_phishing`, `malware`, `ransomware`
- `social_engineering`, `insider_threat`, `advanced_persistent_threat`
- `credential_harvesting`, `watering_hole`, `supply_chain`
- `physical_security`, `voice_phishing`, `sms_phishing`

### **2. Enum Validation Errors**

**Error:** `seniority: Input should be 'entry', 'junior', 'mid', ...`

**Solution:**
```yaml
target_profile:
  # ❌ Invalid
  seniority: "middle_manager"
  
  # ✅ Valid
  seniority: "mid"
```

**Valid Seniority Levels:**
- `entry`, `junior`, `mid`, `senior`, `lead`
- `manager`, `director`, `vice_president`, `senior_vice_president`
- `executive`, `c_level`

### **3. Missing Required Fields**

**Error:** `difficulty_level: Field required`

**Solution:**
```yaml
# ❌ Missing required fields
metadata:
  name: "My Scenario"

# ✅ Complete required fields
metadata:
  name: "My Scenario"
  description: "Detailed description"
  version: "1.0.0"
difficulty_level: 5
estimated_duration: 30
```

### **4. Type Validation Errors**

**Error:** `max_iterations: Input should be a valid integer`

**Solution:**
```yaml
simulation_parameters:
  # ❌ String value
  max_iterations: "3"
  
  # ✅ Integer value
  max_iterations: 3
```

## 🔧 **Auto-Fix Capabilities**

The validation system includes intelligent auto-fix features:

### **Automatic Fixes Applied:**
- **Enum Mapping**: `hybrid_attack` → `advanced_persistent_threat`
- **Type Conversion**: String numbers to integers
- **Field Removal**: Unsupported fields automatically removed
- **Default Values**: Missing fields populated with defaults
- **Format Standardization**: Boolean and timestamp normalization

### **Running Auto-Fix:**
```bash
# Fix all templates with backup creation
python -m src.threatgpt.cli.main templates validate-pro --auto-fix --backup

# Using standalone fixer
python fix_templates.py
```

**Safety Features:**
- 🔒 **Automatic Backups**: Original files preserved
- 📝 **Fix Documentation**: All changes logged in file headers
- ⚡ **Validation Pre-check**: Only valid fixes applied
- 🎯 **Selective Fixing**: Problematic fields only

## 📊 **Current Validation Status**

### **Template Ecosystem Health**
- **Total Templates**: 22
- **Valid Templates**: 18 (81.8% success rate)
- **Health Score**: 86.4/100 (Good status)
- **Threat Type Coverage**: 5+ categories (Excellent diversity)

### **Common Issues Resolved**
1. ✅ **10 templates auto-fixed** with enum and type corrections
2. ✅ **Schema compliance** improved from ~73% to 82%
3. ✅ **Backup safety** implemented for all modifications
4. ✅ **Professional reporting** with detailed error context

## 🎯 **Best Practices for Team Members**

### **Template Development Workflow**
1. **Start with Existing Template**: Clone a working template
   ```bash
   python -m src.threatgpt.cli.main templates clone executive_phishing my_new_scenario
   ```

2. **Use Interactive Creator**: Professional wizard for new templates
   ```bash
   python -m src.threatgpt.cli.main templates create
   ```

3. **Validate Early and Often**: Check validation during development
   ```bash
   python -m src.threatgpt.cli.main templates show my_template --validate
   ```

4. **Run Health Checks**: Monitor ecosystem before commits
   ```bash
   python -m src.threatgpt.cli.main templates health
   ```

### **CI/CD Integration Recommendations**
```bash
# Pre-commit validation hook
python -m src.threatgpt.cli.main templates validate-pro --auto-fix

# Build pipeline validation
python -m src.threatgpt.cli.main templates validate-all --output-dir ci-reports/
```

### **Team Collaboration Standards**
- ✅ **Always validate** before committing templates
- 📝 **Document changes** in metadata.updated_at
- 🔍 **Review health reports** regularly
- 🎯 **Maintain 85%+** validation success rate
- 🛡️ **Use auto-fix** for standard corrections
- 📊 **Monitor ecosystem** statistics

## 🚀 **Advanced Validation Features**

### **Custom Validation Rules**
- **MITRE ATT&CK Validation**: Technique ID format checking
- **Timestamp Validation**: ISO format enforcement
- **Reference URL Validation**: Link format verification
- **Content Length Limits**: Optimized for performance
- **Cross-field Dependencies**: Logical consistency checks

### **Validation Modes**
- **Strict Mode**: Full schema enforcement (default)
- **Lenient Mode**: Warning-only validation
- **Development Mode**: Enhanced error context
- **Production Mode**: Performance optimized

### **Error Recovery**
- **Graceful Degradation**: Partial validation for corrupted files
- **Context Preservation**: Original structure maintained
- **Incremental Fixing**: Step-by-step error resolution
- **Rollback Support**: Easy reversion to backup versions

---

## 📞 **Support and Resources**

### **Quick Reference Commands**
```bash
# Single template validation
templates show <name> --validate

# Professional validation suite  
templates validate-pro [--auto-fix] [--backup]

# Ecosystem health check
templates health

# Statistics and distribution
templates stats

# Create new template
templates create

# Clone existing template
templates clone <source> <new_name>
```

### **Documentation Files**
- `PROFESSIONAL_TEMPLATE_SYSTEM.md` - Complete system overview
- `src/threatgpt/config/models.py` - Schema definitions
- `src/threatgpt/config/yaml_loader.py` - Validation engine
- `templates/` - Example templates and patterns

This validation system ensures professional-grade template quality while providing team members with powerful tools for development, validation, and maintenance of the ThreatGPT threat scenario library.

---

*ThreatGPT Template Validation System - Professional Standards Maintained* 🛡️