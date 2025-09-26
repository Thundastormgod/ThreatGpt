# ThreatGPT CLI Reference Guide

**Version:** 1.0.0  
**Last Updated:** September 26, 2025  

This document provides a complete reference for all ThreatGPT CLI commands and their options.

---

## 🚀 Quick Start

```bash
# Basic usage
python -m src.threatgpt.cli.main --help

# With configuration and verbose output
python -m src.threatgpt.cli.main --config config.yaml --verbose <command>
```

---

## 📋 Global Options

Available for all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--version` | | Show version and exit |
| `--verbose` | `-v` | Enable verbose output |
| `--config TEXT` | `-c` | Configuration file path |
| `--help` | | Show help message |

---

## 🎯 Main Command Groups

### 1. **simulate** - Execute Threat Simulations

Execute threat simulation scenarios with comprehensive options.

```bash
python -m src.threatgpt.cli.main simulate [OPTIONS]
```

#### Options:
| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--scenario TEXT` | `-s` | **Required** | Path to threat scenario configuration file |
| `--target TEXT` | `-t` | Optional | Target profile specification |
| `--output [json\|yaml\|report]` | `-o` | Optional | Output format |
| `--dry-run` | | Flag | Validate configuration without executing |
| `--preview` | | Flag | Show detailed scenario preview before execution |

#### Examples:
```bash
# Basic simulation execution
python -m src.threatgpt.cli.main simulate -s templates/executive_phishing.yaml

# Dry run (validation only)
python -m src.threatgpt.cli.main simulate -s templates/finance_bec.yaml --dry-run

# With preview and custom output
python -m src.threatgpt.cli.main simulate -s templates/it_helpdesk_impersonation.yaml --preview --output json

# With custom target profile
python -m src.threatgpt.cli.main simulate -s templates/executive_phishing.yaml -t "CEO,Technology,Senior"
```

---

### 2. **templates** - Manage Scenario Templates

Comprehensive template management with validation and detailed viewing.

```bash
python -m src.threatgpt.cli.main templates [COMMAND] [OPTIONS]
```

#### Subcommands:

##### `list-all` - List All Templates
```bash
python -m src.threatgpt.cli.main templates list-all [OPTIONS]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--validate` | `-v` | Validate all templates against schema |
| `--format [table\|tree\|simple]` | `-f` | Output format |

##### `show` - Show Template Details
```bash
python -m src.threatgpt.cli.main templates show [TEMPLATE_NAME]
```

##### `validate-all` - Validate All Templates
```bash
python -m src.threatgpt.cli.main templates validate-all
```

##### `copy` - Copy Template
```bash
python -m src.threatgpt.cli.main templates copy [SOURCE] [DESTINATION]
```

#### Examples:
```bash
# List all templates
python -m src.threatgpt.cli.main templates list-all

# List with validation
python -m src.threatgpt.cli.main templates list-all --validate --format table

# Show specific template
python -m src.threatgpt.cli.main templates show executive_phishing.yaml

# Validate all templates
python -m src.threatgpt.cli.main templates validate-all

# Copy template
python -m src.threatgpt.cli.main templates copy executive_phishing.yaml my_custom_phishing.yaml
```

---

### 3. **llm** - LLM Integration Management

Manage and test Large Language Model integrations.

```bash
python -m src.threatgpt.cli.main llm [COMMAND] [OPTIONS]
```

#### Subcommands:

##### `test-providers` - Test LLM Providers
```bash
python -m src.threatgpt.cli.main llm test-providers
```

##### `generate` - Generate Threat Content
```bash
python -m src.threatgpt.cli.main llm generate [OPTIONS] SCENARIO_FILE
```

**Options:**
| Option | Description |
|--------|-------------|
| `--content-type [email_phishing\|sms_phishing\|voice_script\|social_media_post\|document_lure\|web_page\|chat_message\|pretext_scenario]` | Type of content to generate |
| `--provider [openai\|anthropic\|openrouter]` | LLM provider to use |
| `--model TEXT` | Specific model to use |
| `--variants INTEGER` | Number of variants to generate |
| `--output PATH` | Output file path |
| `--openai-key TEXT` | OpenAI API key |
| `--anthropic-key TEXT` | Anthropic API key |
| `--openrouter-key TEXT` | OpenRouter API key |

