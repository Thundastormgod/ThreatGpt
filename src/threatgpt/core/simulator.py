"""Core threat simulation engine for ThreatGPT.

This module provides the main simulation engine that orchestrates threat scenario
execution using LLM providers and validation systems.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Any, List, Dict
from uuid import uuid4

from threatgpt.core.models import (
    ThreatScenario, 
    SimulationResult, 
    SimulationStage,
    SimulationStatus
)

logger = logging.getLogger(__name__)


class ThreatSimulator:
    """Core threat simulation engine."""
    
    def __init__(self, llm_provider: Optional[Any] = None, max_stages: int = 10) -> None:
        """Initialize the threat simulator.
        
        Args:
            llm_provider: LLM provider instance for content generation
            max_stages: Maximum number of simulation stages to execute
        """
        from threatgpt.llm.manager import LLMManager
        
        self.llm_provider = llm_provider or LLMManager()
        self.max_stages = max_stages
        self._active_simulations: Dict[str, SimulationResult] = {}
    
    async def execute_simulation(self, scenario: ThreatScenario) -> SimulationResult:
        """Execute a threat simulation scenario.
        
        Args:
            scenario: The threat scenario to execute
            
        Returns:
            SimulationResult containing the execution results
            
        Raises:
            ValueError: If scenario is invalid or missing required data
            RuntimeError: If simulation execution fails
        """
        if not scenario.name:
            raise ValueError("Scenario must have a valid name")
            
        logger.info(f"Starting simulation for scenario: {scenario.name}")
        
        # Create simulation result
        result = SimulationResult(
            status=SimulationStatus.RUNNING,
            scenario_id=scenario.scenario_id,
            start_time=datetime.utcnow()
        )
        
        # Track active simulation
        self._active_simulations[result.result_id] = result
        
        try:
            # Execute simulation stages
            await self._execute_stages(scenario, result)
            
            # Mark as completed
            result.mark_completed(success=True)
            logger.info(f"Simulation completed successfully: {scenario.name}")
            
        except Exception as e:
            logger.error(f"Simulation failed for scenario {scenario.name}: {str(e)}")
            result.mark_completed(success=False, error_message=str(e))
            
        finally:
            # Remove from active simulations
            self._active_simulations.pop(result.result_id, None)
            
        return result
    
    async def _execute_stages(self, scenario: ThreatScenario, result: SimulationResult) -> None:
        """Execute the individual stages of a simulation.
        
        Args:
            scenario: The threat scenario being executed
            result: The simulation result to update
        """
        # Define basic simulation stages
        stages_config = [
            {"type": "reconnaissance", "description": "Initial target reconnaissance"},
            {"type": "attack_planning", "description": "Plan attack methodology"},
            {"type": "execution", "description": "Execute the threat scenario"},
            {"type": "persistence", "description": "Establish persistence mechanisms"},
            {"type": "data_collection", "description": "Collect target information"},
            {"type": "exfiltration", "description": "Data exfiltration simulation"},
            {"type": "cleanup", "description": "Clean up simulation artifacts"}
        ]
        
        for i, stage_config in enumerate(stages_config[:self.max_stages]):
            stage_start = datetime.utcnow()
            
            try:
                # Generate stage content using LLM
                stage_content = await self._generate_stage_content(
                    scenario, 
                    stage_config["type"], 
                    stage_config["description"]
                )
                
                # Create simulation stage
                stage = SimulationStage(
                    stage_type=stage_config["type"],
                    content=stage_content,
                    timestamp=stage_start,
                    success=True,
                    metadata={
                        "stage_number": i + 1,
                        "total_stages": len(stages_config),
                        "scenario_name": scenario.name
                    }
                )
                
                # Calculate duration
                stage_end = datetime.utcnow()
                stage.duration_seconds = (stage_end - stage_start).total_seconds()
                
                # Add stage to result
                result.add_stage(stage)
                
                logger.debug(f"Completed stage {i+1}: {stage_config['type']}")
                
                # Small delay between stages for realism
                await asyncio.sleep(0.1)
                
            except Exception as e:
                # Create failed stage
                stage = SimulationStage(
                    stage_type=stage_config["type"],
                    content="Stage execution failed",
                    timestamp=stage_start,
                    success=False,
                    error_message=str(e),
                    metadata={"stage_number": i + 1, "error": str(e)}
                )
                
                result.add_stage(stage)
                logger.warning(f"Stage {i+1} failed: {str(e)}")
                
                # Continue with next stage unless critical failure
                if "critical" in str(e).lower():
                    break
    
    async def _generate_stage_content(self, scenario: ThreatScenario, stage_type: str, description: str) -> str:
        """Generate content for a simulation stage using LLM.
        
        Args:
            scenario: The threat scenario
            stage_type: Type of stage being executed
            description: Description of the stage
            
        Returns:
            Generated content for the stage
        """
        try:
            # Check if LLM provider is available
            if not self.llm_provider or not self.llm_provider.is_available():
                logger.warning("No LLM provider available, using fallback content")
                return self._generate_fallback_content(scenario, stage_type, description)
            
            # Create detailed prompt for actual scenario sample generation
            prompt = self._create_scenario_generation_prompt(scenario, stage_type, description)
            
            # Generate content using LLM manager
            response = await self.llm_provider.generate_content(
                prompt=prompt,
                scenario_type=f"threat_simulation_{stage_type}",
                max_tokens=800,
                temperature=0.7
            )
            
            if response and response.content:
                logger.debug(f"Generated {len(response.content)} characters for stage {stage_type}")
                return response.content
            else:
                logger.warning(f"Empty response from LLM for stage {stage_type}")
                return self._generate_fallback_content(scenario, stage_type, description)
                
        except Exception as e:
            logger.error(f"LLM content generation failed for stage {stage_type}: {str(e)}")
            return self._generate_fallback_content(scenario, stage_type, description)
    
    def _create_scenario_generation_prompt(self, scenario: ThreatScenario, stage_type: str, description: str) -> str:
        """Create stage-specific prompts for generating actual threat scenario samples."""
        threat_type = scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else str(scenario.threat_type)
        
        # Base context for all prompts
        base_context = f"""
