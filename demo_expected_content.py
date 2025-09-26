#!/usr/bin/env python3
"""Create a mock simulation to demonstrate ThreatGPT content format and logging"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

# Add src to path so we can import ThreatGPT modules
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from threatgpt.core.output_models import SimulationOutput, ScenarioMetadata, TargetProfile, SimulationMetrics, QualityAssessment, ContentGeneration, ProviderInfo
from threatgpt.core.simulation_logger import SimulationLogger

def create_mock_simulation_content():
    """Create exactly the type of content ThreatGPT expects from AI models"""
    
    print("🎯 ThreatGPT AI Content Expectations:")
    print("=" * 60)
    
    # Stage 1: Reconnaissance content
    reconnaissance_content = """
# Executive Spear-Phishing Reconnaissance Analysis

## Educational Overview
This reconnaissance phase demonstrates common information gathering techniques that attackers use against C-level executives, focusing on defensive awareness and detection.

## Information Gathering Techniques (EDUCATIONAL)

### 1. Open Source Intelligence (OSINT)
**What attackers typically research:**
- Executive LinkedIn profiles and professional history
- Company press releases and financial reports
- Social media presence and personal interests
- Board meeting schedules and company events

**Defensive Indicators to Monitor:**
- Unusual profile viewing patterns on corporate social media
- Increased reconnaissance activity around earnings calls
- Suspicious searches for executive contact information

### 2. Corporate Intelligence Gathering
**Target Information:**
- Organizational structure and reporting relationships
- Recent company mergers, acquisitions, or partnerships
- Current business challenges and strategic initiatives
- Key vendor relationships and technology partners

**Detection Methods:**
- Monitor for unusual queries to public company databases
- Watch for suspicious LinkedIn connection requests to executives
- Track unusual website visitor patterns on investor relations pages

### 3. Technical Reconnaissance
**Infrastructure Assessment:**
- Email server configurations and security headers
- Domain registration and DNS information
- Technology stack analysis from job postings
- Security vendor relationships from public contracts

## Indicators of Compromise (IoCs)

**Behavioral Indicators:**
- Unusual email reconnaissance (header analysis, delivery testing)
- Suspicious social media engagement with executives
- Abnormal website traffic patterns from security scanning tools
- Increased phishing attempts against assistant/support staff

**Technical Indicators:**
- Reconnaissance tools in web server logs
- Unusual DNS queries for company domains
- Email header probing attempts
- Social engineering calls to IT help desk

## Defensive Recommendations

1. **Executive Protection Program:**
   - Limit public exposure of executive schedules and travel
   - Implement executive-specific email security controls
   - Provide advanced security awareness training for C-level staff

2. **Monitoring and Detection:**
   - Deploy threat intelligence feeds focused on executive targeting
   - Monitor social media for reconnaissance activities
   - Implement behavioral analysis for executive email accounts

3. **Information Disclosure Controls:**
   - Review and limit publicly available organizational information
   - Implement privacy controls on executive social media profiles
   - Control access to company organizational charts and directories

**Training Focus:** This scenario emphasizes recognizing pre-attack reconnaissance activities and implementing appropriate executive protection measures.
"""

    # Stage 2: Attack Planning content
    attack_planning_content = """
# Executive Spear-Phishing Attack Planning Analysis

## Educational Overview
This phase demonstrates how attackers plan sophisticated spear-phishing campaigns against executives, focusing on defensive preparation and prevention strategies.

## Attack Vector Planning (EDUCATIONAL)

### 1. Email Campaign Strategy
**Typical Attack Approaches:**
- Board meeting document sharing pretext
- Urgent financial report requests
- Regulatory compliance documentation
- Strategic partnership proposals

**Defensive Counter-Measures:**
- Implement executive email filtering with board meeting keywords
- Establish verification protocols for urgent financial requests
- Create secure channels for sensitive document sharing
- Train executives on verification procedures

### 2. Social Engineering Tactics
**Common Pretexts:**
- Impersonation of board members or legal counsel
- Time-sensitive compliance or audit requests
- Confidential merger and acquisition communications
- Executive assistant requests for schedule changes

**Detection Strategies:**
- Verify sender identity through secondary channels
- Flag emails with urgent financial or legal language
- Implement callback verification for sensitive requests
- Monitor for impersonation attempts

### 3. Technical Delivery Methods
**Delivery Mechanisms:**
- Malicious PDF attachments disguised as board reports
- Credential harvesting through fake document portals
- Calendar meeting requests with malicious links
- Voicemail notifications with malicious payloads

## Risk Assessment Matrix

**High-Risk Indicators:**
- External emails requesting confidential information
- Urgent requests bypassing normal approval processes
- Links to external document sharing platforms
- Requests for credential verification

