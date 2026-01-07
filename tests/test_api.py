from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@patch("src.api.routes.run_scan")
@patch("src.api.routes.parse_kubescape_results")
def test_post_scan(mock_parse, mock_run):
    mock_run.return_value = {"raw": "data"}
    mock_parse.return_value = []
    
    response = client.post("/scan")
    assert response.status_code == 200
    assert "findings" in response.json()