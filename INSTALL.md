# 🚀 Quick Setup Guide

Get ThreatGPT running in 5 minutes!

## Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **API Key** from [OpenRouter](https://openrouter.ai/keys) (recommended) or [OpenAI](https://platform.openai.com/api-keys)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Thundastormgod/ThreatGpt.git
cd ThreatGpt
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Install ThreatGPT
```bash
pip install -e .
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API key
# Windows: notepad .env
# Linux/Mac: nano .env
```

Add your API key to `.env`:
```env
# OpenRouter (Recommended - supports 200+ models)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Alternative providers
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

## Quick Test

### Verify Installation
```bash
threatgpt status
```
Expected output: ✅ All systems operational

### List Available Scenarios
```bash
threatgpt templates list-all
```

### Run Your First Simulation
```bash
# Quick phishing scenario (30 seconds)
threatgpt simulate --scenario "templates/it_helpdesk_impersonation.yaml"

# View results
threatgpt logs list
```

### Extract Generated Content
```bash
# Organize all content into markdown files
python extract_content.py

# View organized content
dir generated_content
```

## 🎯 What You Get

After setup, you'll have:

- **📧 Email Templates**: Professional phishing examples
- **📞 Phone Scripts**: Social engineering call guides  
- **📚 Training Materials**: Security awareness content
- **🎭 Scenarios**: Complete attack simulations
- **📊 Reports**: Analysis and metrics

## Next Steps

### Explore Available Commands
```bash
threatgpt --help                    # All commands
threatgpt templates show executive  # View scenario details
threatgpt logs stats               # Usage statistics
```

### Run Advanced Scenarios
```bash
# Business Email Compromise (2-3 minutes)
threatgpt simulate --scenario "templates/finance_bec.yaml"

# Supply Chain Attack (5-7 minutes)  
threatgpt simulate --scenario "templates/supply_chain_compromise.yaml"
```

### Customize Scenarios
Edit templates in `templates/` folder to match your organization:
- Change company names and roles
- Adjust difficulty levels
- Add industry-specific context

## 🛠️ Development Setup

For contributors:
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Check code quality
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Troubleshooting

### Common Issues

**"threatgpt command not found"**
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstall in development mode
pip install -e .
```

**"API key not working"**
```bash
# Check .env file exists and has correct key
cat .env  # Linux/Mac
type .env  # Windows

# Test API connection
python -c "import os; print('API Key:', os.getenv('OPENROUTER_API_KEY')[:20] + '...')"
```

**"Simulation fails/timeouts"**
```bash
# Check internet connection
# Verify API key has credits/quota
# Try a shorter scenario first
threatgpt simulate --scenario "templates/it_helpdesk_impersonation.yaml"
```

### Get Help

- **GitHub Issues**: [Report bugs](https://github.com/Thundastormgod/ThreatGpt/issues)
- **Discussions**: [Ask questions](https://github.com/Thundastormgod/ThreatGpt/discussions)
- **Email**: okino007@gmail.com

## System Requirements

- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for API calls

---

**🎉 Ready to simulate threats and enhance cybersecurity training!**

Next: Check out [CONTENT_STORAGE_GUIDE.md](CONTENT_STORAGE_GUIDE.md) to understand how your generated content is organized.