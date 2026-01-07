# Specification: Core Scanner Component

## 1. Overview
The Core Scanner Component is the foundation of the Zelyo Config Guardian. It is responsible for executing security and configuration scans against the local Kubernetes environment using Kubescape and making the results available to other internal components (like the Remediation Engine) via a lightweight API.

## 2. Goals
- Initialize the Python-based application structure.
- Integrate the Kubescape binary to perform scans.
- Parse Kubescape output into a structured format (Findings).
- Expose an internal API to trigger scans and retrieve results.

## 3. Architecture

### 3.1 Component Diagram
```mermaid
graph LR
    A[FastAPI Server] -- Spawns --> B[Kubescape Process]
    B -- JSON Output --> A
    A -- Stores/Caches --> C[Findings Store (In-Memory/Temp)]
    D[Remediation Engine] -- GET /scan --> A
```

### 3.2 Key Modules
- **`main.py`**: Entry point for the FastAPI application.
- **`scanner.py`**: Wrapper class for executing Kubescape commands.
- **`parser.py`**: Logic to transform raw Kubescape JSON into internal `Finding` models.
- **`models.py`**: Pydantic models defining the structure of a `Finding`.
- **`api/routes.py`**: FastAPI routes for `/scan` and `/findings`.

## 4. Data Models

### 4.1 Finding (Pydantic Model)
- `id`: Unique identifier (UUID).
- `resource_id`: K8s resource ID (e.g., `apps/v1/Deployment/my-app`).
- `severity`: Enum (Critical, High, Medium, Low).
- `control_id`: Kubescape control ID (e.g., `C-0001`).
- `description`: Human-readable description of the issue.
- `remediation`: Suggested fix (text).

## 5. API Endpoints

- **`POST /scan`**
    - Triggers an immediate scan.
    - Returns: `202 Accepted` (async) or scan summary.
- **`GET /findings`**
    - Returns list of current findings.
    - Filter parameters: `severity`, `namespace`.

## 6. Non-Functional Requirements
- **Performance**: Scans should complete within reasonable time limits (timeout handling).
- **Security**: The scanner runs with limited privileges (as defined in future RBAC tasks), but currently focuses on logic execution.
- **Error Handling**: Graceful handling of Kubescape failures or missing binaries.
