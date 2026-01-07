# Zelyo Config Guardian

Zelyo Config Guardian is a Kubernetes-native agent designed to detect and proactively fix configuration drifts. It operates as a zero-ops SRE capability, evolving from configuration hygiene to full runtime protection.

## 🚀 Vision
A zero-ops agent that proactively fixes Kubernetes drifts via mergeable PRs, saving teams hours on audits. Built to be Kubernetes-native, starting with Helm-first deployment and transitioning to MCP-based real-time scanning.

## ✨ Core Features
- **Config Hygiene Scanner:** Automatically detects security and configuration issues (e.g., privileged containers, missing limits, non-root enforcement).
- **MCP Integration:** Uses the Model Context Protocol (MCP) to integrate with Kubescape MCP servers over SSE for real-time finding ingestion.
- **Internal API:** Exposes FastAPI endpoints for triggering scans and retrieving structured findings.
- **Dockerized:** Ready for Kubernetes deployment as a sidecar or standalone pod.

## 🛠 Tech Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Scanning:** Kubescape (Binary + MCP Server)
- **Networking:** HTTPX (with SSE support)
- **Validation:** Pydantic v2
- **Testing:** Pytest with coverage and async support

## 📥 Installation

### Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/)
- [Kubescape](https://kubescape.io/) installed locally (for binary mode)

### Setup
```bash
poetry install
```

## 🏃 Usage

### Running the API
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8086
```

### API Endpoints
- **GET `/`**: Redirects to Redoc documentation.
- **POST `/scan`**: Triggers a new configuration scan.
- **GET `/findings`**: Returns the latest list of findings.
- **GET `/redoc`**: Interactive API documentation.

## 🧪 Testing & Quality
We maintain 100% code coverage.

### Run Tests
```bash
poetry run pytest
```

### Run Coverage Report
```bash
poetry run pytest --cov=src --cov-report=term-missing
```

## 🏗 Project Structure
- `src/`: Application source code.
  - `api/`: FastAPI route definitions.
  - `models.py`: Domain Pydantic models.
  - `scanner.py`: Logic for executing Kubescape scans.
  - `parser.py`: Logic for parsing raw scanner output.
  - `mcp_client.py`: SSE client for MCP integration.
- `tests/`: Comprehensive test suite (Unit + Integration).
- `conductor/`: Project management and track tracking (using Conductor methodology).

## 📄 License
Internal use only.