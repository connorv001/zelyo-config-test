![Zelyo Security Test Banner](https://raw.githubusercontent.com/connorv001/zelyo-config-test/main/assets/banner.png)

# Zelyo Config Test

This repository serves as a **GitOps configuration source of truth** for testing security scanning and patching workflows within the Zelyo ecosystem.

> [!IMPORTANT]
> **Primary Purpose**: This repository is specifically designed for **TESTING THE ZELYO AGENT** that we are deploying. It facilitates the validation of agent capabilities in identifying and responding to common vulnerability packages.

## Overview

The primary goal of this repository is to provide a "live" test environment containing a simple application with intentional, known security vulnerabilities. It serves as a benchmark for **common vulnerability packages** and base images.

> [!TIP]
> **Docker Hub Image**: The latest vulnerable image is available at:
> `shubhamverlekar/zelyo-config-test:latest`

## Why This Exists

This setup allows for the verification of:
1. **Zelyo Agent Validation**: Specifically testing the Zelyo Agent's ability to detect and report vulnerabilities in real-time.
2. **Security Scanning**: Testing tools like Kubescape, Trivy, or Grype against a running container and its manifests.
3. **GitOps Synchronization**: Validating that ArgoCD correctly deploys and maintains the state defined in this repository.
4. **Patching Workflows**: Demonstrating the transition from a vulnerable state to a patched state by simply updating the `Dockerfile` or `requirements.txt`.

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

These vulnerabilities can be reproduced and scanned using any standard container security scanner as part of the Zelyo Agent testing suite.
