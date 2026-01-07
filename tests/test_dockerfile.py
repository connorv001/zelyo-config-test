import os

def test_dockerfile_exists():
    assert os.path.exists("Dockerfile")

def test_dockerfile_installs_kubescape():
    with open("Dockerfile", "r") as f:
        content = f.read()
    assert "kubescape" in content
    assert "python:3.11" in content or "python:3.12" in content
