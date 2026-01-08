"""
Zelyo IP Data Collector - Comprehensive Data for Continuous Learning

This module captures anonymized data specifically for building IP:
1. Remediation patterns - What fixes work for which control types
2. LLM performance - Response quality, latency, success rates by model
3. User feedback - Which PRs get approved vs rejected
4. Cluster patterns - Common misconfiguration patterns across deployments

All data is anonymized and GDPR/privacy compliant.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum


class EventType(str, Enum):
    SCAN = "scan"
    FINDING = "finding"
    REMEDIATION = "remediation"
    PR_CREATED = "pr_created"
    PR_MERGED = "pr_merged"
    PR_REJECTED = "pr_rejected"
    ESCALATION = "escalation"
    USER_FEEDBACK = "user_feedback"
    LLM_CALL = "llm_call"


@dataclass
class ScanEvent:
    """Scan-level metrics for pattern analysis."""
    event_type: str = EventType.SCAN
    timestamp: str = ""
    cluster_hash: str = ""  # Anonymized cluster ID
    total_findings: int = 0
    security_findings: int = 0
    config_findings: int = 0
    scan_duration_ms: int = 0
    kubescape_version: str = ""
    
    # Distribution data for pattern analysis
    control_id_counts: Dict[str, int] = None
    severity_distribution: Dict[str, int] = None
    resource_type_distribution: Dict[str, int] = None


@dataclass
class FindingPattern:
    """Individual finding data for ML training."""
    event_type: str = EventType.FINDING
    timestamp: str = ""
    
    # Core finding data (anonymized)
    control_id: str = ""
    severity: str = ""
    resource_type: str = ""  # e.g., "Deployment", not the actual name
    namespace_hash: str = ""
    
    # Context for learning
    related_controls: List[str] = None  # Other controls on same resource
    cluster_size_bucket: str = ""  # "small", "medium", "large"
    namespace_type: str = ""  # "system", "application", "unknown"


@dataclass
class RemediationPattern:
    """Remediation data for training fix generation models."""
    event_type: str = EventType.REMEDIATION
    timestamp: str = ""
    
    # Finding context
    control_id: str = ""
    severity: str = ""
    resource_type: str = ""
    
    # LLM performance metrics
    llm_provider: str = ""
    llm_model: str = ""
    response_time_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    
    # Remediation analysis
    is_auto_fixable: bool = False
    requires_escalation: bool = False
    escalation_reason: Optional[str] = None
    
    # Fix categorization (for pattern learning)
    fix_type: str = ""  # "add_security_context", "add_resource_limits", etc.
    fix_complexity: str = ""  # "simple", "moderate", "complex"
    
    # Outcome
    success: bool = False
    error_type: Optional[str] = None


@dataclass
class PROutcome:
    """PR lifecycle data for feedback learning."""
    event_type: str = EventType.PR_CREATED
    timestamp: str = ""
    
    # Context
    control_id: str = ""
    severity: str = ""
    fix_type: str = ""
    
    # PR data (anonymized)
    pr_id_hash: str = ""  # Hashed PR identifier
    
    # Outcome tracking (updated when PR is merged/rejected)
    time_to_decision_hours: Optional[float] = None
    was_approved: Optional[bool] = None
    required_modifications: Optional[bool] = None
    rejection_reason_category: Optional[str] = None  # "false_positive", "wrong_fix", "not_priority"


@dataclass
class LLMCallMetrics:
    """Detailed LLM performance data for model comparison."""
    event_type: str = EventType.LLM_CALL
    timestamp: str = ""
    
    # Provider details
    provider: str = ""  # "openai", "gemini", "openrouter"
    model: str = ""  # "gpt-4o-mini", "claude-3.5-sonnet", etc.
    
    # Request metrics
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    
    # Performance
    latency_ms: int = 0
    success: bool = False
    error_type: Optional[str] = None
    
    # Quality signals (derived from outcomes)
    response_parseable: bool = True
    generated_valid_yaml: bool = True


class ZelyoIPCollector:
    """
    Comprehensive data collector for building Zelyo's continuous learning IP.
    
    Data categories:
    1. Pattern Recognition - Common misconfigurations, fix patterns
    2. Model Performance - LLM comparison, response quality
    3. Feedback Loop - PR outcomes, user corrections
    4. Cluster Intelligence - Anonymized deployment patterns
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or os.getenv(
            "ZELYO_DATA_PATH", 
            "/var/lib/zelyo/learning_data"
        ))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Telemetry settings
        self.telemetry_enabled = os.getenv("ZELYO_TELEMETRY_ENABLED", "false").lower() == "true"
        self.telemetry_endpoint = os.getenv("ZELYO_TELEMETRY_ENDPOINT", "")
        
        # Session tracking
        self.session_id = self._generate_session_id()
        self.events: List[Dict[str, Any]] = []
        
        # Aggregated metrics (for dashboard)
        self.session_metrics = {
            "scans": 0,
            "findings": 0,
            "remediations": 0,
            "prs_created": 0,
            "llm_calls": 0,
        }
    
    def _generate_session_id(self) -> str:
        return hashlib.sha256(
            f"{datetime.now().isoformat()}{os.getpid()}".encode()
        ).hexdigest()[:16]
    
    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()[:12]
    
    def _anonymize_resource(self, resource_id: str) -> str:
        """Extract resource type only."""
        resource_types = [
            "Deployment", "DaemonSet", "StatefulSet", "Pod", "ReplicaSet",
            "Service", "ServiceAccount", "ConfigMap", "Secret", "Ingress",
            "ClusterRole", "Role", "ClusterRoleBinding", "RoleBinding",
            "Namespace", "NetworkPolicy", "PersistentVolumeClaim",
        ]
        for rt in resource_types:
            if rt in resource_id:
                return rt
        return "Unknown"
    
    def _get_namespace_type(self, namespace: str) -> str:
        """Categorize namespace without exposing name."""
        system_ns = ["kube-system", "kube-public", "kube-node-lease", "argocd", "istio-system"]
        if namespace in system_ns:
            return "system"
        elif namespace == "default":
            return "default"
        else:
            return "application"
    
    # =========================================================================
    # DATA COLLECTION METHODS
    # =========================================================================
    
    def collect_scan(
        self,
        findings: List[Dict],
        duration_ms: int,
        cluster_name: str = "unknown",
    ):
        """Collect scan-level metrics."""
        # Analyze findings
        control_counts = {}
        severity_dist = {}
        resource_dist = {}
        security_count = 0
        config_count = 0
        
        security_controls = ["C-0016", "C-0017", "C-0041", "C-0046", "C-0048", "C-0057"]
        
        for f in findings:
            cid = f.get("control_id", "unknown")
            control_counts[cid] = control_counts.get(cid, 0) + 1
            
            sev = f.get("severity", "unknown")
            severity_dist[sev] = severity_dist.get(sev, 0) + 1
            
            rt = self._anonymize_resource(f.get("resource_id", ""))
            resource_dist[rt] = resource_dist.get(rt, 0) + 1
            
            if cid in security_controls:
                security_count += 1
            else:
                config_count += 1
        
        event = ScanEvent(
            timestamp=datetime.now().isoformat(),
            cluster_hash=self._hash(cluster_name),
            total_findings=len(findings),
            security_findings=security_count,
            config_findings=config_count,
            scan_duration_ms=duration_ms,
            control_id_counts=control_counts,
            severity_distribution=severity_dist,
            resource_type_distribution=resource_dist,
        )
        
        self.session_metrics["scans"] += 1
        self._store_event(asdict(event))
    
    def collect_finding(
        self,
        finding: Dict,
        related_controls: List[str] = None,
        cluster_size: str = "medium",
    ):
        """Collect individual finding for pattern analysis."""
        event = FindingPattern(
            timestamp=datetime.now().isoformat(),
            control_id=finding.get("control_id", ""),
            severity=finding.get("severity", "unknown"),
            resource_type=self._anonymize_resource(finding.get("resource_id", "")),
            namespace_hash=self._hash(finding.get("namespace", "default")),
            related_controls=related_controls or [],
            cluster_size_bucket=cluster_size,
            namespace_type=self._get_namespace_type(finding.get("namespace", "default")),
        )
        
        self.session_metrics["findings"] += 1
        self._store_event(asdict(event))
    
    def collect_remediation(
        self,
        control_id: str,
        severity: str,
        resource_type: str,
        llm_provider: str,
        llm_model: str,
        response_time_ms: int,
        is_auto_fixable: bool,
        requires_escalation: bool,
        fix_type: str,
        success: bool,
        input_tokens: int = 0,
        output_tokens: int = 0,
        escalation_reason: str = None,
        error_type: str = None,
    ):
        """Collect remediation generation data."""
        # Determine fix complexity
        complex_controls = ["C-0035", "C-0036", "C-0037"]
        simple_controls = ["C-0017", "C-0055", "C-0270", "C-0271"]
        
        if control_id in simple_controls:
            complexity = "simple"
        elif control_id in complex_controls:
            complexity = "complex"
        else:
            complexity = "moderate"
        
        event = RemediationPattern(
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            severity=severity,
            resource_type=resource_type,
            llm_provider=llm_provider,
            llm_model=llm_model,
            response_time_ms=response_time_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            is_auto_fixable=is_auto_fixable,
            requires_escalation=requires_escalation,
            escalation_reason=escalation_reason,
            fix_type=fix_type,
            fix_complexity=complexity,
            success=success,
            error_type=error_type,
        )
        
        self.session_metrics["remediations"] += 1
        self._store_event(asdict(event))
    
    def collect_pr_outcome(
        self,
        control_id: str,
        severity: str,
        fix_type: str,
        pr_identifier: str,
        was_approved: bool = None,
        time_to_decision_hours: float = None,
        required_modifications: bool = None,
        rejection_reason: str = None,
    ):
        """Collect PR outcome for feedback loop."""
        if was_approved is None:
            event_type = EventType.PR_CREATED
        elif was_approved:
            event_type = EventType.PR_MERGED
        else:
            event_type = EventType.PR_REJECTED
        
        event = PROutcome(
            event_type=event_type,
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            severity=severity,
            fix_type=fix_type,
            pr_id_hash=self._hash(pr_identifier),
            time_to_decision_hours=time_to_decision_hours,
            was_approved=was_approved,
            required_modifications=required_modifications,
            rejection_reason_category=rejection_reason,
        )
        
        if event_type == EventType.PR_CREATED:
            self.session_metrics["prs_created"] += 1
        self._store_event(asdict(event))
    
    def collect_llm_metrics(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: int,
        success: bool,
        response_parseable: bool = True,
        generated_valid_yaml: bool = True,
        error_type: str = None,
    ):
        """Collect LLM performance metrics."""
        event = LLMCallMetrics(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_ms=latency_ms,
            success=success,
            error_type=error_type,
            response_parseable=response_parseable,
            generated_valid_yaml=generated_valid_yaml,
        )
        
        self.session_metrics["llm_calls"] += 1
        self._store_event(asdict(event))
    
    # =========================================================================
    # STORAGE AND EXPORT
    # =========================================================================
    
    def _store_event(self, event: Dict[str, Any]):
        """Store event locally."""
        event["session_id"] = self.session_id
        self.events.append(event)
        
        # Write to daily JSONL file
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = self.storage_path / f"ip_data_{date_str}.jsonl"
        
        with open(file_path, "a") as f:
            f.write(json.dumps(event, default=str) + "\n")
        
        # Optional telemetry
        if self.telemetry_enabled and self.telemetry_endpoint:
            self._send_telemetry(event)
    
    def _send_telemetry(self, event: Dict):
        """Send to central telemetry (non-blocking)."""
        try:
            import httpx
            httpx.post(self.telemetry_endpoint, json=event, timeout=1.0)
        except Exception:
            pass
    
    def get_ip_summary(self) -> Dict[str, Any]:
        """Get summary of collected IP data."""
        return {
            "session_id": self.session_id,
            "session_metrics": self.session_metrics,
            "total_events": len(self.events),
            "storage_path": str(self.storage_path),
            "telemetry_enabled": self.telemetry_enabled,
        }
    
    def export_training_data(self, output_path: str = None) -> str:
        """Export all data for ML training pipeline."""
        output_path = output_path or str(self.storage_path / "training_export.json")
        
        all_events = []
        for jsonl_file in self.storage_path.glob("ip_data_*.jsonl"):
            with open(jsonl_file) as f:
                for line in f:
                    if line.strip():
                        all_events.append(json.loads(line))
        
        # Organize by event type
        organized = {
            "scans": [e for e in all_events if e.get("event_type") == EventType.SCAN],
            "findings": [e for e in all_events if e.get("event_type") == EventType.FINDING],
            "remediations": [e for e in all_events if e.get("event_type") == EventType.REMEDIATION],
            "pr_outcomes": [e for e in all_events if e.get("event_type") in [EventType.PR_CREATED, EventType.PR_MERGED, EventType.PR_REJECTED]],
            "llm_metrics": [e for e in all_events if e.get("event_type") == EventType.LLM_CALL],
        }
        
        export = {
            "version": "2.0",
            "exported_at": datetime.now().isoformat(),
            "total_events": len(all_events),
            "data": organized,
        }
        
        with open(output_path, "w") as f:
            json.dump(export, f, indent=2, default=str)
        
        return output_path


# Global collector
_ip_collector: Optional[ZelyoIPCollector] = None


def get_ip_collector() -> ZelyoIPCollector:
    """Get or create global IP collector."""
    global _ip_collector
    if _ip_collector is None:
        _ip_collector = ZelyoIPCollector()
    return _ip_collector
