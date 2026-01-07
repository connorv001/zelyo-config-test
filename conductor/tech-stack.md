# Technology Stack - Zelyo Config Guardian

## Core Languages & Frameworks
- **Primary Language:** Python 3.11+
- **Backend Framework:** FastAPI (Used for the Remediation Engine and internal component communication)
- **Async Logic:** `httpx` for asynchronous API calls to GitHub and Kubernetes.

## Kubernetes Integration
- **Scanner:** Kubescape (Integrated via MCP server over localhost SSE)
- **Deployment:** Helm v3 (Kubernetes-native sidecar pattern)
- **API Communication:** `kubernetes-python` (Official K8s client)
- **State Management:** Kubernetes Custom Resource Definitions (CRDs) for audit logs and status; ConfigMaps for thresholds and rules.

## GitOps & Remediation
- **GitHub API:** REST API v3 via `httpx`.
- **Authentication:** Personal Access Token (PAT) (Passed securely via Helm secrets/values).
- **Future Roadmap:** Support for GitHub Apps for enhanced security and scoped permissions.

## Security & Safety
- **RBAC:** Scoped ServiceAccount permissions for reading cluster state and writing to specific CRDs.
- **Circuit Breakers:** Custom Python logic within the Remediation Engine to monitor PR frequency and error rates.
- **Containerization:** Docker (Multi-stage builds for small, secure images).

## Monitoring & Logging
- **Logging:** Structured JSON logging (Standard Library) for easy parsing by external log aggregators.
- **Observability:** Prometheus metrics (via FastAPI instrumentation) for tracking scan counts and PR success rates.