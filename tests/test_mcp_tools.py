import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from src.mcp_client import MCPClient

@pytest.mark.asyncio
async def test_call_tool():
    url = "http://localhost:8000/sse"
    client = MCPClient(url)
    
    mock_stream = AsyncMock()
    mock_stream.__aiter__.return_value = []
    
    client.client.post = AsyncMock()
    # Mocking the response of the tool call
    client.client.post.return_value = MagicMock(status_code=200)
    # The actual result reading would happen in the read loop, but for sending:
    
    with patch("src.mcp_client.connect_sse") as mock_connect_sse:
        mock_connect_sse.return_value.__aenter__.return_value = mock_stream
        await client.connect()
        
        await client.call_tool("kubescape-scan", {"format": "json"})
        
        call_args = client.client.post.call_args[1]
        payload = call_args['json']
        assert payload['method'] == 'tools/call'
        assert payload['params']['name'] == 'kubescape-scan'
        assert payload['params']['arguments']['format'] == 'json'
