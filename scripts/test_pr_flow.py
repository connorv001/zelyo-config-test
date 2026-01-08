import sys
import os
import asyncio
sys.path.append(os.getcwd())
from src.remediation.engine import RemediationEngine
from src.github.pr_creator import GitHubPRCreator

async def test_flow():
    print("🚀 Starting End-to-End Remediation Test...")
    
    # 1. Define a Mock Finding (simulating what Kubescape returns)
    # Based on a common failure: running as root allowed
    mock_finding = {
        "id": "test-finding-123",
        "control_id": "C-0013",
        "description": "Container 'zelyo-api' in 'Deployment/zelyo-guardian' is allowed to run as root.",
        "resource_id": "zelyo/Deployment/zelyo-guardian",
        "severity": "High",
        "remediation": "Set 'securityContext.runAsNonRoot' to true.",
        "file_path": "k8s/deployment.yaml" # Hinting the file path
    }
    
    print(f"📝 Analyzing Finding (Real LLM): {mock_finding['control_id']}")
    
    # 2. Run Remediation Engine (LLM)
    engine = RemediationEngine()
    result = await engine.analyze_finding(mock_finding)
    
    # Debug info
    print(f"✅ Remediation Generated:")
    print(f"   Analysis: {result.analysis}")
    print(f"   Strategy: {result.remediation.strategy}")
    print(f"   Target File: {result.remediation.target_file}")
    
    if not result.remediation.yaml_patch:
        print("❌ No YAML patch generated. Aborting.")
        return

    # 3. Create PR
    print(f"gh_repo: {os.getenv('GITHUB_REPO')}")
    print(f"gh_app_id: {os.getenv('GITHUB_APP_ID')}")
    print("📤 Creating Pull Request...")
    
    try:
        pr_creator = GitHubPRCreator()
        pr_url = pr_creator.create_remediation_pr(
            control_id=result.control_id,
            description=mock_finding["description"],
            resource_id=mock_finding["resource_id"],
            severity=result.analysis.severity,
            yaml_patch=result.remediation.yaml_patch,
            fix_strategy=result.remediation.strategy,
            risk_summary=result.analysis.risk_summary,
            file_path=result.remediation.target_file
        )
        print(f"🎉 PR Created Successfully!")
        print(f"🔗 URL: {pr_url['pr_url']}")
    except Exception as e:
        print(f"❌ PR Creation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    print(f"Loaded .env")
    asyncio.run(test_flow())
