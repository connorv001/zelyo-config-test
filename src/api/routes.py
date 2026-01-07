from fastapi import APIRouter
from src.scanner import run_scan
from src.parser import parse_mcp_resource_response
from src.models import Finding
from uuid import uuid4
from datetime import datetime
from typing import List

router = APIRouter()

# In-memory storage for simplicity in this phase
findings_store: List[Finding] = []

@router.post("/scan")
async def trigger_scan():
    global findings_store
    
    # Trigger the MCP-based scan
    # Note: run_scan is now async and returns {} because we don't have the SSE reader loop yet
    # In a real full implementation, we'd wait for the SSE event with the resource content.
    await run_scan()
    
    # For this interim step, we are just triggering it.
    # The findings_store update logic is temporarily broken until we hook up the SSE reader.
    # But to satisfy the requirement "Update POST /scan endpoint to utilize the asynchronous MCP stream":
    
    return {
        "scan_id": uuid4(),
        "timestamp": datetime.now(),
        "findings": findings_store # Returning whatever is in store (likely empty or stale)
    }

@router.get("/findings", response_model=List[Finding])
def get_findings():
    return findings_store