Scenario: {scenario.name}
Threat Type: {threat_type}
Description: {scenario.description}
Stage: {stage_type} - {description}
"""
        
        # Generate different content based on stage type and threat type
        if stage_type == "reconnaissance":
            return self._create_reconnaissance_prompt(scenario, base_context)
        elif stage_type == "attack_planning":
            return self._create_attack_planning_prompt(scenario, base_context)
        elif threat_type in ["phishing", "spear_phishing", "sms_phishing"]:
            return self._create_phishing_sample_prompt(scenario, base_context, stage_type)
        elif threat_type in ["social_engineering", "vishing"]:
            return self._create_social_engineering_prompt(scenario, base_context, stage_type)
        elif threat_type in ["bec", "business_email_compromise"]:
            return self._create_bec_sample_prompt(scenario, base_context, stage_type)
        else:
            return self._create_generic_scenario_prompt(scenario, base_context, stage_type)
    
    def _create_phishing_sample_prompt(self, scenario: ThreatScenario, base_context: str, stage_type: str) -> str:
        """Generate actual phishing email samples."""
        threat_type = scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else str(scenario.threat_type)
        
        if "sms" in threat_type.lower():
            return f"""{base_context}

Generate a realistic SMS phishing message sample that demonstrates this threat scenario.

Requirements:
- Create an actual SMS text message that could be sent to the target
- Use realistic urgency and social engineering tactics
- Include believable but fake URLs (use example.com domains)
- Make it specific to the target profile and industry
- Use professional language appropriate for the target
- Include psychological triggers that would make someone click
- Keep message length appropriate for SMS (160-300 characters)

Generate the SMS message content:"""
        else:
            return f"""{base_context}

Generate a realistic phishing email sample that demonstrates this threat scenario.

Requirements:
- Create an actual email that could be sent to the target (Subject line, From, Body)
- Use realistic social engineering tactics and urgency
- Include believable but fake sender addresses and URLs (use example.com domains)
- Make it specific to the target profile, role, and industry context
- Use appropriate professional language and formatting
- Include psychological triggers and call-to-action
- Add realistic email signatures and branding elements

Generate the complete email sample:"""
    
    def _create_social_engineering_prompt(self, scenario: ThreatScenario, base_context: str, stage_type: str) -> str:
        """Generate social engineering script samples."""
        return f"""{base_context}

Generate a realistic social engineering phone script sample for this threat scenario.

Requirements:
- Create an actual phone conversation script that could be used
- Include both caller lines and expected target responses
- Use realistic pretexts and authority/urgency tactics
- Make it specific to the target's role and industry
- Include techniques to build rapport and trust
- Add realistic company/service impersonation details
- Include methods to extract information or gain access
- Show how to handle common objections or questions

Generate the phone script sample:"""
    
    def _create_bec_sample_prompt(self, scenario: ThreatScenario, base_context: str, stage_type: str) -> str:
        """Generate BEC (Business Email Compromise) samples."""
        return f"""{base_context}

Generate a realistic BEC (Business Email Compromise) email sample for this threat scenario.

Requirements:
- Create an actual email that impersonates a high-level executive or trusted vendor
- Use realistic business language and urgent financial requests
- Include believable but fake executive names and company details
- Make it specific to the target's industry and business context
- Use professional formatting and appropriate tone
- Include psychological pressure and time constraints
- Add realistic financial transaction details (use fake account numbers)
- Show techniques to bypass scrutiny and verification

Generate the BEC email sample:"""
    
    def _create_reconnaissance_prompt(self, scenario: ThreatScenario, base_context: str) -> str:
        """Generate reconnaissance activity samples."""
        return f"""{base_context}

Generate realistic reconnaissance activities and information gathering samples for this threat scenario.

