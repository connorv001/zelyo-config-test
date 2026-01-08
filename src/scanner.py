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
    # Configurable URL
    import os
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8090/sse")
    
    client = MCPClient(mcp_url)
    try:
        # We start the connection (handshake)
        await client.connect()
        await client.initialize()
        
        # We request the resource and get the data back (via HTTP response in this adapter impl)
        response = await client.read_resource("kubescape://findings/config-hygiene")
        
        # Close connection

        
        if response and "result" in response and "contents" in response["result"]:
            contents = response["result"]["contents"]
            if contents and len(contents) > 0:
                text_data = contents[0].get("text", "{}")
                return json.loads(text_data)
                
        return {}
    except Exception as e:
        import traceback
        print(f"Scanner error: {e}")
        traceback.print_exc()
        return {}
    finally:
        await client.close()
