from unittest.mock import patch, MagicMock
from src.scanner import is_kubescape_installed, run_scan

@patch("subprocess.run")
def test_is_kubescape_installed_success(mock_run: MagicMock):
    mock_run.return_value = MagicMock(returncode=0)
    assert is_kubescape_installed() is True

@patch("subprocess.run")
def test_is_kubescape_installed_failure(mock_run: MagicMock):
    mock_run.side_effect = FileNotFoundError()
    assert is_kubescape_installed() is False

@patch("subprocess.run")
def test_run_scan_success(mock_run: MagicMock):
    mock_run.return_value = MagicMock(returncode=0, stdout=b'{"results": []}')
    result = run_scan()
    assert result == {"results": []}
    mock_run.assert_called_once_with(
        ["kubescape", "scan", "--format", "json"],
        capture_output=True,
        check=True
    )
