
import httpx
import sys

API_URL = "http://localhost:8086"

def verify_api():
    print("🚀 Verifying API Endpoints...")
    
    # 1. Check Findings
    try:
        response = httpx.get(f"{API_URL}/findings")
        if response.status_code == 200:
            findings = response.json()
            print(f"✅ GET /findings: Success ({len(findings)} findings)")
        else:
            print(f"❌ GET /findings: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ GET /findings: Connection Error ({e})")

    # 2. Check Config
    try:
        response = httpx.get(f"{API_URL}/config")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ GET /config: Success")
            print(f"   LLM Configured: {config.get('llm_configured')}")
            print(f"   GitHub Configured: {config.get('github_configured')}")
        else:
            print(f"❌ GET /config: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ GET /config: Connection Error ({e})")

if __name__ == "__main__":
    verify_api()
