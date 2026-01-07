# Plan: Core Scanner Component

## Phase 1: Project Skeleton & Configuration
- [x] Task: Initialize Python project with `poetry`, creating `pyproject.toml` and lock file. [37d1174]
- [x] Task: Set up `src/` directory structure and create a basic `main.py` with a "Hello World" FastAPI endpoint to verify setup. [98a65f6]
- [x] Task: Create `Dockerfile` optimized for Python 3.11+ and install Kubescape binary within the image. [6189077]
- [x] Task: Configure `pytest` and code quality tools (ruff/mypy) in `pyproject.toml`. [937a72d]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Project Skeleton & Configuration' (Protocol in workflow.md) [checkpoint: d8dd274]

## Phase 2: Domain Models & Kubescape Integration
- [x] Task: Define Pydantic models in `src/models.py` for `Finding` and `ScanResult` based on the spec. [ad40344]
- [x] Task: Create `src/scanner.py` and implement a function to check if Kubescape is installed/executable. [6413934]
- [x] Task: Implement `run_scan()` method in `src/scanner.py` using `subprocess` to execute `kubescape scan --format json ...`. [022ed9b]
- [x] Task: Create `src/parser.py` to parse raw Kubescape JSON output into list of `Finding` objects. [eb06384]
- [x] Task: Conductor - User Manual Verification 'Phase 2: Domain Models & Kubescape Integration' (Protocol in workflow.md) [checkpoint: 3e66fee]

## Phase 3: API Implementation
- [x] Task: Implement `POST /scan` endpoint in `src/api/routes.py` to trigger the scanner logic. [a625b1c]
- [ ] Task: Implement `GET /findings` endpoint to return parsed results (mocked persistence or in-memory list for now).
- [ ] Task: Integrate API routes into `main.py`.
- [ ] Task: Write integration tests for the full flow (API -> Scanner -> Parser).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: API Implementation' (Protocol in workflow.md)
