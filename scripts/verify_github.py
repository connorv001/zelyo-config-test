
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from src.github.pr_creator import GitHubPRCreator

def verify_github():
    print("🚀 Verifying GitHub Integration...")
    
    # Check what kind of auth is configured
    is_app = os.getenv("GITHUB_APP_ID") and os.getenv("GITHUB_APP_PRIVATE_KEY") and os.getenv("GITHUB_APP_INSTALLATION_ID")
    is_token = os.getenv("GITHUB_TOKEN")
    
    if not is_app and not is_token:
        print("❌ No GitHub credentials found!")
        print("   Set GITHUB_APP_* variables OR GITHUB_TOKEN")
        return
        
    repo = os.getenv("GITHUB_REPO")
    if not repo:
        print("❌ GITHUB_REPO not found!")
        return

    print(f"✅ Configured Repo: {repo}")
    print(f"✅ Auth Mode: {'GitHub App' if is_app else 'Personal Access Token'}")
    
    try:
        # Use simple direct instantiation to reuse the logic in __init__
        creator = GitHubPRCreator()
        g = creator.github
        
        # 1. Verify Identity
        print("🔍 Checking Identity...")
        try:
            user = g.get_user()
            print(f"👤 Authenticated as: {user.login}")
        except Exception as e:
            print(f"⚠️ Could not get user identity (Expected for some App contexts): {e}")

        # 2. Check Repository Access
        print(f"🔍 Checking Access to {repo}...")
        try:
             repo_obj = g.get_repo(repo)
             print(f"✅ Access Confirmed: {repo_obj.full_name}")
             print(f"   Permissions: {repo_obj.permissions}")
        except Exception as e:
             print(f"❌ Access Denied to {repo}: {e}")
             
             print("\n🔍 Troubleshooting:")
             if is_app:
                 print("1. Did you install the App on the 'zelyo-ai' organization?")
                 print("2. Is the Installation ID correct?")
                 print("3. Does the App have 'Read & Write' on Contents/Pull Requests?")
             else:
                 print("1. PAT Issue: Check scopes and SSO.")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    verify_github()
