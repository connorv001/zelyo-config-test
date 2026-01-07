def test_pyproject_has_tool_config():
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    assert "[tool.pytest.ini_options]" in content
    assert "[tool.ruff]" in content
    assert "[tool.mypy]" in content