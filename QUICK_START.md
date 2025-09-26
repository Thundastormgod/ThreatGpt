# ThreatGPT - Quick Start Guide 🚀

Welcome to ThreatGPT! This guide will get you up and running in minutes.

## 📋 Prerequisites

- Python 3.11+ installed
- OpenRouter API account and key
- Windows/Linux/macOS terminal access

## 🔧 Setup Instructions

### 1. Clone and Install
```bash
git clone <your-repo-url>
cd ThreatGpt
pip install -e .
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
# OpenRouter Configuration (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional Configuration
THREATGPT_CONFIG_PATH=./config.yaml
THREATGPT_LOG_LEVEL=INFO
THREATGPT_SAFETY_MODE=enabled
```

### 3. Verify Installation
```bash
threatgpt --help
```

## 🎯 Quick Test Run

### Run Your First Simulation
```bash
# List available templates
threatgpt templates list

# Run IT Help Desk simulation
threatgpt simulate --scenario "templates/it_helpdesk_impersonation.yaml"

# View results
threatgpt logs list
```

## 📁 Generated Content Locations

- **Simulation Logs**: `logs/simulations/successful/`
- **Organized Content**: `generated_content/`
- **Training Materials**: `generated_content/training_materials/`
- **Phone Scripts**: `generated_content/phone_scripts/`
- **Email Templates**: `generated_content/email_templates/`

## 📖 Available Templates

- `it_helpdesk_impersonation.yaml` - Social engineering phone calls
- `executive_phishing.yaml` - Spear-phishing campaigns
- `finance_bec.yaml` - Business email compromise
- `supply_chain_compromise.yaml` - Supply chain attacks

## 🛠️ Useful Commands

```bash
# System status
threatgpt status

# List all simulations
threatgpt logs list

# View specific simulation
threatgpt logs show <simulation-id>

# Extract content to organized folders
python extract_content.py

# Run infrastructure audit
python infrastructure_audit.py
```

## 🎉 That's It!

You're ready to generate professional cybersecurity training content with AI! 

For detailed documentation, see `CONTENT_STORAGE_GUIDE.md`.