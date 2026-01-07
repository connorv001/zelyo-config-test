from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNKNOWN = "Unknown"

class Finding(BaseModel):
    id: UUID
    resource_id: str
    severity: Severity
    control_id: str
    description: str
    remediation: Optional[str] = None

class ScanResult(BaseModel):
    scan_id: UUID
    timestamp: datetime
    findings: List[Finding]
