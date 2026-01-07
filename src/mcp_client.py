import httpx
from httpx_sse import connect_sse
from typing import Optional, Any

class MCPClient:
    def __init__(self, url: str):
        self.url = url
        self.client = httpx.AsyncClient()
        self.sse_context = None

    async def connect(self) -> Any:
        # In a real application, this context manager needs to be handled carefully
        # to keep the connection open. For this MVP step, we are just establishing it.
        # We'll likely need to refactor this to be an async context manager itself.
        self.sse_context = connect_sse(self.client, "GET", self.url)
        return await self.sse_context.__aenter__()
    
    async def close(self):
        if self.sse_context:
            await self.sse_context.__aexit__(None, None, None)
        await self.client.aclose()