**Medium-Risk Indicators:**
- Unusual email timing (after hours, weekends)
- Generic greetings despite claiming personal relationship
- Minor spelling errors in sender domains
- Pressure tactics emphasizing urgency or confidentiality

## Defensive Implementation

1. **Email Security Controls:**
   - Advanced threat protection for executive accounts
   - Domain spoofing protection and DMARC implementation
   - Attachment sandboxing for document analysis
   - Link protection with real-time reputation checking

2. **Process Controls:**
   - Multi-factor authentication for all sensitive operations
   - Out-of-band verification for financial requests
   - Secure document sharing platforms with access logging
   - Regular security awareness updates for executives

3. **Incident Response Preparation:**
   - Executive-focused incident response procedures
   - Rapid containment protocols for compromised accounts
   - Communications plan for potential breaches
   - Forensic procedures for executive device analysis

**Training Emphasis:** Focus on process verification, threat recognition, and incident reporting procedures.
"""

    # Stage 3: Execution content
    execution_content = """
# Executive Spear-Phishing Execution Analysis

## Educational Overview
This phase demonstrates the final execution of spear-phishing attacks against executives, emphasizing incident detection, response, and recovery procedures.

## Attack Execution Methods (EDUCATIONAL)

### 1. Email Delivery and Engagement
**Typical Execution Timeline:**
- Initial reconnaissance: 2-4 weeks
- Email crafting and testing: 1-2 weeks
- Delivery timing: Business hours during busy periods
- Follow-up attempts: 24-48 hours after initial delivery

**Detection Opportunities:**
- Email security gateway alerts for suspicious patterns
- User reporting of suspicious communications
- Behavioral analysis detecting unusual email interactions
- Endpoint detection of malicious file execution

### 2. Credential Harvesting Techniques
**Common Methods:**
- Fake document portals requiring login credentials
- Spoofed company login pages for "urgent access"
- Multi-factor authentication bypass attempts
- Session hijacking through malicious links

**Prevention and Detection:**
- Single sign-on (SSO) implementation with conditional access
- Multi-factor authentication for all executive accounts
- Behavioral analysis for unusual login patterns
- Real-time alerting for credential compromise indicators

### 3. Post-Compromise Activities
**Typical Attacker Actions:**
- Email account reconnaissance and contact harvesting
- Internal phishing campaigns using compromised accounts
- Data exfiltration of sensitive communications
- Lateral movement to additional executive accounts

## Incident Response Procedures

### Immediate Response (0-1 hour):
1. **Account Containment:**
   - Disable compromised executive account
   - Reset all associated passwords and MFA tokens
   - Block suspicious IP addresses at firewall level
   - Isolate potentially affected systems

2. **Communication Protocol:**
   - Notify executive team and board members
   - Inform legal and compliance teams
   - Coordinate with external security partners
   - Prepare stakeholder communications

### Investigation Phase (1-24 hours):
1. **Forensic Analysis:**
   - Email flow analysis and timeline reconstruction
   - System access log review and anomaly detection
   - Network traffic analysis for data exfiltration
   - Endpoint forensics on executive devices

2. **Impact Assessment:**
   - Identify accessed sensitive information
   - Determine scope of potential data exposure
   - Assess regulatory reporting requirements
   - Evaluate business continuity impacts

### Recovery and Lessons Learned:
1. **System Restoration:**
   - Secure account recovery procedures
   - Enhanced monitoring implementation
   - Updated security controls deployment
   - Refreshed security awareness training

2. **Process Improvements:**
   - Executive protection program updates
   - Enhanced email security implementations
   - Improved incident response procedures
   - Regular tabletop exercises and drills

## Forensic Artifacts and Evidence

**Email Evidence:**
- Message headers and routing information
- Attachment analysis and malware signatures
- Link analysis and destination verification
- Timing analysis and sender verification

**System Evidence:**
- Login logs and access patterns
- File access and modification timestamps
- Network connections and data transfers
- Process execution and behavioral analysis

**Training Outcomes:** 
- Improved executive security awareness
- Enhanced incident response capabilities
- Strengthened technical security controls
- Better threat intelligence integration

