import subprocess
import json
from typing import Any, Dict
from src.mcp_client import MCPClient

def is_kubescape_installed() -> bool:
    try:
        subprocess.run(["kubescape", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

async def run_scan() -> Dict[str, Any]:
    # Placeholder URL - in a real app this comes from config
    client = MCPClient("http://localhost:8000/sse")
    await client.connect()
    await client.initialize()
    await client.read_resource("kubescape://findings/config-hygiene")
    await client.close()
    
    # Returning empty for now as we don't have the reader loop hooked up to capture the result
    return {}
