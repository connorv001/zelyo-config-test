# Zelyo Config Test

This repository serves as a **GitOps configuration source of truth** for testing security scanning and patching workflows within the Zelyo ecosystem.

## Purpose

The primary goal of this repository is to provide a "live" test environment containing a simple application with intentional, known security vulnerabilities. These vulnerabilities are specifically designed to be **fixed only through image and package version updates**, rather than code changes.

This setup allows for the verification of:
1. **Security Scanning**: Testing tools like Kubescape, Trivy, or Grype against a running container and its manifests.
2. **GitOps Synchronization**: Validating that ArgoCD correctly deploys and maintains the state defined in this repository.
3. **Patching Workflows**: Demonstrating the transition from a vulnerable state to a patched state by simply updating the `Dockerfile` or `requirements.txt`.

## Project Components

### 1. Application (`app.py`)
A simple Python Flask "Hello World" application. While the code itself is minimal and secure, the environment it runs in is intentionally compromised via old dependencies.

### 2. Containerization (`Dockerfile`)
Uses a vulnerable base image (`python:3.11.14-slim`) and installs old, vulnerable versions of common packages.

### 3. GitOps Manifests (`argocd/`)
Contains the Kubernetes manifests and ArgoCD Application definition required to deploy the application into a `test-application` namespace.

## Deployment

The application is deployed via ArgoCD. The ArgoCD configuration points to this repository as the source.

### Manifests
- `argocd/deployment.yaml`: Defines the Kubernetes Deployment and Service.
- `argocd/application.yaml`: The ArgoCD Application manifest.

## Vulnerability Details

The current image contains vulnerabilities in the following components:
- **Base Image**: Python 3.11.14
- **Packages**:
    - `langchain-core==0.1.53` (Critical/High CVEs)
    - `langchain-community==0.0.38` (High CVEs)
    - `langchain-text-splitters==0.0.2` (High CVEs)

These vulnerabilities can be reproduced and scanned using any standard container security scanner.
