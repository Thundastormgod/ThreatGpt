# ThreatGPT Scenario Templates

This directory contains example threat scenario configurations demonstrating the full capabilities of the ThreatGPT YAML schema.

## Template Categories

### 📧 Email-Based Threats
- **executive_phishing.yaml** - Sophisticated spear-phishing targeting C-level executives
- **credential_harvesting.yaml** - Fake login page for credential collection
- **finance_bec.yaml** - Business Email Compromise targeting finance teams

### 📱 Mobile & SMS Threats
- **executive_smishing.yaml** - SMS phishing targeting mobile executives
- **covid_scam.yaml** - Health-themed mobile scam campaign

### 🎯 Social Engineering
- **it_helpdesk_impersonation.yaml** - Help desk impersonation for access
- **vendor_impersonation.yaml** - Third-party vendor impersonation
- **new_employee_pretext.yaml** - New employee onboarding pretext

### 🔒 Advanced Persistent Threats
- **supply_chain_compromise.yaml** - Software supply chain attack simulation
- **watering_hole_attack.yaml** - Industry website compromise

### 👥 Insider Threats
- **disgruntled_employee.yaml** - Malicious insider scenario
- **privilege_escalation.yaml** - Internal privilege escalation

## Usage

1. **Validation**: Use `threatgpt validate <template.yaml>` to check schema compliance
2. **Simulation**: Use `threatgpt simulate <template.yaml>` to run the scenario
3. **Customization**: Copy and modify templates for your specific organization

## Schema Features Demonstrated

Each template showcases different aspects of the YAML schema:
- **Comprehensive Metadata**: Version control, authorship, tags
- **Target Profiling**: Role-based targeting with behavioral analysis
- **MITRE ATT&CK Integration**: Technique and tactic mapping
- **Behavioral Patterns**: Psychological triggers and social engineering tactics
- **Simulation Parameters**: Adaptive execution controls
- **Compliance Controls**: Audit logging and content filtering

## Best Practices

- Start with simpler scenarios and gradually increase complexity
- Always validate templates before production use
- Customize target profiles to match your organization
- Review MITRE ATT&CK mappings for accuracy
- Test scenarios in controlled environments first