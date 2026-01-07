import httpx
from httpx_sse import aconnect_sse
from typing import Optional, Any, Dict
from uuid import uuid4

class MCPClient:
    def __init__(self, url: str):
        self.url = url
        self.client = httpx.AsyncClient()
        self.sse_context = None
        self.post_url = url.replace("/sse", "/messages") if "/sse" in url else url + "/messages"

    async def connect(self) -> Any:
        self.sse_context = aconnect_sse(self.client, "GET", self.url)
        return await self.sse_context.__aenter__()
    
    async def close(self):
        if self.sse_context:
            await self.sse_context.__aexit__(None, None, None)
        await self.client.aclose()

    async def initialize(self):
        init_payload = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "zelyo-config-guardian",
                    "version": "0.1.0"
                }
            }
        }
        await self.client.post(self.post_url, json=init_payload)
        
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        await self.client.post(self.post_url, json=initialized_notification)

    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        await self.client.post(self.post_url, json=payload)
        # In a complete implementation, we would await the response matching this ID from the SSE stream.

    async def read_resource(self, uri: str):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        }
        await self.client.post(self.post_url, json=payload)