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
            
            # Create detailed prompt for stage content generation
            prompt = f"""
Generate detailed educational content for a cybersecurity training simulation.

Scenario Details:
- Name: {scenario.name}
- Threat Type: {scenario.threat_type.value if hasattr(scenario.threat_type, 'value') else scenario.threat_type}
- Description: {scenario.description}

Current Stage:
- Stage Type: {stage_type}
- Description: {description}

Requirements:
1. Create realistic but educational content
2. Focus on detection and prevention techniques
3. Include specific indicators of compromise (IoCs)
4. Provide defensive recommendations
5. Use placeholder data for sensitive information
6. Keep content appropriate for security training

Generate comprehensive content for this simulation stage:
"""
            
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