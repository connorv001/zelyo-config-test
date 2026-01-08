
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm.provider import LLMClient
from src.remediation.engine import RemediationEngine
from dotenv import load_dotenv

load_dotenv()

async def verify_llm():
    print("🚀 Verifying LLM Integration...")
    
    # Check Environment
    provider = os.getenv("LLM_PROVIDER", "unknown")
    print(f"✅ Provider: {provider}")
    
    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            print("❌ GEMINI_API_KEY not found!")
            return
        print("✅ GEMINI_API_KEY found")
    elif provider == "openai":
         key = os.getenv("OPENAI_API_KEY")
         if not key:
            print("❌ OPENAI_API_KEY not found!")
            return
         print("✅ OPENAI_API_KEY found")
            
    # Test Connection
    print("\n📡 Testing Connection...")
    client = LLMClient()
    try:
        response = await client.invoke(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Connection Successful' and nothing else."
        )
        print(f"🤖 Response: {response}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # Test Remediation Engine
    print("\n🛠 Testing Remediation Engine...")
    engine = RemediationEngine()
    
    mock_finding = {
        "id": "test-finding-1",
        "control_id": "C-0013",
        "description": "Non-root containers",
        "resource_id": "apps/v1/default/Deployment/nginx",
        "severity": "Medium",
        "remediation": "Set securityContext.runAsNonRoot to true"
    }
    
    try:
        result = await engine.analyze_finding(mock_finding)
        print("✅ Analysis Successful!")
        print(f"📋 Strategy: {result.remediation.strategy}")
        print(f"🔧 YAML Patch: \n{result.remediation.yaml_patch}")
    except Exception as e:
        print(f"❌ Remediation Analysis Failed: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_llm())