Requirements:
- Create actual examples of information that would be gathered about the target
- Show specific OSINT sources and techniques that would be used
- Include realistic but fake target information and company details
- Demonstrate how collected information would be used for the attack
- Show social media, website, and public record research examples
- Include timing and targeting strategies
- Add realistic target profiling and attack preparation steps

Generate the reconnaissance sample:"""
    
    def _create_attack_planning_prompt(self, scenario: ThreatScenario, base_context: str) -> str:
        """Generate attack planning samples."""
        return f"""{base_context}

Generate a realistic attack execution plan sample for this threat scenario.

Requirements:
- Create an actual step-by-step attack plan that could be followed
- Include specific timing, methods, and resources needed
- Show realistic but fake infrastructure setup (domains, servers, etc.)
- Demonstrate attack flow and decision points
- Include contingency plans and backup methods
- Add realistic success metrics and goals
- Show how to maintain persistence and avoid detection
- Include exit strategies and cleanup procedures

Generate the attack plan sample:"""
    
    def _create_generic_scenario_prompt(self, scenario: ThreatScenario, base_context: str, stage_type: str) -> str:
        """Generate generic threat scenario samples."""
        return f"""{base_context}

Generate a realistic threat scenario sample that demonstrates this specific attack type.

Requirements:
- Create actual content that could be used in this type of attack
- Use realistic tactics, techniques, and procedures (TTPs)
- Include believable but fake details appropriate for the threat type
- Make it specific to the target profile and industry context
- Show realistic attack methods and social engineering approaches
- Include appropriate technical details and execution steps
- Add realistic timing and delivery mechanisms

Generate the scenario sample:"""
    
    def _generate_fallback_content(self, scenario: ThreatScenario, stage_type: str, description: str) -> str:
        """Generate fallback content when LLM is unavailable."""
        threat_type = scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else str(scenario.threat_type)
        
        fallback_templates = {
            "reconnaissance": f"""
[RECONNAISSANCE STAGE]
Scenario: {scenario.name}
Threat Type: {threat_type}

In this stage, attackers would typically:
• Gather information about the target organization
• Identify potential entry points and vulnerabilities
• Research key personnel and organizational structure
• Collect technical information about systems and infrastructure

Defensive Measures:
• Monitor for unusual reconnaissance activities
• Implement proper information disclosure policies
• Use threat intelligence to identify scanning attempts
• Educate employees about social engineering attempts

Indicators of Compromise:
• Unusual network scanning activities
• Suspicious social media research
• Unexpected information requests
• Anomalous DNS queries
""",
            "attack_planning": f"""
[ATTACK PLANNING STAGE]
Scenario: {scenario.name}
Threat Type: {threat_type}

Attack planning typically involves:
• Analyzing gathered reconnaissance data
• Selecting appropriate attack vectors
• Developing custom tools or adapting existing ones
• Planning timing and sequence of attack phases

Defensive Strategies:
• Implement defense-in-depth architecture
• Regular vulnerability assessments and patching
• Employee security awareness training
• Incident response plan preparation

Key Prevention Points:
• Network segmentation
• Access controls and privilege management
• Security monitoring and alerting
• Regular security audits
""",
            "execution": f"""
[EXECUTION STAGE]
Scenario: {scenario.name}
Threat Type: {threat_type}

Execution phase characteristics:
• Initial access attempts using planned attack vectors
• Exploitation of identified vulnerabilities
• Deployment of malicious payloads or social engineering
• Attempts to establish foothold in target environment

Detection Opportunities:
• Endpoint detection and response (EDR) systems
• Network traffic analysis
• Behavioral analytics
• User activity monitoring

Immediate Response Actions:
• Isolate affected systems
• Preserve evidence for analysis
• Activate incident response team
• Communicate with stakeholders
"""
        }
        
        # Return specific template or generic content
        return fallback_templates.get(stage_type, f"""
[{stage_type.upper()} STAGE]
Scenario: {scenario.name}
Threat Type: {threat_type}

Stage Description: {description}

This simulation stage would demonstrate key aspects of the {stage_type} phase
in a {threat_type} attack scenario. Educational content and defensive
recommendations would be provided here.

Note: Full content generation requires LLM provider configuration.
""")
    
    def get_active_simulations(self) -> Dict[str, SimulationResult]:
        """Get currently active simulations.
        
        Returns:
            Dictionary of active simulation results by ID
        """
        return self._active_simulations.copy()
    
    def cancel_simulation(self, result_id: str) -> bool:
        """Cancel an active simulation.
        
        Args:
            result_id: ID of the simulation result to cancel
            
        Returns:
            True if simulation was cancelled, False if not found
        """
        if result_id in self._active_simulations:
            result = self._active_simulations[result_id]
            result.status = SimulationStatus.CANCELLED
            result.mark_completed(success=False, error_message="Simulation cancelled by user")
            self._active_simulations.pop(result_id)
            logger.info(f"Simulation cancelled: {result_id}")
            return True
        return False
    
    def __repr__(self) -> str:
        active_count = len(self._active_simulations)
        return f"ThreatSimulator(provider={type(self.llm_provider).__name__}, active={active_count})"