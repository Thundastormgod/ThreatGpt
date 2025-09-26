# ThreatGPT Content Storage System

## 📍 **Content Storage Locations**

### 1. **Raw Simulation Logs** 
- **Location**: `logs/simulations/successful/`
- **Format**: JSON files with complete simulation data
- **Contains**: Full simulation results, metadata, timing, and AI-generated content
- **Example**: `20250926_140256_0288373c-bf6a-41ad-a310-95b43aecd0ec.json`

### 2. **Organized AI Content** 
- **Location**: `generated_content/`
- **Format**: Markdown files organized by category
- **Contains**: Extracted AI-generated content with metadata headers
- **Auto-updated**: ✅ Extraction tool available

## 📂 **Content Organization Structure**

```
generated_content/
├── README.md                    # Overview and statistics
├── content_index.json          # Searchable content index
├── scenarios/                   # Complete threat scenarios
├── phone_scripts/              # Social engineering call scripts
├── email_templates/            # Phishing email examples  
├── training_materials/         # Security awareness content
└── reports/                    # Analysis and summaries
```

## 🎯 **Content Categories**

### 📞 **Phone Scripts** (`phone_scripts/`)
- IT help desk impersonation calls
- Executive impersonation scenarios
- Technical support scam scripts
- Social engineering conversation flows

### 📧 **Email Templates** (`email_templates/`)
- Spear-phishing campaign examples
- Business Email Compromise (BEC) templates
- Credential harvesting emails
- Executive impersonation messages

### 🎯 **Scenarios** (`scenarios/`)
- Multi-stage attack walkthroughs
- Reconnaissance phase documentation
- Attack chain explanations
- Post-exploitation activities

### 📚 **Training Materials** (`training_materials/`)
- Security awareness content
- Warning signs and red flags
- Defensive procedures and countermeasures
- Incident response guides
- Employee training scenarios

### 📊 **Reports** (`reports/`)
- Threat landscape analysis
- Training effectiveness reports
- Security recommendations
- Simulation summaries

## 🔧 **Content Management Tools**

### 1. **Content Extraction Tool** (`extract_content.py`)
```bash
python extract_content.py
```
- Extracts content from all simulation logs
- Organizes into appropriate categories
- Creates searchable index
- Generates summary statistics

### 2. **Auto Content Saver** (`src/threatgpt/utils/auto_content_saver.py`)
- Automatically saves content during simulations
- Real-time organization and categorization
- Markdown formatting with metadata
- Integration with simulation pipeline

## 📊 **Current Content Statistics**

Based on latest extraction:
- **Total Simulations Processed**: 7
- **Content Items Extracted**: 4
- **Training Materials**: 4 high-quality educational documents
- **Content Quality**: Professional cybersecurity training materials

## 🚀 **Content Usage Examples**

### **Training Materials Available**:
1. **IT Help Desk Impersonation** - Reconnaissance phase analysis with IoCs
2. **Executive Spear-Phishing** - Multi-stage campaign documentation 
3. **Social Engineering Scripts** - Phone-based attack scenarios
4. **Defensive Procedures** - Security awareness guidelines

### **Content Features**:
- ✅ Educational disclaimers throughout
- ✅ Realistic but safe examples using placeholder data
- ✅ Detailed metadata for easy categorization
- ✅ Professional Markdown formatting
- ✅ Integration-ready for training platforms
- ✅ Search and index capabilities

## 🎉 **Status: FULLY OPERATIONAL**

✅ **AI Content Generation**: Working with OpenRouter integration  
✅ **Content Storage**: Organized folder structure created  
✅ **Content Extraction**: Automated tool available  
✅ **Content Organization**: Categorized by type and use case  
✅ **Content Access**: Easy browsing with README and index  
✅ **Content Quality**: Professional training-grade materials  

The ThreatGPT system now automatically saves all AI-generated content in an organized, searchable format ready for immediate use in cybersecurity training programs! 🎯