from fastapi import APIRouter
from src.scanner import run_scan
from src.parser import parse_kubescape_results
from src.models import ScanResult
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post("/scan")
def trigger_scan():
    raw_results = run_scan()
    findings = parse_kubescape_results(raw_results)
    
    return {
        "scan_id": uuid4(),
        "timestamp": datetime.now(),
        "findings": findings
    }
