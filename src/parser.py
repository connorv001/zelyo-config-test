from typing import Any, Dict, List
from uuid import uuid4
from src.models import Finding, Severity

def parse_kubescape_results(raw_data: Dict[str, Any]) -> List[Finding]:
    findings = []
    results = raw_data.get("results", [])
    
    for result in results:
        resource_id = result.get("resourceID", "unknown")
        controls = result.get("controls", [])
        
        for control in controls:
            status = control.get("status", {}).get("status")
            if status == "failed":
                finding = Finding(
                    id=uuid4(),
                    resource_id=resource_id,
                    severity=Severity.UNKNOWN,  # Simplified for now
                    control_id=control.get("controlID", "unknown"),
                    description=control.get("name", ""),
                    remediation="Refer to Kubescape documentation for control " + control.get("controlID", "")
                )
                findings.append(finding)
                
    return findings
