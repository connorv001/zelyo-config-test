from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from src.main import app
import pytest

client = TestClient(app)

def test_get_findings():
    response = client.get("/findings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_post_scan_async():
    with patch("src.api.routes.run_scan", new_callable=AsyncMock) as mock_run:
        with patch("src.api.routes.parse_mcp_resource_response") as mock_parse:
            # Mocking run_scan to return None or empty dict as it just triggers
            mock_run.return_value = {} 
            # We are switching to parse_mcp_resource_response? 
            # Wait, scanner.py run_scan now returns {} and calls MCP.
            # And we need to parse the MCP response.
            # But run_scan currently returns {}, so parse_kubescape_results would fail or return empty.
            
            # The refactor plan says: "Update POST /scan endpoint to utilize the asynchronous MCP stream."
            
            mock_parse.return_value = []
            
            response = client.post("/scan")
            assert response.status_code == 200
            assert "findings" in response.json()
