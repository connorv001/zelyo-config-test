from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

# Store received messages for verification
received_messages = []

@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        # Keep connection open
        while True:
            if await request.is_disconnected():
                break
            await asyncio.sleep(1)
            yield "data: {\"type\": \"keep-alive\"}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/messages")
async def messages_endpoint(request: Request):
    payload = await request.json()
    received_messages.append(payload)
    print(f"Server received: {payload}")
    return {"status": "ok"}

@app.get("/verify")
async def verify_endpoint():
    return received_messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8087)

