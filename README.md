# ThreatGPT: AI-Powered Threat Simulation Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Tests](https://github.com/threatgpt/threatgpt/workflows/Tests/badge.svg)](https://github.com/threatgpt/threatgpt/actions)

ThreatGPT is a production-grade cybersecurity threat simulation platform that leverages Large Language Models (LLMs) to generate realistic, context-aware threat scenarios for training, awareness, and red teaming activities.

## 🚀 Features

- **Multi-LLM Support**: ✅ Integrates with OpenRouter, OpenAI GPT-4 and Anthropic Claude
- **YAML-Based Configuration**: ✅ Define threat scenarios using intuitive YAML schemas  
- **Production-Ready Core**: ✅ Scalable simulation engine with proper data models
- **CLI Interface**: ✅ Command-line tool for scenario management and execution
- **REST API**: ✅ FastAPI-based REST endpoints for enterprise integration
- **Safety Framework**: 🚧 Built-in content filtering and compliance (planned)
- **Analytics & Reporting**: 🚧 Comprehensive logging & metrics (planned)

## 🏗️ Architecture

```
ThreatGPT Platform
├── CLI Interface          ✅ Command-line tool for direct usage
├── REST API              ✅ FastAPI-based enterprise integration
├── Core Simulation       ✅ Threat scenario orchestration engine
├── LLM Integration       ✅ Multi-provider LLM abstraction layer
├── Configuration System  ✅ YAML-based scenario management
├── Safety Module         🚧 Content filtering & compliance (planned)
└── Analytics & Reporting 🚧 Comprehensive metrics (planned)
```

### Current Implementation Status

- **✅ Complete**: Core simulation engine, LLM integration, configuration system, CLI, and API
- **🚧 In Progress**: Safety and compliance modules, advanced analytics
- **📋 Planned**: Enterprise authentication, advanced reporting, MITRE ATT&CK mapping

## 📋 Quick Start

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip
- Redis (for caching)
- PostgreSQL (for data persistence)

### Installation

```bash
# Clone the repository
git clone https://github.com/Thundastormgod/ThreatGpt.git
cd ThreatGpt

# Install with Poetry (recommended)
poetry install

# Or install with pip
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Basic Usage

```bash
# Activate virtual environment (if using Poetry)
poetry shell

# Run a simple phishing simulation
threatgpt simulate --scenario my_scenario.yaml

# List available threat templates
threatgpt templates --list

# Validate a configuration file
threatgpt validate --config my_scenario.yaml

# Generate content directly
threatgpt llm generate --prompt "Create a phishing email" --type phishing
```

### Direct API Usage

```bash
# Generate threat content via API
curl -X POST "http://localhost:8000/llm/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Create a realistic phishing email targeting executives",
       "scenario_type": "phishing",
       "max_tokens": 500
     }'

# Create and run a simulation
curl -X POST "http://localhost:8000/scenarios" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Executive Phishing Campaign",
       "threat_type": "phishing",
       "description": "Sophisticated phishing attack targeting C-level executives",
       "severity": "high"
     }'
```

## 🔧 Development

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/threatgpt/threatgpt.git
cd threatgpt

# Install development dependencies
poetry install --with dev,test

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=src/threatgpt --cov-report=html
```

### Code Quality

We maintain high code quality standards:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Security scanning
bandit -r src/

# Run all checks
pre-commit run --all-files
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m e2e          # End-to-end tests only

# Run with coverage
pytest --cov=src/threatgpt --cov-report=html --cov-report=term
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t threatgpt:latest .

# Run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale api=3
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=threatgpt

# View logs
kubectl logs -f deployment/threatgpt-api
```

## 📚 Documentation

- **[API Documentation](docs/api/)** - REST API reference
- **[User Guide](docs/user-guide/)** - Comprehensive usage guide
- **[Developer Guide](docs/developer/)** - Contributing and development
- **[Configuration Reference](docs/configuration/)** - Schema documentation
- **[Security Guide](docs/security/)** - Security best practices

## 🛡️ Security & Ethics

ThreatGPT is designed with security and ethical considerations at its core:

- **Content Filtering**: Real-time analysis prevents harmful content generation
- **Audit Logging**: Comprehensive tracking of all simulation activities
- **GDPR Compliance**: Built-in data protection and privacy controls
- **Ethical Guidelines**: Clear usage policies and responsible AI practices

### Responsible Use

This tool is intended for:
- ✅ Cybersecurity training and awareness
- ✅ Red team exercises and penetration testing
- ✅ Security research and education
- ✅ Compliance testing and validation

This tool should NOT be used for:
- ❌ Actual malicious activities
- ❌ Unauthorized testing or attacks
- ❌ Harassment or harmful content generation
- ❌ Bypassing security controls

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `pytest`
5. Run code quality checks: `pre-commit run --all-files`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MITRE ATT&CK framework for attack technique mapping
- OpenAI and Anthropic for LLM capabilities
- The cybersecurity community for inspiration and feedback

## 📞 Support

- **Documentation**: [https://threatgpt.readthedocs.io](https://threatgpt.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/Thundastormgod/ThreatGpt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Thundastormgod/ThreatGpt/discussions)
- **Email**: okino007@gmail.com

---

**⚠️ Disclaimer**: ThreatGPT is a simulation tool for educational and authorized testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.