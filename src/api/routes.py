from fastapi import APIRouter
from src.scanner import run_scan
from src.parser import parse_kubescape_results
from src.models import Finding
from uuid import uuid4
from datetime import datetime
from typing import List

router = APIRouter()

# In-memory storage for simplicity in this phase
findings_store: List[Finding] = []

@router.post("/scan")
def trigger_scan():
    global findings_store
    raw_results = run_scan()
    findings = parse_kubescape_results(raw_results)
    findings_store = findings
    
    return {
        "scan_id": uuid4(),
        "timestamp": datetime.now(),
        "findings": findings
    }

@router.get("/findings", response_model=List[Finding])
def get_findings():
    return findings_store