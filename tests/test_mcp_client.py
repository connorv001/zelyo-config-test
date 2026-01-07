import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.mcp_client import MCPClient

@pytest.mark.asyncio
async def test_sse_connection_success():
    url = "http://localhost:8000/sse"
    
    with patch("src.mcp_client.aconnect_sse") as mock_connect_sse:
        mock_context = AsyncMock()
        mock_connect_sse.return_value = mock_context
        mock_context.__aenter__.return_value = MagicMock()
        
        client = MCPClient(url)
        await client.connect()
        
        mock_connect_sse.assert_called_with(client.client, "GET", url)
        await client.close()

@pytest.mark.asyncio
async def test_sse_connection_failure():
    url = "http://localhost:8000/sse"
    
    with patch("src.mcp_client.aconnect_sse") as mock_connect_sse:
        mock_context = AsyncMock()
        mock_connect_sse.return_value = mock_context
        mock_context.__aenter__.side_effect = Exception("Connection failed")
        
        client = MCPClient(url)
        with pytest.raises(Exception):
            await client.connect()
        
        await client.close()