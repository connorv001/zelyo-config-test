import pytest
from src.parser import parse_kubescape_results
from src.models import Severity

def test_parse_kubescape_results_empty():
    raw_data = {"results": []}
    findings = parse_kubescape_results(raw_data)
    assert findings == []

def test_parse_kubescape_results_basic():
    # This is a simplified version of what Kubescape actually returns
    # We need to map it to our Finding model.
    raw_data = {
        "results": [
            {
                "resourceID": "apps/v1/Deployment/my-app",
                "controls": [
                    {
                        "controlID": "C-0001",
                        "name": "Privileged container",
                        "status": {"status": "failed"},
                        "rules": [
                            {
                                "name": "rule-1",
                                "paths": [{"failedPath": "spec.template.spec.containers[0].securityContext.privileged"}]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    findings = parse_kubescape_results(raw_data)
    assert len(findings) == 1
    assert findings[0].resource_id == "apps/v1/Deployment/my-app"
    assert findings[0].control_id == "C-0001"
