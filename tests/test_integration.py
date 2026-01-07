from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.scanner import is_kubescape_installed

client = TestClient(app)

@pytest.mark.skipif(not is_kubescape_installed(), reason="Kubescape not installed")
def test_full_scan_flow():
    # Trigger scan
    response = client.post("/scan")
    assert response.status_code == 200
    data = response.json()
    assert "findings" in data
    assert isinstance(data["findings"], list)
    
    # Check findings endpoint
    response = client.get("/findings")
    assert response.status_code == 200
    findings = response.json()
    assert len(findings) == len(data["findings"])
