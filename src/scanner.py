import subprocess
import json
from typing import Any, Dict

def is_kubescape_installed() -> bool:
    try:
        subprocess.run(["kubescape", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_scan() -> Dict[str, Any]:
    result = subprocess.run(
        ["kubescape", "scan", "--format", "json"],
        capture_output=True,
        check=True
    )
    return json.loads(result.stdout)
