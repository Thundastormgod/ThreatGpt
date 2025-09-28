# 📝 ThreatGPT Template Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Copy sample template
cp templates/sample_phishing_template.yaml templates/my_template.yaml

# Validate template
threatgpt simulate --dry-run -s templates/my_template.yaml

# Run simulation
threatgpt simulate -s templates/my_template.yaml
```

## ✅ Required Fields Checklist

```yaml
metadata:
  name: "Your Template Name"        # ✅ Required
  description: "What it does"       # ✅ Required  
  version: "1.0.0"                 # ✅ Required
  author: "Your Name"               # ✅ Required

threat_type: "phishing"             # ✅ Required (see valid values below)
delivery_vector: "email"            # ✅ Required
difficulty_level: 5                 # ✅ Required (1-10)
estimated_duration: 30              # ✅ Required (minutes)

target_profile:
  role: "Employee"                  # ✅ Required
  department: "general"             # ✅ Required (max 50 chars)
  seniority: "mid"                  # ✅ Required (junior/mid/senior)
  technical_level: "moderate"       # ✅ Required (low/moderate/high)
  security_awareness_level: 5       # ✅ Required (1-10)
  industry: "technology"            # ✅ Required

behavioral_pattern:
  psychological_triggers:           # ✅ Required (list)
    - "urgency"
    - "authority"
  social_engineering_tactics:       # ✅ Required (list)
    - "impersonation"
    - "pretexting"
```

## 📚 Valid Enum Values

### `threat_type`
- `phishing` | `spear_phishing` | `malware` | `ransomware`
- `social_engineering` | `insider_threat` | `advanced_persistent_threat`
- `credential_harvesting` | `watering_hole` | `supply_chain`
- `physical_security` | `voice_phishing` | `sms_phishing`

### `delivery_vector`
- `email` | `sms` | `phone` | `web` | `usb` | `wifi` | `physical`

### `seniority`
- `junior` | `mid` | `senior`

### `technical_level`
- `low` | `moderate` | `high`

## 🎯 Template Types Examples

### 📧 Email Phishing
```yaml
threat_type: "phishing"
delivery_vector: "email"
```

### 📱 SMS Phishing  
```yaml
threat_type: "sms_phishing"
delivery_vector: "sms"
```

### 📞 Phone Social Engineering
```yaml
threat_type: "social_engineering"
delivery_vector: "phone"
```

### 💼 Business Email Compromise
```yaml
threat_type: "spear_phishing"
delivery_vector: "email"
target_profile:
  role: "Finance Manager"
  department: "finance"
  seniority: "senior"
```

## ⚠️ Common Errors

| Error | Fix |
|-------|-----|
| `threat_type: "email_phishing"` | Use `"phishing"` |
| `department: "information_technology"` | Max 50 chars: `"technology"` |
| `psychological_triggers: "urgency"` | Use list: `["urgency"]` |
| Missing `seniority` field | Add: `seniority: "mid"` |

## 🔍 Testing Steps

1. **Validate**: `threatgpt simulate --dry-run -s templates/your_template.yaml`
2. **Test Run**: `threatgpt simulate -s templates/your_template.yaml`  
3. **Check Output**: Look in `generated_content/` folder

## 📖 Full Documentation

- **TEMPLATE_CREATION_GUIDE.md** - Complete creation guide
- **TEMPLATE_MANUAL.md** - 950+ line comprehensive manual
- **templates/sample_phishing_template.yaml** - Copy-ready template
- **templates/README.md** - Template directory overview