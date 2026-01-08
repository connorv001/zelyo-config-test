import asyncio
import httpx
import time
import subprocess
import os
import json
from datetime import datetime
from collections import defaultdict

# Configuration
MCP_PORT = 8090
API_PORT = 8086
REPORT_FILE = "TEST_REPORT.md"

# Kubescape control categorization based on Zelyo vision
# Categories: Configuration, Security, Real-Time Monitoring
SECURITY_CONTROLS = [
    "C-0001", "C-0002", "C-0007", "C-0012", "C-0015", "C-0016", "C-0017", 
    "C-0020", "C-0021", "C-0026", "C-0031", "C-0034", "C-0035", "C-0036", 
    "C-0037", "C-0038", "C-0039", "C-0041", "C-0042", "C-0044", "C-0045",
    "C-0046", "C-0048", "C-0053", "C-0054", "C-0055", "C-0056", "C-0057",
    "C-0058", "C-0059", "C-0060", "C-0061", "C-0062", "C-0063", "C-0065",
    "C-0066", "C-0067", "C-0068", "C-0069", "C-0070", "C-0188", "C-0256",
]

CONFIG_CONTROLS = [
    "C-0004", "C-0006", "C-0009", "C-0013", "C-0014", "C-0018", "C-0030",
    "C-0050", "C-0055", "C-0074", "C-0076", "C-0077", "C-0078", "C-0079",
    "C-0081", "C-0086", "C-0087", "C-0088", "C-0089", "C-0090", "C-0092",
]

def categorize_finding(control_id):
    if control_id in SECURITY_CONTROLS:
        return "Security"
    elif control_id in CONFIG_CONTROLS:
        return "Configuration"
    else:
        return "Other"

def generate_markdown_report(success, duration, response_data, error=None):
    timestamp = datetime.now().isoformat()
    
    report = f"""# Zelyo Config Guardian - Test Verification Report

> **Vision:** Kubernetes Cluster monitoring for Configuration, Security, and Real-Time anomaly detection with autonomous GitOps remediation (Human-in-the-Loop).

---

**Date:** {timestamp}  
**Status:** {'✅ PASSED' if success else '❌ FAILED'}  
**Duration:** {duration:.2f} seconds

---

## Executive Summary

Zelyo Config Guardian acts as a 24/7 automated SRE robot:
1. 👁️ **Eyes Open:** Continuously scans for Configuration & Security issues
2. 🤖 **Hands Ready:** Suggests fixes via GitOps Pull Requests
3. 👨‍💻 **Human Approval:** All fixes require Senior Engineer validation

---

"""
    if success:
        findings = response_data.get("findings", [])
        scan_id = response_data.get("scan_id")
        
        # Categorize findings
        categorized = defaultdict(list)
        for finding in findings:
            category = categorize_finding(finding.get("control_id", ""))
            categorized[category].append(finding)
        
        report += f"""## Scan Results

| Metric | Value |
|--------|-------|
| **Scan ID** | `{scan_id}` |
| **Total Findings** | {len(findings)} |
| **Security Issues** | {len(categorized['Security'])} |
| **Configuration Issues** | {len(categorized['Configuration'])} |
| **Other Issues** | {len(categorized['Other'])} |

---

## 🔒 Security Findings ({len(categorized['Security'])})

These findings relate to potential security vulnerabilities that could be exploited by attackers (privilege escalation, exposed secrets, excessive permissions, etc.)

| # | Control ID | Description | Resource | Remediation Action |
|---|------------|-------------|----------|-------------------|
"""
        for i, finding in enumerate(categorized['Security'], 1):
            desc = finding.get('description', 'N/A')[:50]
            resource = finding.get('resource_id', 'N/A')
            if len(resource) > 60:
                resource = resource[:57] + "..."
            control = finding.get('control_id', 'N/A')
            remediation = finding.get('remediation', 'N/A')[:40]
            report += f"| {i} | `{control}` | {desc} | `{resource}` | {remediation}... |\n"

        report += f"""
---

## ⚙️ Configuration Findings ({len(categorized['Configuration'])})

These findings relate to misconfigurations that could lead to operational issues, resource waste, or degraded performance.

| # | Control ID | Description | Resource | Remediation Action |
|---|------------|-------------|----------|-------------------|
"""
        for i, finding in enumerate(categorized['Configuration'], 1):
            desc = finding.get('description', 'N/A')[:50]
            resource = finding.get('resource_id', 'N/A')
            if len(resource) > 60:
                resource = resource[:57] + "..."
            control = finding.get('control_id', 'N/A')
            remediation = finding.get('remediation', 'N/A')[:40]
            report += f"| {i} | `{control}` | {desc} | `{resource}` | {remediation}... |\n"

        if categorized['Other']:
            report += f"""
---

## 📋 Other Findings ({len(categorized['Other'])})

Findings that don't fit strictly into Security or Configuration categories.

| # | Control ID | Description | Resource |
|---|------------|-------------|----------|
"""
            for i, finding in enumerate(categorized['Other'], 1):
                desc = finding.get('description', 'N/A')[:50]
                resource = finding.get('resource_id', 'N/A')
                if len(resource) > 60:
                    resource = resource[:57] + "..."
                control = finding.get('control_id', 'N/A')
                report += f"| {i} | `{control}` | {desc} | `{resource}` |\n"

        report += f"""
---

## 🚀 Next Steps (GitOps Integration)

For each finding above, Zelyo will:
1. **Analyze** the issue and determine if an automated fix is possible
2. **Generate** a remediation manifest or configuration change
3. **Create PR** in the GitOps repository with the proposed fix
4. **Await Approval** from a Senior Engineer (Human-in-the-Loop)
5. **Apply** the fix upon approval via ArgoCD/Flux

---

## 📊 Real-Time Monitoring (Future)

| Feature | Status |
|---------|--------|
| Request spike detection | 🔜 Planned |
| Privilege escalation monitoring | 🔜 Planned |
| Excessive syscall detection | 🔜 Planned |
| Bandwidth/Disk I/O anomalies | 🔜 Planned |
| CPU/Memory spike detection | 🔜 Planned |

---

*Report generated by Zelyo Config Guardian v0.1.0*
"""
    else:
        report += f"""## Error

```
{error}
```
"""

    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"Report generated at {REPORT_FILE}")

async def run_test():
    print("Starting services...")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    mcp_proc = subprocess.Popen(
        ["poetry", "run", "uvicorn", "src.kubescape_mcp_adapter:app", "--host", "127.0.0.1", "--port", str(MCP_PORT)],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    api_proc = subprocess.Popen(
        ["poetry", "run", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", str(API_PORT)],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    try:
        print("Waiting for services to be ready...")
        await asyncio.sleep(5)
        
        print("Triggering scan...")
        start_time = time.time()
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"http://127.0.0.1:{API_PORT}/scan")
            
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"Scan successful! Findings: {len(data.get('findings', []))}")
            generate_markdown_report(True, duration, data)
        else:
            print(f"Scan failed with status {response.status_code}")
            generate_markdown_report(False, duration, {}, error=f"Status: {response.status_code}\nBody: {response.text}")
            
    except Exception as e:
        print(f"Test exception: {e}")
        generate_markdown_report(False, 0, {}, error=str(e))
        
    finally:
        print("Cleaning up processes...")
        mcp_proc.terminate()
        api_proc.terminate()
        mcp_proc.wait()
        api_proc.wait()

if __name__ == "__main__":
    asyncio.run(run_test())