##### `list-templates` - List Prompt Templates
```bash
python -m src.threatgpt.cli.main llm list-templates
```

##### `show-template` - Show Template Details
```bash
python -m src.threatgpt.cli.main llm show-template [TEMPLATE_NAME]
```

#### Examples:
```bash
# Test all configured providers
python -m src.threatgpt.cli.main llm test-providers

# Generate phishing email content
python -m src.threatgpt.cli.main llm generate templates/executive_phishing.yaml --content-type email_phishing --variants 3

# Generate with specific provider
python -m src.threatgpt.cli.main llm generate templates/finance_bec.yaml --provider openrouter --model "anthropic/claude-3-haiku"

# List available prompt templates
python -m src.threatgpt.cli.main llm list-templates

# Show specific template
python -m src.threatgpt.cli.main llm show-template phishing_email
```

---

### 4. **validate** - Configuration Validation

Validate threat scenario configurations against YAML schema.

```bash
python -m src.threatgpt.cli.main validate [OPTIONS] [CONFIG_FILE]
```

#### Options:
| Option | Short | Description |
|--------|-------|-------------|
| `--schema-only` | | Validate schema only, skip semantic validation |
| `--directory TEXT` | `-d` | Validate all YAML files in directory |
| `--strict` | | Enable strict validation mode |

#### Examples:
```bash
# Validate single file
python -m src.threatgpt.cli.main validate templates/executive_phishing.yaml

# Validate all files in directory
python -m src.threatgpt.cli.main validate --directory templates/

# Schema-only validation
python -m src.threatgpt.cli.main validate --schema-only templates/finance_bec.yaml

# Strict validation mode
python -m src.threatgpt.cli.main validate --strict templates/supply_chain_compromise.yaml
```

---

### 5. **status** - System Status

Show ThreatGPT system status and health information.

```bash
python -m src.threatgpt.cli.main status
```

#### Examples:
```bash
# Show system status
python -m src.threatgpt.cli.main status

# Verbose status with configuration details
python -m src.threatgpt.cli.main --verbose status
```

---

### 6. **deploy** - Deployment & Campaign Management

Manage threat deployment and campaign operations.

```bash
python -m src.threatgpt.cli.main deploy [COMMAND] [OPTIONS]
```

#### Subcommands:

##### `campaign` - Deploy Campaign
```bash
python -m src.threatgpt.cli.main deploy campaign [OPTIONS]
```

##### `monitor` - Monitor Campaign
```bash
python -m src.threatgpt.cli.main deploy monitor [CAMPAIGN_ID]
```

##### `status` - Campaign Status
```bash
python -m src.threatgpt.cli.main deploy status [CAMPAIGN_ID]
```

##### `cancel` - Cancel Campaign
```bash
python -m src.threatgpt.cli.main deploy cancel [CAMPAIGN_ID]
```

##### `platforms` - List Integration Platforms
```bash
python -m src.threatgpt.cli.main deploy platforms
```

##### `templates` - Manage Deployment Templates
```bash
python -m src.threatgpt.cli.main deploy templates
```

#### Examples:
```bash
# List available platforms
python -m src.threatgpt.cli.main deploy platforms

# Deploy campaign
python -m src.threatgpt.cli.main deploy campaign --scenario templates/executive_phishing.yaml

# Monitor active campaign
python -m src.threatgpt.cli.main deploy monitor abc123-def456

# Get campaign status
python -m src.threatgpt.cli.main deploy status abc123-def456

# Cancel campaign
python -m src.threatgpt.cli.main deploy cancel abc123-def456
```

---

### 7. **intel** - Intelligence Gathering

OSINT and intelligence reconnaissance capabilities.

```bash
python -m src.threatgpt.cli.main intel [COMMAND] [OPTIONS]
```

