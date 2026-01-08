"""API routes for Zelyo Config Guardian."""

from fastapi import APIRouter, HTTPException
from src.scanner import run_scan
from src.parser import parse_kubescape_results
from src.models import Finding
from uuid import uuid4
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import os

router = APIRouter()

# In-memory storage
findings_store: List[Finding] = []


# =============================================================================
# SCAN ENDPOINTS
# =============================================================================

@router.post("/scan")
async def trigger_scan():
    """Trigger a Kubernetes configuration/security scan."""
    global findings_store
    
    raw_results = await run_scan()
    findings = parse_kubescape_results(raw_results)
    findings_store = findings
    
    return {
        "scan_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(),
        "findings_count": len(findings),
        "findings": [f.model_dump() for f in findings]
    }


@router.get("/findings")
def get_findings():
    """Get all findings from the last scan."""
    return [f.model_dump() for f in findings_store]


@router.get("/findings/{finding_id}")
def get_finding(finding_id: str):
    """Get a specific finding by ID."""
    for f in findings_store:
        if str(f.id) == finding_id:
            return f.model_dump()
    raise HTTPException(status_code=404, detail="Finding not found")


# =============================================================================
# REMEDIATION ENDPOINTS
# =============================================================================

class RemediateRequest(BaseModel):
    """Request body for remediation."""
    finding_id: str


class RemediateResponse(BaseModel):
    """Response from remediation engine."""
    finding_id: str
    control_id: str
    severity: str
    risk_summary: str
    is_auto_fixable: bool
    requires_escalation: bool
    escalation_reason: Optional[str] = None
    strategy: str
    yaml_patch: Optional[str] = None
    manual_steps: Optional[List[str]] = None
    pr_title: str
    pr_description: str


@router.post("/remediate", response_model=RemediateResponse)
async def remediate_finding(request: RemediateRequest):
    """
    Analyze a finding and generate remediation using LLM.
    
    Requires LLM_PROVIDER and corresponding API key to be set.
    """
    # Check if LLM is configured
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENROUTER_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="No LLM API key configured. Set OPENAI_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY."
        )
    
    # Find the finding
    finding = None
    for f in findings_store:
        if str(f.id) == request.finding_id:
            finding = f
            break
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    # Import here to avoid import errors when LLM deps aren't installed
    from src.remediation.engine import RemediationEngine
    
    engine = RemediationEngine()
    result = await engine.analyze_finding(finding.model_dump())
    
    return RemediateResponse(
        finding_id=result.finding_id,
        control_id=result.control_id,
        severity=result.analysis.severity,
        risk_summary=result.analysis.risk_summary,
        is_auto_fixable=result.analysis.is_auto_fixable,
        requires_escalation=result.analysis.requires_escalation,
        escalation_reason=result.analysis.escalation_reason,
        strategy=result.remediation.strategy,
        yaml_patch=result.remediation.yaml_patch,
        manual_steps=result.remediation.manual_steps,
        pr_title=result.pr_metadata.title,
        pr_description=result.pr_metadata.description,
    )


# =============================================================================
# GITHUB PR ENDPOINTS
# =============================================================================

class CreatePRRequest(BaseModel):
    """Request body for PR creation."""
    finding_id: str
    yaml_patch: str
    fix_strategy: str
    risk_summary: str
    file_path: Optional[str] = None


class CreatePRResponse(BaseModel):
    """Response from PR creation."""
    pr_url: str
    pr_number: int
    branch_name: str
    file_path: str


@router.post("/create-pr", response_model=CreatePRResponse)
async def create_pr(request: CreatePRRequest):
    """
    Create a GitHub PR with the remediation fix.
    
    Requires GITHUB_TOKEN and GITHUB_REPO to be set.
    """
    # Check GitHub configuration
    if not os.getenv("GITHUB_TOKEN"):
        raise HTTPException(status_code=503, detail="GITHUB_TOKEN not configured")
    if not os.getenv("GITHUB_REPO"):
        raise HTTPException(status_code=503, detail="GITHUB_REPO not configured")
    
    # Find the finding
    finding = None
    for f in findings_store:
        if str(f.id) == request.finding_id:
            finding = f
            break
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    from src.github.pr_creator import GitHubPRCreator
    
    creator = GitHubPRCreator()
    result = creator.create_remediation_pr(
        control_id=finding.control_id,
        description=finding.description,
        resource_id=finding.resource_id,
        severity=finding.severity.value if hasattr(finding.severity, 'value') else str(finding.severity),
        yaml_patch=request.yaml_patch,
        fix_strategy=request.fix_strategy,
        risk_summary=request.risk_summary,
        file_path=request.file_path,
    )
    
    return CreatePRResponse(**result)


class EscalateRequest(BaseModel):
    """Request body for escalation."""
    finding_id: str
    escalation_reason: str


class EscalateResponse(BaseModel):
    """Response from escalation."""
    issue_url: str
    issue_number: int


@router.post("/escalate", response_model=EscalateResponse)
async def escalate_finding(request: EscalateRequest):
    """
    Create a GitHub issue for findings that need human escalation.
    
    Requires GITHUB_TOKEN and GITHUB_REPO to be set.
    """
    if not os.getenv("GITHUB_TOKEN"):
        raise HTTPException(status_code=503, detail="GITHUB_TOKEN not configured")
    if not os.getenv("GITHUB_REPO"):
        raise HTTPException(status_code=503, detail="GITHUB_REPO not configured")
    
    finding = None
    for f in findings_store:
        if str(f.id) == request.finding_id:
            finding = f
            break
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    from src.github.pr_creator import GitHubPRCreator
    
    creator = GitHubPRCreator()
    result = creator.create_escalation_issue(
        control_id=finding.control_id,
        description=finding.description,
        resource_id=finding.resource_id,
        severity=finding.severity.value if hasattr(finding.severity, 'value') else str(finding.severity),
        escalation_reason=request.escalation_reason,
    )
    
    return EscalateResponse(**result)


# =============================================================================
# HEALTH & CONFIG
# =============================================================================

@router.get("/config")
def get_config():
    """Get current configuration status (no secrets exposed)."""
    return {
        "llm_provider": os.getenv("LLM_PROVIDER", "not_set"),
        "llm_configured": bool(
            os.getenv("OPENAI_API_KEY") or 
            os.getenv("GEMINI_API_KEY") or 
            os.getenv("OPENROUTER_API_KEY")
        ),
        "github_configured": bool(os.getenv("GITHUB_TOKEN") and os.getenv("GITHUB_REPO")),
        "github_repo": os.getenv("GITHUB_REPO", "not_set"),
        "mcp_server_url": os.getenv("MCP_SERVER_URL", "http://localhost:8090/sse"),
        "telemetry_enabled": os.getenv("ZELYO_TELEMETRY_ENABLED", "false"),
    }


# =============================================================================
# DATA COLLECTOR / CONTINUOUS LEARNING
# =============================================================================

@router.get("/collector/stats")
def get_collector_stats():
    """Get anonymized statistics from the learning data collector."""
    from src.collector.learning_data import get_collector
    collector = get_collector()
    return collector.get_session_stats()


@router.post("/collector/export")
def export_collector_data():
    """Export all collected data for ML training."""
    from src.collector.learning_data import get_collector
    collector = get_collector()
    export_path = collector.export_for_training()
    return {
        "status": "exported",
        "path": export_path,
        "event_count": len(collector.events),
    }

