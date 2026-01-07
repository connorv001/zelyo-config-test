import pytest
from unittest.mock import patch, AsyncMock
from src.mcp_client import MCPClient
import httpx

@pytest.mark.asyncio
async def test_connect_retry_on_failure():
    url = "http://localhost:8000/sse"
    client = MCPClient(url)
    
    with patch("src.mcp_client.aconnect_sse") as mock_connect:
        # Fail twice, then succeed
        mock_connect.side_effect = [
            httpx.ConnectError("Failed"),
            httpx.ConnectError("Failed"),
            AsyncMock(__aenter__=AsyncMock(return_value=AsyncMock()))
        ]
        
        # We need to implement retry logic in the client
        await client.connect(retries=3)
        assert mock_connect.call_count == 3