#### Subcommands:

##### `gather` - Gather Intelligence
```bash
python -m src.threatgpt.cli.main intel gather [OPTIONS] TARGET
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--types [profile\|company\|social_media\|threat_intel\|domain]` | `-t` | Types of intelligence to gather |
| `--output PATH` | `-o` | Output file for intelligence results |
| `--format [json\|table\|report]` | `-f` | Output format |
| `--force-refresh` | | Force fresh gathering, ignore cache |

##### `enhance` - Enhance Scenario with Intelligence
```bash
python -m src.threatgpt.cli.main intel enhance [SCENARIO_FILE]
```

##### `sources` - List Intelligence Sources
```bash
python -m src.threatgpt.cli.main intel sources
```

##### `cache` - Manage Intelligence Cache
```bash
python -m src.threatgpt.cli.main intel cache [clear|status|size]
```

#### Examples:
```bash
# Gather intelligence on target
python -m src.threatgpt.cli.main intel gather john.doe@company.com

# Gather specific types of intelligence
python -m src.threatgpt.cli.main intel gather --types profile,company,social_media john.doe@company.com

# Enhanced intelligence gathering with report output
python -m src.threatgpt.cli.main intel gather -t profile,domain -f report -o intelligence_report.html company.com

# Enhance scenario with real-time intelligence
python -m src.threatgpt.cli.main intel enhance templates/executive_phishing.yaml

# List available intelligence sources
python -m src.threatgpt.cli.main intel sources

# Clear intelligence cache
python -m src.threatgpt.cli.main intel cache clear
```

---

### 8. **report** - Generate Reports

Generate comprehensive simulation reports.

```bash
python -m src.threatgpt.cli.main report [OPTIONS]
```

#### Options:
| Option | Short | Description |
|--------|-------|-------------|
| `--simulation-id TEXT` | | **Required** - Simulation ID to generate report for |
| `--format [pdf\|html\|json\|csv]` | | Report format |
| `--output-file TEXT` | `-o` | Output file path |

#### Examples:
```bash
# Generate HTML report
python -m src.threatgpt.cli.main report --simulation-id abc123-def456 --format html

# Generate PDF report with custom output path
python -m src.threatgpt.cli.main report --simulation-id abc123-def456 --format pdf -o reports/simulation_report.pdf

# Generate JSON data export
python -m src.threatgpt.cli.main report --simulation-id abc123-def456 --format json -o simulation_data.json

# Generate CSV for analysis
python -m src.threatgpt.cli.main report --simulation-id abc123-def456 --format csv
```

---

### 9. **safety** - Safety & Compliance

Safety and compliance checking tools.

```bash
python -m src.threatgpt.cli.main safety [OPTIONS]
```

#### Options:
| Option | Description |
|--------|-------------|
| `--check-content TEXT` | Check content against safety policies |
| `--policy TEXT` | Specific policy to check against |

#### Examples:
```bash
# Check content safety
python -m src.threatgpt.cli.main safety --check-content "suspicious email content"

# Check against specific policy
python -m src.threatgpt.cli.main safety --check-content "content" --policy corporate_policy

# General safety check
python -m src.threatgpt.cli.main safety
```

---

### 10. **datasets** - Cybersecurity Dataset Management

Manage real-world cybersecurity datasets to enhance threat simulation realism.

#### 10.1 Dataset Commands

**List Available Datasets**
```bash
python -m src.threatgpt.cli.main datasets list
```

**Download and Process Datasets**
```bash
# Download specific dataset
python -m src.threatgpt.cli.main datasets download enron
python -m src.threatgpt.cli.main datasets download phishtank
python -m src.threatgpt.cli.main datasets download cert_insider

# Force re-download
python -m src.threatgpt.cli.main datasets download mitre_attack --force
```

**Check Dataset Status**
```bash
# Table format (default)
python -m src.threatgpt.cli.main datasets status

# JSON format for scripting
python -m src.threatgpt.cli.main datasets status --format json
```

