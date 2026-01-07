import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.mcp_client import MCPClient

@pytest.mark.asyncio
async def test_read_resource():
    url = "http://localhost:8000/sse"
    client = MCPClient(url)
    
    mock_stream = AsyncMock()
    mock_stream.__aiter__.return_value = []
    
    client.client.post = AsyncMock()
    client.client.post.return_value = MagicMock(status_code=200)
    
    with patch("src.mcp_client.aconnect_sse") as mock_connect_sse:
        mock_connect_sse.return_value.__aenter__.return_value = mock_stream
        await client.connect()
        
        resource_uri = "kubescape://findings/config-hygiene"
        await client.read_resource(resource_uri)
        
        call_args = client.client.post.call_args[1]
        payload = call_args['json']
        assert payload['method'] == 'resources/read'
        assert payload['params']['uri'] == resource_uri
