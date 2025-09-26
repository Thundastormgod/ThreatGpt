# Dataset Integration Plan for ThreatGPT

## Overview

ThreatGPT can leverage publicly available and synthetic datasets to enhance the realism and effectiveness of generated threat scenarios. This document outlines how to integrate key cybersecurity datasets into the platform.

## Supported Datasets

### 📧 Email & Phishing Datasets

#### 1. Enron Email Corpus
- **Source**: [Carnegie Mellon University](https://www.cs.cmu.edu/~./enron/)
- **Size**: ~500,000 emails from 150 users
- **Use Cases**: 
  - Legitimate email patterns and language
  - Corporate communication styles
  - Email headers and metadata patterns
- **Integration**: Email style templates, language patterns for spear-phishing

#### 2. PhishTank Database
- **Source**: [PhishTank.org](https://www.phishtank.com/)
- **Content**: Verified phishing URLs and campaigns
- **Use Cases**:
  - URL patterns and structures
  - Domain spoofing techniques
  - Campaign timing and targeting
- **Integration**: URL generation, domain spoofing templates

#### 3. Nazario Phishing Archive
- **Source**: [Monkey.org](https://monkey.org/~jose/phishing/)
- **Content**: Historical phishing emails and websites
- **Use Cases**:
  - Phishing email templates
  - Social engineering techniques
  - Brand impersonation patterns
- **Integration**: Email content generation, brand mimicry

### 🔒 Insider Threat Datasets

#### 4. CERT Insider Threat Dataset
- **Source**: [CMU CERT Division](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=508099)
- **Content**: Synthetic insider threat scenarios
- **Use Cases**:
  - Behavioral patterns of malicious insiders
  - Data exfiltration methods
  - Privilege escalation scenarios
- **Integration**: Insider threat scenario generation

#### 5. Los Alamos National Laboratory (LANL) Dataset
- **Source**: [LANL Cyber Security](https://csr.lanl.gov/data/)
- **Content**: Network authentication logs
- **Use Cases**:
  - Authentication patterns
  - Lateral movement detection
  - Network behavior analysis
- **Integration**: Network-based threat scenarios

### 🎯 Attack Pattern Datasets

#### 6. MITRE ATT&CK Framework
- **Source**: [MITRE ATT&CK](https://attack.mitre.org/)
- **Content**: Tactics, techniques, and procedures (TTPs)
- **Use Cases**:
  - Attack chain generation
  - Technique mapping
  - Realistic attack progression
- **Integration**: Scenario validation and enhancement

## Implementation Architecture

### 1. Dataset Management Module

```python
# src/threatgpt/datasets/
├── __init__.py
├── manager.py          # Dataset manager and loader
├── processors/         # Dataset-specific processors
│   ├── enron.py        # Enron corpus processor
│   ├── phishtank.py    # PhishTank data processor
│   ├── cert_insider.py # CERT insider threat processor
│   └── lanl_auth.py    # LANL authentication logs
├── models.py           # Dataset models and schemas
├── storage.py          # Dataset storage and caching
└── utils.py            # Dataset utilities
```

### 2. Dataset Configuration

```yaml
# config.yaml - Dataset Configuration
datasets:
  enabled: true
  storage_path: "data/datasets"
  update_interval: "weekly"
  
  # Email Datasets
  enron:
    enabled: true
    path: "data/datasets/enron"
    url: "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
    features:
      - email_style
      - corporate_language
      - sender_patterns
  
  phishtank:
    enabled: true
    api_key: ""  # Set via PHISHTANK_API_KEY
    update_frequency: "daily"
    features:
      - url_patterns
      - domain_spoofing
      - campaign_tracking
  
  # Insider Threat Datasets
  cert_insider:
    enabled: true
    path: "data/datasets/cert_insider"
    scenarios:
      - privilege_escalation
      - data_exfiltration
      - malicious_access
  
  # Attack Pattern Datasets
  mitre_attack:
    enabled: true
    api_url: "https://attack.mitre.org/docs/stix/enterprise-attack.json"
    update_frequency: "monthly"
```

### 3. Dataset Processing Pipeline

```python
# Example: Enron Email Processor
class EnronProcessor:
    """Process Enron email corpus for ThreatGPT."""
    
    def extract_email_patterns(self) -> Dict[str, Any]:
        """Extract email communication patterns."""
        return {
            'subject_patterns': self._analyze_subjects(),
            'greeting_styles': self._extract_greetings(),
            'signature_formats': self._analyze_signatures(),
            'corporate_language': self._extract_language_patterns()
        }
    
    def generate_template(self, role: str, company: str) -> EmailTemplate:
        """Generate email template based on role and company."""
        patterns = self.get_patterns_for_role(role)
        return EmailTemplate(
            subject_style=patterns['subject_style'],
            greeting=patterns['greeting'],
            language_tone=patterns['tone'],
            signature=patterns['signature']
        )
```

## Integration Points

### 1. Enhanced Prompt Engineering

```python
# src/threatgpt/llm/prompts.py
class DatasetEnhancedPrompts:
    """Prompts enhanced with dataset insights."""
    
    def generate_phishing_email(self, target_profile: dict, dataset_insights: dict) -> str:
        """Generate phishing email using dataset insights."""
        enron_style = dataset_insights['enron']['corporate_style']
        phishtank_patterns = dataset_insights['phishtank']['url_patterns']
        
        prompt = f"""
        Generate a spear-phishing email targeting {target_profile['role']} at {target_profile['company']}.
        
        Use these authentic corporate email patterns:
        - Subject style: {enron_style['subject_patterns']}
        - Language tone: {enron_style['language_tone']}
        - Greeting format: {enron_style['greeting_style']}
        
        Include realistic malicious URL using patterns from PhishTank:
        - Domain spoofing: {phishtank_patterns['spoofing_techniques']}
        - URL structure: {phishtank_patterns['common_structures']}
        
        Ensure the email appears legitimate while containing subtle threat indicators.
        """
        return prompt
```

### 2. Scenario Enhancement

```python
# src/threatgpt/core/scenario_enhancer.py
class DatasetScenarioEnhancer:
    """Enhance scenarios with dataset-derived insights."""
    
    def enhance_insider_threat(self, scenario: ThreatScenario) -> ThreatScenario:
        """Enhance insider threat scenario with CERT dataset insights."""
        cert_patterns = self.dataset_manager.get_insider_patterns()
        
        # Add realistic behavioral indicators
        scenario.behavioral_indicators = cert_patterns['behavioral_indicators']
        scenario.attack_progression = cert_patterns['attack_chains']
        scenario.data_targets = cert_patterns['common_targets']
        
        return scenario
```

### 3. Template System Integration

```yaml
# templates/enhanced_phishing.yaml
metadata:
  name: "Dataset-Enhanced Executive Phishing"
  version: "2.0"
  datasets_used:
    - enron
    - phishtank
    - mitre_attack

threat_type: "spear_phishing"
target_profile:
  role: "executive"
  department: "finance"

dataset_enhancements:
  email_style:
    source: "enron"
    patterns:
      - corporate_communication
      - executive_language
  
  url_generation:
    source: "phishtank"
    techniques:
      - domain_spoofing
      - subdomain_hijacking
  
  attack_chain:
    source: "mitre_attack"
    techniques:
      - "T1566.001"  # Spearphishing Attachment
      - "T1204.002"  # User Execution: Malicious File
```

## Implementation Steps

### Phase 1: Dataset Infrastructure (Week 1-2)
1. **Dataset Manager**: Core dataset management system
2. **Storage Layer**: Efficient dataset storage and caching
3. **Update Mechanisms**: Automated dataset updates
4. **Configuration System**: Dataset configuration management

### Phase 2: Dataset Processors (Week 3-4)
1. **Enron Processor**: Email pattern extraction
2. **PhishTank Processor**: URL and campaign analysis
3. **CERT Processor**: Insider threat pattern extraction
4. **MITRE ATT&CK Processor**: Attack technique mapping

### Phase 3: Integration (Week 5-6)
1. **Prompt Enhancement**: Dataset-informed prompt generation
2. **Scenario Enhancement**: Realistic scenario augmentation
3. **Template System**: Dataset-enhanced templates
4. **Quality Validation**: Dataset-based validation metrics

### Phase 4: Advanced Features (Week 7-8)
1. **Dynamic Learning**: Continuous dataset learning
2. **Pattern Recognition**: Advanced pattern extraction
3. **Temporal Analysis**: Time-based pattern analysis
4. **Cross-Dataset Correlation**: Multi-dataset insights

## CLI Commands for Dataset Management

```bash
# Dataset management commands
python -m src.threatgpt.cli.main datasets list
python -m src.threatgpt.cli.main datasets download --dataset enron
python -m src.threatgpt.cli.main datasets update --all
python -m src.threatgpt.cli.main datasets status

# Enhanced scenario generation
python -m src.threatgpt.cli.main simulate \
  --scenario templates/phishing.yaml \
  --enhance-with-datasets \
  --datasets enron,phishtank

# Dataset-based template creation
python -m src.threatgpt.cli.main templates create \
  --type phishing \
  --enhance-with enron \
  --target-role executive
```

## Data Privacy and Ethics

### Privacy Safeguards
- **Data Anonymization**: Remove all PII from datasets
- **Consent Compliance**: Ensure proper data usage permissions
- **Secure Storage**: Encrypted dataset storage
- **Access Controls**: Role-based dataset access

### Ethical Guidelines
- **Legitimate Use Only**: Educational and authorized testing only
- **No Malicious Content**: Filter out actual malware/exploits
- **Compliance**: GDPR, CCPA, and other privacy law compliance
- **Audit Trails**: Comprehensive logging of dataset usage

## Performance Optimization

### Caching Strategy
```python
# Intelligent dataset caching
@cache_with_ttl(hours=24)
def get_email_patterns(role: str, industry: str) -> Dict[str, Any]:
    """Cached email pattern retrieval."""
    pass

@cache_with_ttl(hours=1)
def get_fresh_phishing_urls(count: int = 100) -> List[str]:
    """Fresh phishing URL patterns."""
    pass
```

### Preprocessing Pipeline
- **Batch Processing**: Efficient dataset preprocessing
- **Incremental Updates**: Only process new data
- **Pattern Extraction**: Pre-computed pattern libraries
- **Index Optimization**: Fast pattern lookup

## Monitoring and Metrics

### Dataset Health
- **Freshness**: Dataset age and update status
- **Quality**: Data quality metrics
- **Coverage**: Pattern coverage analysis
- **Usage**: Dataset utilization statistics

### Integration Effectiveness
- **Realism Score**: Dataset-enhanced scenario realism
- **Detection Rate**: How well enhanced scenarios are detected
- **User Feedback**: Scenario quality ratings
- **Performance Impact**: Dataset integration performance cost

## Future Enhancements

### Advanced Dataset Integration
- **Custom Dataset Support**: User-provided datasets
- **Real-time Feeds**: Live threat intelligence feeds
- **ML-Enhanced Patterns**: Machine learning pattern extraction
- **Cross-Dataset Analysis**: Multi-dataset correlation analysis

### Synthetic Data Generation
- **GANs for Email Generation**: AI-generated realistic emails
- **Synthetic User Behavior**: Realistic user activity patterns
- **Network Traffic Synthesis**: Realistic network patterns
- **Temporal Pattern Simulation**: Time-based behavior patterns

This comprehensive dataset integration approach will significantly enhance ThreatGPT's realism and effectiveness while maintaining ethical standards and privacy compliance.