import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.scanner import is_kubescape_installed, run_scan

@patch("subprocess.run")
def test_is_kubescape_installed_success(mock_run: MagicMock):
    mock_run.return_value = MagicMock(returncode=0)
    assert is_kubescape_installed() is True

@patch("subprocess.run")
def test_is_kubescape_installed_failure(mock_run: MagicMock):
    mock_run.side_effect = FileNotFoundError()
    assert is_kubescape_installed() is False

@pytest.mark.asyncio
async def test_run_scan_success():
    with patch("src.scanner.MCPClient") as MockMCPClient:
        mock_client = MockMCPClient.return_value
        mock_client.connect = AsyncMock()
        mock_client.initialize = AsyncMock()
        mock_client.read_resource = AsyncMock()
        mock_client.close = AsyncMock()
        
        # We'll assume for this MVP refactor that run_scan triggers the request
        # Since we don't have the full SSE reader loop returning data yet,
        # we can't easily return *real* data from this function without blocking.
        # So we might return a placeholder or empty dict for now, 
        # relying on the side effects (calling MCP).
        
        result = await run_scan()
        
        # Verify orchestration
        mock_client.connect.assert_called_once()
        mock_client.initialize.assert_called_once()
        mock_client.read_resource.assert_called_with("kubescape://findings/config-hygiene")
        mock_client.close.assert_called_once()
        
        # For now, it might return empty until we hook up the reader
        assert result == {}