**Extract Patterns for Threat Modeling**
```bash
# Email patterns by role and industry
python -m src.threatgpt.cli.main datasets patterns email --role executive --industry financial
python -m src.threatgpt.cli.main datasets patterns email --role employee --industry healthcare

# Phishing patterns by target sector
python -m src.threatgpt.cli.main datasets patterns phishing --industry banking
python -m src.threatgpt.cli.main datasets patterns phishing --industry technology

# Insider threat patterns
python -m src.threatgpt.cli.main datasets patterns insider-threat --role administrator
python -m src.threatgpt.cli.main datasets patterns insider-threat --role analyst

# Get patterns in JSON format
python -m src.threatgpt.cli.main datasets patterns email --role manager --format json
```

**Clear Pattern Cache**
```bash
python -m src.threatgpt.cli.main datasets clear-cache
```

#### 10.2 Available Datasets

| Dataset | Type | Description | Size | Use Cases |
|---------|------|-------------|------|-----------|
| **Enron Email Corpus** | `enron` | 500K+ executive emails | ~1.2GB | Email style patterns, phishing templates |
| **PhishTank Database** | `phishtank` | Real-time phishing URLs | ~50MB | Domain patterns, URL analysis |
| **CERT Insider Threat** | `cert_insider` | Behavioral patterns | ~10MB | Insider threat modeling |
| **LANL Authentication** | `lanl_auth` | Network auth logs | ~500MB | Authentication anomalies |
| **MITRE ATT&CK** | `mitre_attack` | TTPs framework | ~25MB | Attack pattern modeling |

#### 10.3 Pattern Integration Examples

**Enhanced Phishing Simulation**
```bash
# Extract email patterns for target role
python -m src.threatgpt.cli.main datasets patterns email --role executive --industry finance

# Get phishing domain patterns
python -m src.threatgpt.cli.main datasets patterns phishing --industry banking

# Use patterns in simulation
python -m src.threatgpt.cli.main simulate --scenario phishing_executive.yaml --enhance-with-datasets
```

**Insider Threat Scenario Enhancement**
```bash
# Get insider threat behavioral patterns
python -m src.threatgpt.cli.main datasets patterns insider-threat --role database_admin

# Integrate with authentication patterns
python -m src.threatgpt.cli.main datasets patterns authentication --time-period after_hours

# Run enhanced insider threat simulation
python -m src.threatgpt.cli.main simulate --scenario insider_threat.yaml --datasets-context
```

#### 10.4 Dataset Privacy & Ethics

- **Data Sanitization**: Personal information is automatically filtered out
- **Ethical Usage**: Datasets used only for defensive security training
- **Compliance**: GDPR, CCPA, and SOC2 compliant data handling
- **Storage**: Local storage with encryption at rest

---

## 🔧 Advanced Usage Patterns

### Environment Variables

Set API keys and configuration via environment variables:

```bash
# LLM Provider API Keys
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export OPENROUTER_API_KEY="your_openrouter_key"

# Configuration
export THREATGPT_CONFIG_PATH="./config.yaml"
export THREATGPT_LOG_LEVEL="INFO"
```

### Configuration File Usage

```bash
# Use custom configuration file
python -m src.threatgpt.cli.main --config ./custom_config.yaml simulate -s templates/phishing.yaml

# Verbose output with configuration
python -m src.threatgpt.cli.main --verbose --config ./prod_config.yaml status
```

### Batch Operations

```bash
# Validate all templates
python -m src.threatgpt.cli.main templates validate-all

# Validate entire directory
python -m src.threatgpt.cli.main validate --directory ./scenarios/

# Generate multiple content variants
python -m src.threatgpt.cli.main llm generate templates/phishing.yaml --variants 5 --output batch_content.json
```

### Pipeline Integration

```bash
# JSON output for pipeline processing
python -m src.threatgpt.cli.main simulate -s templates/phishing.yaml --output json | jq '.results'

# Dry run validation in CI/CD
python -m src.threatgpt.cli.main simulate -s templates/*.yaml --dry-run

# Status check for monitoring
python -m src.threatgpt.cli.main status --format json
```

