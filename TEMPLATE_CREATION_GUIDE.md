# 📋 ThreatGPT Template Creation Guide

## Quick Start: Sample Template

Here's a simple, well-documented template that team members can copy and modify:

### `sample_phishing_template.yaml`

```yaml
# =============================================================================
# ThreatGPT Template - Simple Phishing Example
# =============================================================================
# This is a basic template showing all required fields and common options.
# Copy this template and modify for your specific scenario needs.

# Template Metadata (Required)
metadata:
  name: "Sample Phishing Campaign"                    # Clear, descriptive name
  description: "Basic phishing example for training"  # What this template does
  version: "1.0.0"                                   # Semantic versioning
  author: "Your Team Name"                           # Who created this
  created_at: "2025-09-28T10:00:00Z"               # ISO format timestamp
  tags: ["phishing", "training", "sample"]          # Searchable tags
  references:                                        # Optional documentation links
    - "https://attack.mitre.org/techniques/T1566/001/"

# Threat Classification (Required)
threat_type: "phishing"                             # Must be valid enum value
delivery_vector: "email"                            # How attack is delivered

# Required Fields
difficulty_level: 5                                 # 1-10 scale
estimated_duration: 30                              # Minutes

# Target Profile (Required)
target_profile:
  role: "Employee"                                   # Job role
  department: "general"                              # Department (max 50 chars)
  seniority: "mid"                                   # junior/mid/senior
  technical_level: "moderate"                        # low/moderate/high
  security_awareness_level: 5                        # 1-10 scale
  industry: "technology"                             # Industry type

# Attack Behavior (Required)
behavioral_pattern:
  psychological_triggers:                            # Must be a list
    - "urgency"
    - "authority"
    - "curiosity"
  
  social_engineering_tactics:                        # Must be a list
    - "impersonation"
    - "pretexting"
    - "time_pressure"

# Optional: Simulation Parameters
simulation_parameters:
  max_iterations: 2
  max_duration_minutes: 45
  escalation_enabled: true

# Optional: Custom Parameters (your specific settings)
custom_parameters:
  email_templates:
    subject_lines:
      - "Urgent: Account Security Alert"
      - "Action Required: Verify Your Account"
    sender_domains:
      - "security-alerts.example.com"
      - "account-verify.example.com"
```

---

## 🔧 Template Creation Steps

### Step 1: Copy the Sample Template
```bash
cp templates/sample_phishing_template.yaml templates/my_new_template.yaml
```

### Step 2: Modify Required Fields

**Must Change:**
- `metadata.name` - Your scenario name
- `metadata.description` - What your template does
- `metadata.author` - Your name/team
- `target_profile` - Match your target audience
- `behavioral_pattern` - Attack methods you want to simulate

### Step 3: Validate Your Template
```bash
threatgpt simulate --dry-run -s templates/my_new_template.yaml
```

### Step 4: Test Run
```bash
threatgpt simulate -s templates/my_new_template.yaml
```

---

## ✅ Required Fields Checklist

Every template **MUST** have these fields:

### 📝 **Metadata Section**
- [ ] `name` - Template name
- [ ] `description` - What it does
- [ ] `version` - Version number
- [ ] `author` - Creator name

### 🎯 **Core Classification**
- [ ] `threat_type` - Valid enum value (see below)
- [ ] `delivery_vector` - How attack is delivered
- [ ] `difficulty_level` - Number 1-10
- [ ] `estimated_duration` - Minutes (number)

### 👤 **Target Profile** 
- [ ] `role` - Job role
- [ ] `department` - Department (max 50 characters)
- [ ] `seniority` - junior/mid/senior
- [ ] `technical_level` - low/moderate/high
- [ ] `security_awareness_level` - Number 1-10
- [ ] `industry` - Industry type

### 🎭 **Behavioral Pattern**
- [ ] `psychological_triggers` - List of trigger types
- [ ] `social_engineering_tactics` - List of tactics

---

## 📚 Valid Enum Values

### `threat_type` Options:
- `phishing`
- `spear_phishing`
- `malware`
- `ransomware`
- `social_engineering`
- `insider_threat`
- `advanced_persistent_threat`
- `credential_harvesting`
- `watering_hole`
- `supply_chain`
- `physical_security`
- `voice_phishing` (vishing)
- `sms_phishing` (smishing)

### `delivery_vector` Options:
- `email`
- `sms`
- `phone`
- `web`
- `usb`
- `wifi`
- `physical`

### `seniority` Options:
- `junior`
- `mid` 
- `senior`

### `technical_level` Options:
- `low`
- `moderate`
- `high`

---

## 🚀 Quick Template Examples

### Email Phishing
```yaml
threat_type: "phishing"
delivery_vector: "email"
target_profile:
  role: "Office Worker"
  department: "general"
```

### SMS Phishing (Smishing)
```yaml
threat_type: "sms_phishing"
delivery_vector: "sms"
target_profile:
  role: "Mobile User"
  department: "general"
```

### Social Engineering Call
```yaml
threat_type: "social_engineering"
delivery_vector: "phone"
target_profile:
  role: "Receptionist"
  department: "admin"
```

### Business Email Compromise
```yaml
threat_type: "spear_phishing"
delivery_vector: "email"
target_profile:
  role: "Finance Manager"
  department: "finance"
  seniority: "senior"
```

---

## ⚠️ Common Mistakes to Avoid

1. **Invalid Enum Values**
   ```yaml
   # ❌ Wrong
   threat_type: "email_phishing"
   
   # ✅ Correct  
   threat_type: "phishing"
   ```

2. **Department Too Long**
   ```yaml
   # ❌ Wrong (too long)
   department: "information_technology_and_cybersecurity"
   
   # ✅ Correct
   department: "technology"
   ```

3. **Missing Required Fields**
   ```yaml
   # ❌ Missing seniority and technical_level
   target_profile:
     role: "Manager"
     department: "sales"
   
   # ✅ Complete
   target_profile:
     role: "Manager"
     department: "sales"
     seniority: "mid"
     technical_level: "moderate"
   ```

4. **Wrong Data Types**
   ```yaml
   # ❌ Wrong (should be list)
   psychological_triggers: "urgency, authority"
   
   # ✅ Correct
   psychological_triggers:
     - "urgency"
     - "authority"
   ```

---

## 🔍 Testing Your Template

### 1. Validation Test
```bash
threatgpt simulate --dry-run -s templates/your_template.yaml
```
**Expected Output:** ✅ Scenario loaded and validated successfully

### 2. Full Simulation Test
```bash
threatgpt simulate -s templates/your_template.yaml
```
**Expected Output:** Completed simulation with generated content

### 3. Check Generated Content
Look in `generated_content/` folder for:
- Email templates
- Phone scripts  
- Scenario samples
- Training materials

---

## 📖 Additional Resources

- **TEMPLATE_MANUAL.md** - Complete 950+ line documentation
- **templates/README.md** - Template directory overview
- **TEMPLATE_VALIDATION_GUIDE.md** - Validation troubleshooting
- **existing templates/** - 12+ example templates to learn from

---

## 🆘 Need Help?

1. **Validation Errors**: Check the validation guide
2. **Schema Questions**: See TEMPLATE_MANUAL.md
3. **Examples**: Browse existing templates in `/templates/`
4. **Testing**: Use `--dry-run` flag first

---

**Happy Template Creating! 🎯**