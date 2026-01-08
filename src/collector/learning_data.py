"""
Zelyo Data Collector - Anonymized Telemetry for Continuous Learning

Collects anonymized data about:
- Findings detected (control IDs, severity distribution)
- Remediations generated (success/failure, types)
- Patterns in security issues
- LLM response quality metrics

This data is used to:
1. Build IP for Zelyo's continuous learning
2. Improve remediation suggestions over time
3. Identify common security patterns
4. Train future ML models

Privacy: All data is anonymized - no secrets, tokens, or PII are collected.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from pathlib import Path


class FindingEvent(BaseModel):
    """Anonymized finding event."""
    event_type: str = "finding"
    timestamp: str
    control_id: str
    severity: str
    resource_type: str  # e.g., "Deployment", "ServiceAccount" (no names)
    namespace_hash: str  # Hashed namespace
    cluster_hash: str  # Hashed cluster identifier


class RemediationEvent(BaseModel):
    """Anonymized remediation event."""
    event_type: str = "remediation"
    timestamp: str
    control_id: str
    severity: str
    is_auto_fixable: bool
    requires_escalation: bool
    llm_provider: str
    response_time_ms: int
    success: bool
    error_type: Optional[str] = None


class PREvent(BaseModel):
    """Anonymized PR creation event."""
    event_type: str = "pr_created"
    timestamp: str
    control_id: str
    severity: str
    pr_created: bool
    escalation_issue_created: bool


class LearningDataCollector:
    """
    Collects anonymized telemetry for continuous learning.
    
    Data is stored locally and can optionally be sent to a central server.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or os.getenv(
            "ZELYO_DATA_PATH", 
            "/var/lib/zelyo/learning_data"
        ))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Central telemetry endpoint (optional, disabled by default)
        self.telemetry_enabled = os.getenv("ZELYO_TELEMETRY_ENABLED", "false").lower() == "true"
        self.telemetry_endpoint = os.getenv("ZELYO_TELEMETRY_ENDPOINT", "")
        
        # Session tracking
        self.session_id = self._generate_session_id()
        self.events: List[Dict[str, Any]] = []
    
    def _generate_session_id(self) -> str:
        """Generate anonymous session ID."""
        return hashlib.sha256(
            f"{datetime.now().isoformat()}{os.getpid()}".encode()
        ).hexdigest()[:16]
    
    def _anonymize_resource(self, resource_id: str) -> str:
        """Extract resource type without sensitive names."""
        # e.g., "apps/v1/default/Deployment/my-app" -> "Deployment"
        parts = resource_id.split("/")
        for part in parts:
            if part in ["Deployment", "DaemonSet", "StatefulSet", "Pod", 
                       "Service", "ServiceAccount", "ConfigMap", "Secret",
                       "ClusterRole", "Role", "ClusterRoleBinding", "RoleBinding",
                       "Namespace", "Ingress", "NetworkPolicy"]:
                return part
        return "Unknown"
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash sensitive identifiers."""
        return hashlib.sha256(identifier.encode()).hexdigest()[:12]
    
    def collect_finding(
        self,
        control_id: str,
        severity: str,
        resource_id: str,
        namespace: str = "default",
        cluster_name: str = "unknown"
    ):
        """Collect anonymized finding data."""
        event = FindingEvent(
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            severity=severity,
            resource_type=self._anonymize_resource(resource_id),
            namespace_hash=self._hash_identifier(namespace),
            cluster_hash=self._hash_identifier(cluster_name),
        )
        self._store_event(event.model_dump())
    
    def collect_remediation(
        self,
        control_id: str,
        severity: str,
        is_auto_fixable: bool,
        requires_escalation: bool,
        llm_provider: str,
        response_time_ms: int,
        success: bool,
        error_type: Optional[str] = None
    ):
        """Collect anonymized remediation data."""
        event = RemediationEvent(
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            severity=severity,
            is_auto_fixable=is_auto_fixable,
            requires_escalation=requires_escalation,
            llm_provider=llm_provider,
            response_time_ms=response_time_ms,
            success=success,
            error_type=error_type,
        )
        self._store_event(event.model_dump())
    
    def collect_pr_event(
        self,
        control_id: str,
        severity: str,
        pr_created: bool,
        escalation_issue_created: bool = False
    ):
        """Collect anonymized PR creation data."""
        event = PREvent(
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            severity=severity,
            pr_created=pr_created,
            escalation_issue_created=escalation_issue_created,
        )
        self._store_event(event.model_dump())
    
    def _store_event(self, event: Dict[str, Any]):
        """Store event to local file and optionally send to telemetry endpoint."""
        event["session_id"] = self.session_id
        self.events.append(event)
        
        # Write to local JSONL file
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = self.storage_path / f"events_{date_str}.jsonl"
        
        with open(file_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Optionally send to central telemetry (if enabled)
        if self.telemetry_enabled and self.telemetry_endpoint:
            self._send_telemetry(event)
    
    def _send_telemetry(self, event: Dict[str, Any]):
        """Send telemetry to central server (async, fire-and-forget)."""
        try:
            import httpx
            # Fire and forget - don't block on telemetry
            # In production, this would be async/queued
            httpx.post(
                self.telemetry_endpoint,
                json=event,
                timeout=1.0,
            )
        except Exception:
            pass  # Never fail on telemetry
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics for current session."""
        findings = [e for e in self.events if e.get("event_type") == "finding"]
        remediations = [e for e in self.events if e.get("event_type") == "remediation"]
        prs = [e for e in self.events if e.get("event_type") == "pr_created"]
        
        return {
            "session_id": self.session_id,
            "total_events": len(self.events),
            "findings_count": len(findings),
            "remediations_count": len(remediations),
            "prs_created": len([p for p in prs if p.get("pr_created")]),
            "escalations": len([p for p in prs if p.get("escalation_issue_created")]),
            "auto_fixable_ratio": (
                sum(1 for r in remediations if r.get("is_auto_fixable")) / len(remediations)
                if remediations else 0
            ),
            "control_id_distribution": self._get_distribution(findings, "control_id"),
            "severity_distribution": self._get_distribution(findings, "severity"),
        }
    
    def _get_distribution(self, events: List[Dict], key: str) -> Dict[str, int]:
        """Get distribution of a key across events."""
        dist = {}
        for e in events:
            val = e.get(key, "unknown")
            dist[val] = dist.get(val, 0) + 1
        return dist
    
    def export_for_training(self, output_path: Optional[str] = None) -> str:
        """Export all collected data in a format suitable for ML training."""
        output_path = output_path or str(self.storage_path / "training_export.json")
        
        all_events = []
        for jsonl_file in self.storage_path.glob("events_*.jsonl"):
            with open(jsonl_file) as f:
                for line in f:
                    if line.strip():
                        all_events.append(json.loads(line))
        
        export_data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "event_count": len(all_events),
            "events": all_events,
        }
        
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)
        
        return output_path


# Global collector instance
_collector: Optional[LearningDataCollector] = None


def get_collector() -> LearningDataCollector:
    """Get or create global collector instance."""
    global _collector
    if _collector is None:
        _collector = LearningDataCollector()
    return _collector
