from unittest.mock import patch, MagicMock
from src.scanner import is_kubescape_installed

@patch("subprocess.run")
def test_is_kubescape_installed_success(mock_run: MagicMock):
    mock_run.return_value = MagicMock(returncode=0)
    assert is_kubescape_installed() is True

@patch("subprocess.run")
def test_is_kubescape_installed_failure(mock_run: MagicMock):
    mock_run.side_effect = FileNotFoundError()
    assert is_kubescape_installed() is False
