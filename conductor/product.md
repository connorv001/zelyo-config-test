# Initial Concept
Zelyo Config Guardian deploys as a Kubernetes-native sidecar pod via Helm, scanning for config drifts and generating GitHub PRs without external dependencies. The vision delivers autonomous SRE capabilities, evolving from hygiene fixes to full runtime protection.

Product Vision
A zero-ops agent that proactively fixes Kubernetes drifts via mergeable PRs, saving teams 20+ hours weekly on audits. Starts narrow (config hygiene) for quick wins, expands to eBPF runtime remediation. Kubernetes-native means Helm-first, CRD integration, and sidecar patterns for seamless cluster embedding.
​

Core Components
Modular design runs in one pod for simplicity and portability.
​

Component	Purpose	Kubernetes Integration
Scanner Pod	Detects drifts (privileged pods, limits)	Kubescape MCP server via localhost SSE 
​
Remediation Engine	Triages (Tier 1 auto-fix) and PR logic	Internal FastAPI, RBAC-scoped API reads
GitHub Bridge	PR creation with diffs/explanations	Values.yaml token; rate-limited API calls
Safety Layer	Circuit breaker, dry-run mode	ConfigMap for thresholds; audit logs to CRDs