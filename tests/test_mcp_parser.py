import pytest
import json
from src.parser import parse_mcp_resource_response
from src.models import Severity

def test_parse_mcp_resource_response():
    # Simulated Kubescape findings within MCP response
    kubescape_data = {
        "results": [
            {
                "resourceID": "apps/v1/default/Deployment/test",
                "controls": [
                    {
                        "controlID": "C-0001",
                        "name": "Test Control",
                        "status": {"status": "failed"}
                    }
                ]
            }
        ]
    }
    
    mcp_response = {
        "contents": [
            {
                "uri": "kubescape://findings/config-hygiene",
                "text": json.dumps(kubescape_data)
            }
        ]
    }
    
    findings = parse_mcp_resource_response(mcp_response)
    assert len(findings) == 1
    assert findings[0].resource_id == "apps/v1/default/Deployment/test"
    assert findings[0].control_id == "C-0001"
