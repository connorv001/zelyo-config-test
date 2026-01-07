import subprocess

def is_kubescape_installed() -> bool:
    try:
        subprocess.run(["kubescape", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
