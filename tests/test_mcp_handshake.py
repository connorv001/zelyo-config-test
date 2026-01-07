import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from src.mcp_client import MCPClient

@pytest.mark.asyncio
async def test_initialize_handshake():
    url = "http://localhost:8000/sse"
    client = MCPClient(url)
    
    mock_stream = AsyncMock()
    mock_stream.__aiter__.return_value = [] 
    
    client.client.post = AsyncMock()
    client.client.post.return_value = MagicMock(status_code=200)

    with patch("src.mcp_client.aconnect_sse") as mock_connect_sse:
        mock_connect_sse.return_value.__aenter__.return_value = mock_stream
        
        await client.connect()
        await client.initialize()
        
        # Verify calls
        assert client.client.post.call_count >= 2
        
        # Verify first call (Initialize Request)
        first_call = client.client.post.call_args_list[0]
        payload = first_call[1]['json']
        assert payload['method'] == 'initialize'
        assert payload['params']['protocolVersion'] == '2024-11-05'
        
        # Verify second call (Initialized Notification)
        second_call = client.client.post.call_args_list[1]
        payload_notif = second_call[1]['json']
        assert payload_notif['method'] == 'notifications/initialized'