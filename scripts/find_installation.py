
import jwt
import time
import sys
import httpx

APP_ID = "2599012"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA34cRIL54a1uYyY/pP+m6hE+wB58aR7r3s0yE2R/06oIeCquK
mI35nLg5Z8nLw1aU7o8yvC... (truncated for brevity in script log, but will use full key in real execution)
"""

# I need to use the full private key from the previous step output
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA34cRIL54a1uYyY/pP+m6hE+wB58aR7r3s0yE2R/06oIeCquK
mI35nLg5Z8nLw1aU7o8yvCP9zRzVvF0d3eA4bM/1jX6lKqW8nO9sT0vU2+3r4pYs
9o2lQ5zJ8xW9v0uL1aN3oP4rS5qT6vU7+1sX8yZ9wB0cE1dF2gH3iJ4kLmLvnO8u
P7qR9sT2wU4vV3xYZD6eC1fH2gI5jKcLmnO9uP8qS6rT7vV8+2tY9zJ0dE2fH3gI
... (I will actually read it from the file in the script to avoid copy-paste errors)
"""

def get_jwt(app_id, pem_file_path):
    with open(pem_file_path, 'r') as f:
        private_key = f.read()
    
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + 600,
        'iss': app_id
    }
    encoded = jwt.encode(payload, private_key, algorithm='RS256')
    return encoded

def find_installations():
    pem_path = "/root/projects/zelyo-ops2/zelyo-security-guardian.2026-01-08.private-key.pem"
    app_id = "2599012"
    
    try:
        token = get_jwt(app_id, pem_path)
    except Exception as e:
        print(f"Error creating JWT: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"🔍 Listing Installations for App ID {app_id}...")
    try:
        response = httpx.get("https://api.github.com/app/installations", headers=headers)
        if response.status_code == 200:
            installations = response.json()
            if not installations:
                print("❌ No installations found! You must install the App on your Organization.")
                return
                
            for inst in installations:
                print(f"✅ Found Installation:")
                print(f"   Account: {inst['account']['login']} ({inst['account']['type']})")
                print(f"   ID: {inst['id']}")
                print(f"   Repository Selection: {inst['repository_selection']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Request Failed: {e}")

if __name__ == "__main__":
    find_installations()
