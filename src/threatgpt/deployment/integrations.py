"""Enterprise platform integrations for ThreatGPT deployment services.

This module provides integrations with major enterprise security platforms
for automated threat deployment and metrics collection.
"""

import asyncio
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

import aiohttp
from pydantic import BaseModel, Field

from . import DeploymentChannel, DeploymentResult, CampaignMetrics


class PlatformIntegration(ABC):
    """Base class for enterprise platform integrations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_credentials = config.get("credentials", {})
        self.base_url = config.get("base_url", "")
        
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the platform."""
        pass
    
    @abstractmethod
    async def deploy_content(
        self, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy threat content through the platform."""
        pass
    
    @abstractmethod
    async def get_campaign_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Retrieve campaign metrics from the platform."""
        pass


class Microsoft365Integration(PlatformIntegration):
    """Integration with Microsoft 365 for email-based threat deployment."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.tenant_id = config.get("tenant_id")
        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.graph_api_url = "https://graph.microsoft.com/v1.0"
        self.access_token = None
        
    async def authenticate(self) -> bool:
        """Authenticate with Microsoft Graph API."""
        
        auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(auth_url, data=auth_data) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data.get("access_token")
                        return True
                    else:
                        print(f"Authentication failed: {response.status}")
                        return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    async def deploy_content(
        self, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy phishing emails through Microsoft 365."""
        
        if not self.access_token:
            await self.authenticate()
        
        deployment_id = str(uuid4())
        start_time = datetime.utcnow()
        
        successful_deployments = 0
        failed_deployments = 0
        tracking_ids = []
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Send emails through Graph API
        async with aiohttp.ClientSession() as session:
            for target in targets:
                try:
                    # Construct email message
                    email_message = {
                        "message": {
                            "subject": content.get("subject", ""),
                            "body": {
                                "contentType": "HTML",
                                "content": content.get("body_html", "")
                            },
                            "toRecipients": [
                                {
                                    "emailAddress": {
                                        "address": target.get("email"),
                                        "name": target.get("name", "")
                                    }
                                }
                            ],
                            "from": {
                                "emailAddress": {
                                    "address": content.get("sender_email"),
                                    "name": content.get("sender_name", "")
                                }
                            }
                        },
                        "saveToSentItems": False
                    }
                    
                    # Send email via Graph API
                    send_url = f"{self.graph_api_url}/users/{content.get('sender_email')}/sendMail"
                    
                    async with session.post(
                        send_url, 
                        headers=headers, 
                        json=email_message
                    ) as response:
                        
                        if response.status == 202:  # Accepted
                            tracking_id = str(uuid4())
                            tracking_ids.append(tracking_id)
                            successful_deployments += 1
                        else:
                            failed_deployments += 1
                            error_text = await response.text()
                            print(f"Failed to send email to {target.get('email')}: {error_text}")
                
                except Exception as e:
                    failed_deployments += 1
                    print(f"Error sending email: {e}")
        
        deployment_duration = (datetime.utcnow() - start_time).total_seconds()
        
        return DeploymentResult(
            deployment_id=deployment_id,
            channel=DeploymentChannel.EMAIL,
            status="completed" if failed_deployments == 0 else "partial",
            targets_attempted=len(targets),
            targets_successful=successful_deployments,
            targets_failed=failed_deployments,
            deployment_start=start_time,
            deployment_duration_seconds=deployment_duration,
            tracking_ids=tracking_ids,
            deployment_details={
                "platform": "Microsoft 365",
                "api_version": "v1.0",
                "sender_email": content.get("sender_email")
            }
        )
    
    async def get_campaign_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Retrieve campaign metrics from Microsoft 365."""
        
        # Query message trace and delivery reports
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # In production, this would query actual M365 reporting APIs
        # For now, return mock metrics
        
        return CampaignMetrics(
            campaign_id=campaign_id,
            emails_sent=100,
            emails_delivered=95,
            emails_opened=45,
            links_clicked=12,
            credentials_submitted=3
        )
    
    async def get_user_activity(self, user_email: str, days: int = 7) -> Dict[str, Any]:
        """Get user activity data from Microsoft 365."""
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Query user activity through Graph API
        activity_url = f"{self.graph_api_url}/users/{user_email}/activities"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(activity_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}


class ProofpointIntegration(PlatformIntegration):
    """Integration with Proofpoint for email security and threat simulation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://tap-api-v2.proofpoint.com")
        
    async def authenticate(self) -> bool:
        """Authenticate with Proofpoint API."""
        # Proofpoint uses API key authentication
        return bool(self.api_key)
    
    async def deploy_content(
        self, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy simulated threats through Proofpoint."""
        
        deployment_id = str(uuid4())
        start_time = datetime.utcnow()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create simulation campaign
        campaign_data = {
            "name": content.get("campaign_name", f"ThreatGPT Campaign {deployment_id}"),
            "description": content.get("description", "AI-generated threat simulation"),
            "template": {
                "subject": content.get("subject"),
                "body": content.get("body_html"),
                "sender": content.get("sender_email")
            },
            "targets": [
                {
                    "email": target.get("email"),
                    "firstName": target.get("first_name", ""),
                    "lastName": target.get("last_name", "")
                }
                for target in targets
            ],
            "schedule": {
                "startTime": datetime.utcnow().isoformat(),
                "duration": content.get("duration_hours", 24) * 3600
            }
        }
        
        # Submit simulation campaign
        async with aiohttp.ClientSession() as session:
            create_url = f"{self.base_url}/v2/people/campaigns"
            
            async with session.post(
                create_url, 
                headers=headers, 
                json=campaign_data
            ) as response:
                
                if response.status == 201:
                    campaign_response = await response.json()
                    proofpoint_campaign_id = campaign_response.get("id")
                    
                    deployment_result = DeploymentResult(
                        deployment_id=deployment_id,
                        channel=DeploymentChannel.EMAIL,
                        status="active",
                        targets_attempted=len(targets),
                        targets_successful=len(targets),
                        targets_failed=0,
                        deployment_start=start_time,
                        deployment_duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                        tracking_ids=[proofpoint_campaign_id],
                        deployment_details={
                            "platform": "Proofpoint",
                            "campaign_id": proofpoint_campaign_id,
                            "simulation_type": "phishing"
                        }
                    )
                    
                    return deployment_result
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create Proofpoint campaign: {error_text}")
    
    async def get_campaign_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Retrieve campaign metrics from Proofpoint."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Get campaign results
        results_url = f"{self.base_url}/v2/people/campaigns/{campaign_id}/results"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(results_url, headers=headers) as response:
                if response.status == 200:
                    results_data = await response.json()
                    
                    # Parse Proofpoint metrics format
                    return CampaignMetrics(
                        campaign_id=campaign_id,
                        emails_sent=results_data.get("emailsSent", 0),
                        emails_delivered=results_data.get("emailsDelivered", 0),
                        emails_opened=results_data.get("emailsOpened", 0),
                        links_clicked=results_data.get("linksClicked", 0),
                        attachments_downloaded=results_data.get("attachmentsDownloaded", 0),
                        credentials_submitted=results_data.get("credentialsSubmitted", 0)
                    )
                else:
                    return CampaignMetrics(campaign_id=campaign_id)


class KnowBe4Integration(PlatformIntegration):
    """Integration with KnowBe4 for security awareness training."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://us.api.knowbe4.com")
        
    async def authenticate(self) -> bool:
        """Authenticate with KnowBe4 API."""
        return bool(self.api_key)
    
    async def deploy_content(
        self, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy phishing simulation through KnowBe4."""
        
        deployment_id = str(uuid4())
        start_time = datetime.utcnow()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create phishing campaign
        campaign_data = {
            "name": content.get("campaign_name", f"ThreatGPT Campaign {deployment_id}"),
            "groups": [group["id"] for group in content.get("target_groups", [])],
            "phish_prone_percentage": content.get("phish_prone_percentage", 100),
            "template": {
                "name": content.get("template_name", "Custom ThreatGPT Template"),
                "category": content.get("category", "Phishing"),
                "difficulty": content.get("difficulty", "Medium"),
                "content": {
                    "subject": content.get("subject"),
                    "body": content.get("body_html"),
                    "from_address": content.get("sender_email")
                }
            },
            "schedule": {
                "start_date": datetime.utcnow().isoformat(),
                "duration_weeks": content.get("duration_weeks", 2)
            }
        }
        
        # Submit campaign
        async with aiohttp.ClientSession() as session:
            create_url = f"{self.base_url}/v1/phishing/campaigns"
            
            async with session.post(
                create_url, 
                headers=headers, 
                json=campaign_data
            ) as response:
                
                if response.status == 201:
                    campaign_response = await response.json()
                    knowbe4_campaign_id = campaign_response.get("campaign_id")
                    
                    return DeploymentResult(
                        deployment_id=deployment_id,
                        channel=DeploymentChannel.EMAIL,
                        status="active",
                        targets_attempted=len(targets),
                        targets_successful=len(targets),
                        targets_failed=0,
                        deployment_start=start_time,
                        deployment_duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                        tracking_ids=[knowbe4_campaign_id],
                        deployment_details={
                            "platform": "KnowBe4",
                            "campaign_id": knowbe4_campaign_id,
                            "simulation_type": "phishing_awareness"
                        }
                    )
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create KnowBe4 campaign: {error_text}")
    
    async def get_campaign_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Retrieve campaign metrics from KnowBe4."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Get campaign statistics
        stats_url = f"{self.base_url}/v1/phishing/campaigns/{campaign_id}/stats"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(stats_url, headers=headers) as response:
                if response.status == 200:
                    stats_data = await response.json()
                    
                    return CampaignMetrics(
                        campaign_id=campaign_id,
                        emails_sent=stats_data.get("emails_sent", 0),
                        emails_delivered=stats_data.get("emails_delivered", 0),
                        emails_opened=stats_data.get("emails_opened", 0),
                        links_clicked=stats_data.get("links_clicked", 0),
                        credentials_submitted=stats_data.get("credentials_entered", 0),
                        training_effectiveness_score=stats_data.get("training_score", 0.0),
                        security_awareness_improvement=stats_data.get("awareness_improvement", 0.0)
                    )
                else:
                    return CampaignMetrics(campaign_id=campaign_id)


class SlackIntegration(PlatformIntegration):
    """Integration with Slack for social engineering simulations."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.bot_token = config.get("bot_token")
        self.base_url = "https://slack.com/api"
        
    async def authenticate(self) -> bool:
        """Authenticate with Slack API."""
        
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/auth.test", headers=headers) as response:
                return response.status == 200
    
    async def deploy_content(
        self, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy social engineering messages through Slack."""
        
        deployment_id = str(uuid4())
        start_time = datetime.utcnow()
        
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        successful_deployments = 0
        failed_deployments = 0
        tracking_ids = []
        
        # Send messages to targets
        async with aiohttp.ClientSession() as session:
            for target in targets:
                try:
                    # Personalize message
                    message = content.get("message", "").replace(
                        "{target_name}", target.get("name", "")
                    )
                    
                    # Send direct message
                    message_data = {
                        "channel": target.get("user_id"),
                        "text": message,
                        "as_user": False,
                        "username": content.get("bot_name", "ThreatBot"),
                        "icon_emoji": content.get("icon_emoji", ":robot_face:")
                    }
                    
                    async with session.post(
                        f"{self.base_url}/chat.postMessage",
                        headers=headers,
                        json=message_data
                    ) as response:
                        
                        if response.status == 200:
                            response_data = await response.json()
                            if response_data.get("ok"):
                                tracking_id = response_data.get("ts")
                                tracking_ids.append(tracking_id)
                                successful_deployments += 1
                            else:
                                failed_deployments += 1
                        else:
                            failed_deployments += 1
                
                except Exception as e:
                    failed_deployments += 1
                    print(f"Error sending Slack message: {e}")
        
        deployment_duration = (datetime.utcnow() - start_time).total_seconds()
        
        return DeploymentResult(
            deployment_id=deployment_id,
            channel=DeploymentChannel.SOCIAL_MEDIA,
            status="completed" if failed_deployments == 0 else "partial",
            targets_attempted=len(targets),
            targets_successful=successful_deployments,
            targets_failed=failed_deployments,
            deployment_start=start_time,
            deployment_duration_seconds=deployment_duration,
            tracking_ids=tracking_ids,
            deployment_details={
                "platform": "Slack",
                "message_type": "direct_message",
                "bot_name": content.get("bot_name")
            }
        )
    
    async def get_campaign_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Retrieve campaign metrics from Slack."""
        
        # Slack doesn't have built-in campaign metrics
        # Would need to track interactions through webhook endpoints
        
        return CampaignMetrics(
            campaign_id=campaign_id,
            # Mock some basic metrics
            emails_sent=0,  # Not applicable for Slack
            links_clicked=5,  # Track through webhook
            verification_attempts=2
        )


class PlatformIntegrationManager:
    """Manager for all enterprise platform integrations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.integrations = {}
        
        # Initialize available integrations
        if "microsoft365" in config:
            self.integrations["microsoft365"] = Microsoft365Integration(config["microsoft365"])
        
        if "proofpoint" in config:
            self.integrations["proofpoint"] = ProofpointIntegration(config["proofpoint"])
        
        if "knowbe4" in config:
            self.integrations["knowbe4"] = KnowBe4Integration(config["knowbe4"])
        
        if "slack" in config:
            self.integrations["slack"] = SlackIntegration(config["slack"])
    
    async def authenticate_all(self) -> Dict[str, bool]:
        """Authenticate with all configured platforms."""
        
        auth_results = {}
        
        for platform_name, integration in self.integrations.items():
            try:
                auth_results[platform_name] = await integration.authenticate()
            except Exception as e:
                print(f"Authentication failed for {platform_name}: {e}")
                auth_results[platform_name] = False
        
        return auth_results
    
    async def deploy_through_platform(
        self, 
        platform_name: str, 
        content: Dict[str, Any], 
        targets: List[Dict[str, Any]]
    ) -> Optional[DeploymentResult]:
        """Deploy content through a specific platform."""
        
        if platform_name not in self.integrations:
            raise ValueError(f"Platform {platform_name} not configured")
        
        integration = self.integrations[platform_name]
        
        # ensure authentication
        if not await integration.authenticate():
            raise Exception(f"Failed to authenticate with {platform_name}")
        
        return await integration.deploy_content(content, targets)
    
    async def get_all_campaign_metrics(self, campaign_id: str) -> Dict[str, CampaignMetrics]:
        """Get campaign metrics from all platforms."""
        
        all_metrics = {}
        
        for platform_name, integration in self.integrations.items():
            try:
                metrics = await integration.get_campaign_metrics(campaign_id)
                all_metrics[platform_name] = metrics
            except Exception as e:
                print(f"Failed to get metrics from {platform_name}: {e}")
                all_metrics[platform_name] = CampaignMetrics(campaign_id=campaign_id)
        
        return all_metrics
    
    def get_available_platforms(self) -> List[str]:
        """Get list of available platform integrations."""
        return list(self.integrations.keys())
    
    async def test_platform_connectivity(self, platform_name: str) -> Dict[str, Any]:
        """Test connectivity and functionality of a platform integration."""
        
        if platform_name not in self.integrations:
            return {"error": f"Platform {platform_name} not configured"}
        
        integration = self.integrations[platform_name]
        
        try:
            # Test authentication
            auth_success = await integration.authenticate()
            
            return {
                "platform": platform_name,
                "authentication": auth_success,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy" if auth_success else "authentication_failed"
            }
        
        except Exception as e:
            return {
                "platform": platform_name,
                "authentication": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error"
            }