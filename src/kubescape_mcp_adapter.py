import asyncio
import json
import subprocess
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="Kubescape MCP Adapter")

@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        # Yield an initial event to establish connection
        yield {"event": "message", "data": json.dumps({"jsonrpc": "2.0", "method": "connection/ready"})}
        while True:
            if await request.is_disconnected():
                break
            await asyncio.sleep(1)
            # Keep alive
            yield {"event": "ping", "data": ""}

    return EventSourceResponse(event_generator())

@app.post("/messages")
async def handle_message(request: Request):
    payload = await request.json()
    method = payload.get("method")
    msg_id = payload.get("id")
    
    if method == "initialize":
        # In a real full-duplex SSE/MCP, we'd write the response to the SSE stream.
        # For this MVP/Half-duplex simulation where we might not have a clean way 
        # to inject into the specific SSE queue of the sender in this simple script without a manager,
        # we will just print/log. 
        # BUT, the client expects a response? The client 'initialize' doesn't wait for a response in our current impl.
        pass
    
    elif method == "resources/read":
        uri = payload.get("params", {}).get("uri")
        if uri == "kubescape://findings/config-hygiene":
            print("Running Kubescape scan...")
            # Run the real scan
            try:
                # We use specific flags to make it faster/relevant if needed, 
                # but default 'scan --format json' is what we want.
                # We target the current context.
                process = await asyncio.create_subprocess_exec(
                    "kubescape", "scan", "--format", "json",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    print(f"Scan failed: {stderr.decode()}")
                    return {"error": "Scan failed"}
                
                scan_data = stdout.decode()
                
                # In MCP, we would send a "notifications/resources/list_changed" or direct response.
                # Since our client just sends the request and doesn't explicitly wait for a *matching ID* response
                # in the current simple implementation (it relies on side-effects or just triggering),
                # we will simulate the "Action" of scanning.
                
                # HOWEVER, to make this "Real", we need to actually return the data to the client.
                # Our current `MCPClient.read_resource` sends a POST but doesn't return the data from that POST.
                # It expects the data to come back over SSE.
                
                # LIMITATION: To implement full SSE response routing in this single-file FastAPI script 
                # without a message queue is complex.
                
                # COMPROMISE for this session: 
                # We will return the data in the POST response (HTTP mode) OR 
                # we assume the client polls/gets it.
                
                # Let's verify what `src/mcp_client.py` does.
                # It creates a POST request and discards the result.
                
                # To make this work end-to-end, we need to update the CLIENT to either:
                # A) Read the HTTP response from the POST (Simplest, "HTTP Transport" style)
                # B) Listen to the SSE stream for the result (True MCP)
                
                # Given we want "Real stuff", let's make the Adapter return the data in the POST response for now,
                # and update the client to return it. This deviates slightly from pure SSE-only MCP but is valid HTTP transport.
                
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "contents": [{
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": scan_data
                        }]
                    }
                }
                
            except Exception as e:
                print(f"Error running kubescape: {e}")
                return {"error": str(e)}

    return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

if __name__ == "__main__":
    # Use port 8090 by default or allow config
    uvicorn.run(app, host="127.0.0.1", port=8090)