---

## 📊 Common Workflows

### 1. **Basic Simulation Workflow**
```bash
# 1. Validate template
python -m src.threatgpt.cli.main validate templates/executive_phishing.yaml

# 2. Preview simulation
python -m src.threatgpt.cli.main simulate -s templates/executive_phishing.yaml --preview

# 3. Execute simulation
python -m src.threatgpt.cli.main simulate -s templates/executive_phishing.yaml

# 4. Generate report
python -m src.threatgpt.cli.main report --simulation-id [ID] --format html
```

### 2. **Template Management Workflow**
```bash
# 1. List all templates
python -m src.threatgpt.cli.main templates list-all

# 2. Show specific template details
python -m src.threatgpt.cli.main templates show executive_phishing.yaml

# 3. Copy and customize template
python -m src.threatgpt.cli.main templates copy executive_phishing.yaml my_custom.yaml

# 4. Validate new template
python -m src.threatgpt.cli.main validate my_custom.yaml
```

### 3. **LLM Provider Testing Workflow**
```bash
# 1. Test all providers
python -m src.threatgpt.cli.main llm test-providers

# 2. Generate test content
python -m src.threatgpt.cli.main llm generate templates/phishing.yaml --provider openrouter

# 3. Compare providers
python -m src.threatgpt.cli.main llm generate templates/phishing.yaml --provider openai --variants 2
python -m src.threatgpt.cli.main llm generate templates/phishing.yaml --provider anthropic --variants 2
```

### 4. **Intelligence-Enhanced Simulation**
```bash
# 1. Gather target intelligence
python -m src.threatgpt.cli.main intel gather john.doe@company.com -f report

# 2. Enhance scenario with intelligence
python -m src.threatgpt.cli.main intel enhance templates/executive_phishing.yaml

# 3. Execute enhanced simulation
python -m src.threatgpt.cli.main simulate -s enhanced_scenario.yaml
```

---

## ⚡ Quick Reference Card

### Most Common Commands:
```bash
# System status
python -m src.threatgpt.cli.main status

# List templates
python -m src.threatgpt.cli.main templates list-all

# Validate template
python -m src.threatgpt.cli.main validate templates/phishing.yaml

# Dry run simulation
python -m src.threatgpt.cli.main simulate -s templates/phishing.yaml --dry-run

# Execute simulation
python -m src.threatgpt.cli.main simulate -s templates/phishing.yaml

# Test LLM providers
python -m src.threatgpt.cli.main llm test-providers

# Generate content
python -m src.threatgpt.cli.main llm generate templates/phishing.yaml --content-type email_phishing

# List datasets
python -m src.threatgpt.cli.main datasets list

# Download dataset
python -m src.threatgpt.cli.main datasets download phishtank

# Extract email patterns
python -m src.threatgpt.cli.main datasets patterns email --role executive
```

### Emergency Commands:
```bash
# Cancel running campaign
python -m src.threatgpt.cli.main deploy cancel [CAMPAIGN_ID]

# Clear intelligence cache
python -m src.threatgpt.cli.main intel cache clear

# Safety check content
python -m src.threatgpt.cli.main safety --check-content "content"
```

---

## 🔍 Troubleshooting

### Common Issues:

1. **No LLM providers configured:**
   ```bash
   python -m src.threatgpt.cli.main llm test-providers
   # Set API keys: export OPENAI_API_KEY="your_key"
   ```

2. **Template validation errors:**
   ```bash
   python -m src.threatgpt.cli.main validate templates/your_template.yaml --strict
   ```

3. **Configuration issues:**
   ```bash
   python -m src.threatgpt.cli.main --verbose status
   ```

4. **Permission errors:**
   ```bash
   # Check file permissions and paths
   python -m src.threatgpt.cli.main templates list-all
   ```

---

*This CLI reference covers all available ThreatGPT commands as of version 1.0.0. For the latest updates, use `--help` with any command.*