**Next Steps:**
- Regular security assessments and penetration testing
- Continuous monitoring and threat hunting
- Executive security awareness program updates
- Industry threat intelligence sharing
"""

    return {
        "reconnaissance": reconnaissance_content,
        "attack_planning": attack_planning_content, 
        "execution": execution_content
    }

def create_mock_simulation():
    """Create a complete mock simulation showing expected ThreatGPT output"""
    
    print("\n🚀 Creating Mock Simulation...")
    
    # Get the generated content
    content = create_mock_simulation_content()
    
    # Create the simulation output using our validated models
    simulation_output = SimulationOutput(
        simulation_id=str(uuid.uuid4()),
        version="1.0",
        created_at=datetime.now(),
        started_at=datetime.now(),
        completed_at=datetime.now(),
        status="completed",
        success=True,
        error_message=None,
        scenario=ScenarioMetadata(
            name="Executive Spear-Phishing Campaign",
            description="Advanced spear-phishing attack targeting C-level executives with board meeting pretext and document sharing lure",
            threat_type="spear_phishing",
            delivery_vector="email",
            difficulty_level=8,
            mitre_techniques=["T1566.001", "T1566.002", "T1598.003"],
            scenario_file="templates/executive_phishing.yaml"
        ),
        target_profile=TargetProfile(
            role="Chief Executive Officer",
            department="executive", 
            seniority="c_level",
            industry="financial_services",
            security_awareness=6,
            additional_attributes={}
        ),
        generated_content=[
            ContentGeneration(
                content_type="email",
                content=content["reconnaissance"],
                prompt_used="reconnaissance generation for spear_phishing",
                provider_info=ProviderInfo(
                    name="openrouter",
                    model="x-ai/grok-4-fast:free",
                    api_version="v1",
                    response_time_ms=1234,
                    token_usage={"prompt_tokens": 456, "completion_tokens": 789, "total_tokens": 1245}
                ),
                safety_validated=True,
                educational_markers=["Educational simulation content", "Defensive focus emphasized"],
                generated_at=datetime.now()
            ),
            ContentGeneration(
                content_type="email",
                content=content["attack_planning"],
                prompt_used="attack_planning generation for spear_phishing", 
                provider_info=ProviderInfo(
                    name="openrouter",
                    model="x-ai/grok-4-fast:free",
                    api_version="v1",
                    response_time_ms=1567,
                    token_usage={"prompt_tokens": 445, "completion_tokens": 823, "total_tokens": 1268}
                ),
                safety_validated=True,
                educational_markers=["Educational simulation content", "Process verification focus"],
                generated_at=datetime.now()
            ),
            ContentGeneration(
                content_type="email",
                content=content["execution"],
                prompt_used="execution generation for spear_phishing",
                provider_info=ProviderInfo(
                    name="openrouter", 
                    model="x-ai/grok-4-fast:free",
                    api_version="v1",
                    response_time_ms=1789,
                    token_usage={"prompt_tokens": 467, "completion_tokens": 856, "total_tokens": 1323}
                ),
                safety_validated=True,
                educational_markers=["Educational simulation content", "Incident response focus"],
                generated_at=datetime.now()
            )
        ],
        metrics=SimulationMetrics(
            success_rate=100.0,
            stages_completed=3,
            total_stages=3,
            duration_seconds=5.59,
            errors_encountered=0,
            warnings_issued=0
        ),
        quality_assessment=QualityAssessment(
            realism_score=9,
            educational_value=10,
            safety_compliance=True,
            content_appropriateness=True,
            detection_indicators=["Educational simulation markers included", "Defensive recommendations provided", "IoCs clearly identified"]
        ),
        logs=[],
        recommendations=[
            "Implement executive-specific email security controls",
            "Enhance security awareness training for C-level staff",  
            "Deploy behavioral analysis for executive accounts",
            "Establish verification protocols for urgent requests"
        ],
        artifacts={},
        environment={
            "llm_provider": "openrouter",
            "python_version": "3.11.9",
            "threatgpt_version": "0.1.0"
        }
    )
    
    # Save using our logging system
    logger = SimulationLogger()
    saved_path = logger.save_simulation_result(simulation_output)
    
    print(f"✅ Mock simulation saved to: {saved_path}")
    
    return simulation_output

if __name__ == "__main__":
    print("🎯 ThreatGPT Content Demonstration")
    print("=" * 50)
    
    # Show what content AI should generate
    content = create_mock_simulation_content()
    
    print(f"📝 Reconnaissance Stage Content ({len(content['reconnaissance'])} chars):")
    print(content['reconnaissance'][:300] + "...\n")
    
    print(f"📝 Attack Planning Stage Content ({len(content['attack_planning'])} chars):")
    print(content['attack_planning'][:300] + "...\n")
    
    print(f"📝 Execution Stage Content ({len(content['execution'])} chars):")
    print(content['execution'][:300] + "...\n")
    
    # Create and save complete simulation
    simulation = create_mock_simulation()
    
    print(f"\n🎉 Complete simulation created with {len(simulation.generated_content)} content pieces")
    print(f"Total duration: {simulation.metrics.duration_seconds}s")
    print(f"Success rate: {simulation.metrics.success_rate}%")
    print(f"Educational value: {simulation.quality_assessment.educational_value}/10")
    
    print(f"\n💾 Simulation saved and ready for logs commands!")