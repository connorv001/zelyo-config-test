"""Remediation Engine - LLM-powered fix generation."""

import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from src.llm.provider import LLMClient
from src.llm.prompts import REMEDIATION_SYSTEM_PROMPT, FINDING_ANALYSIS_TEMPLATE


class RemediationAnalysis(BaseModel):
    """Analysis output from remediation engine."""
    severity: str
    risk_summary: str
    is_auto_fixable: bool
    requires_escalation: bool
    escalation_reason: Optional[str] = None


class RemediationOutput(BaseModel):
    """Full remediation output."""
    strategy: str
    yaml_patch: Optional[str] = None
    target_file: Optional[str] = None
    manual_steps: Optional[list] = None


class PRMetadata(BaseModel):
    """PR metadata for GitHub integration."""
    title: str
    description: str


class RemediationResult(BaseModel):
    """Complete remediation result."""
    finding_id: str
    control_id: str
    analysis: RemediationAnalysis
    remediation: RemediationOutput
    pr_metadata: PRMetadata


class RemediationEngine:
    """LLM-powered remediation engine for Kubernetes findings."""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    async def analyze_finding(self, finding: Dict[str, Any]) -> RemediationResult:
        """
        Analyze a finding and generate remediation.
        
        Args:
            finding: Dict with control_id, description, resource_id, severity, remediation
            
        Returns:
            RemediationResult with analysis, fix, and PR metadata
        """
        # Format the prompt
        user_prompt = FINDING_ANALYSIS_TEMPLATE.format(
            control_id=finding.get("control_id", "unknown"),
            description=finding.get("description", "No description"),
            resource_id=finding.get("resource_id", "unknown"),
            severity=finding.get("severity", "Unknown"),
            remediation=finding.get("remediation", "No hint available"),
        )
        
        # Call LLM
        response = await self.llm_client.invoke(
            system_prompt=REMEDIATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        
        # Parse JSON response
        try:
            # Handle potential markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            data = json.loads(response.strip())
        except json.JSONDecodeError:
            # Fallback for malformed responses
            data = {
                "analysis": {
                    "severity": "unknown",
                    "risk_summary": "Failed to parse LLM response",
                    "is_auto_fixable": False,
                    "requires_escalation": True,
                    "escalation_reason": "LLM response parsing failed"
                },
                "remediation": {
                    "strategy": "Manual review required",
                    "yaml_patch": None,
                    "target_file": None,
                    "manual_steps": ["Review finding manually", "Consult Kubescape documentation"]
                },
                "pr_metadata": {
                    "title": f"[REVIEW] {finding.get('control_id', 'unknown')}",
                    "description": "Automated remediation could not be generated."
                }
            }
        
        return RemediationResult(
            finding_id=str(finding.get("id", "unknown")),
            control_id=finding.get("control_id", "unknown"),
            analysis=RemediationAnalysis(**data.get("analysis", {})),
            remediation=RemediationOutput(**data.get("remediation", {})),
            pr_metadata=PRMetadata(**data.get("pr_metadata", {})),
        )
    
    def analyze_finding_sync(self, finding: Dict[str, Any]) -> RemediationResult:
        """Synchronous version for simpler use cases."""
        import asyncio
        return asyncio.run(self.analyze_finding(finding))
