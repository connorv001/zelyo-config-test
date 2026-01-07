import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from src.models import Finding, ScanResult, Severity

def test_finding_creation():
    finding_data = {
        "id": uuid4(),
        "resource_id": "apps/v1/Deployment/my-app",
        "severity": Severity.HIGH,
        "control_id": "C-0001",
        "description": "Privileged container detected",
        "remediation": "Set privileged: false in securityContext"
    }
    finding = Finding(**finding_data)
    assert finding.resource_id == "apps/v1/Deployment/my-app"
    assert finding.severity == Severity.HIGH

def test_finding_invalid_severity():
    finding_data = {
        "id": uuid4(),
        "resource_id": "apps/v1/Deployment/my-app",
        "severity": "INVALID",
        "control_id": "C-0001",
        "description": "Test",
        "remediation": "Test"
    }
    with pytest.raises(ValidationError):
        Finding(**finding_data)

def test_scan_result_creation():
    finding = Finding(
        id=uuid4(),
        resource_id="v1/Pod/test",
        severity=Severity.LOW,
        control_id="C-0002",
        description="test",
        remediation="test"
    )
    result = ScanResult(
        scan_id=uuid4(),
        timestamp=datetime.now(),
        findings=[finding]
    )
    assert len(result.findings) == 1
    assert result.findings[0].severity == Severity.LOW