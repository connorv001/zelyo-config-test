# Zelyo Config Guardian - Vision Alignment Test Report

> **Vision:** Kubernetes monitoring for **Configuration**, **Security**, and **Real-Time anomalies**
> with autonomous **GitOps remediation** (Human-in-the-Loop).

---

## Test Execution Summary

| Metric | Value |
|--------|-------|
| **Date** | 2026-01-08T08:49:45.278782 |
| **Scan ID** | `152251a8-cd12-4be8-a5d0-1c940c9ee726` |
| **Duration** | 15.17s |
| **Total Findings** | 251 |

---

## Vision Pillar Validation

| Pillar | Status | Count | Description |
|--------|--------|-------|-------------|
| 🔒 **Security** | ✅ Active | 173 | Privilege escalation, secrets, RBAC, host access |
| 🔧 **Configuration** | ✅ Active | 75 | Resource limits, network policies, non-root |
| 📊 **Real-Time** | 🔜 Planned | - | Anomaly detection (DDOS, syscalls, spikes) |
| 🔄 **GitOps** | ✅ Ready | All | Human-in-the-Loop PR workflow |

---

## 🔒 Security Findings (173)

*Detects: Privilege escalation, exposed secrets, excessive RBAC, host access, service account misuse*

| # | Control | Description | Resource |
|---|---------|-------------|----------|
| 1 | `C-0057` | Privileged container | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 2 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 3 | `C-0046` | Insecure capabilities | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 4 | `C-0048` | HostPath mount | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 5 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 6 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 7 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 8 | `C-0045` | Writable hostPath mount | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 9 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/hubble-ui/rbac.authorization.k8s` |
| 10 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/dosecret-operator` |
| 11 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-dex-server` |
| 12 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/service-cidrs-controller` |
| 13 | `C-0034` | Automatic mapping of service account | `apps/v1/default/StatefulSet/zelyo-agent` |
| 14 | `C-0016` | Allow privilege escalation | `apps/v1/default/StatefulSet/zelyo-agent` |
| 15 | `C-0017` | Immutable container filesystem | `apps/v1/default/StatefulSet/zelyo-agent` |
| 16 | `C-0055` | Linux hardening | `apps/v1/default/StatefulSet/zelyo-agent` |
| 17 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-server` |
| 18 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/hubble-ui` |
| 19 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/snapshot-controller/rbac.authori` |
| 20 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 21 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 22 | `C-0034` | Automatic mapping of service account | `/v1/zelyo-test/ServiceAccount/default` |
| 23 | `C-0036` | Validate admission controller (validating) | `admissionregistration.k8s.io/v1//ValidatingWebhookConfigurat` |
| 24 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 25 | `C-0048` | HostPath mount | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 26 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 27 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 28 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 29 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/doks-fluentbit/rbac.authorizatio` |
| 30 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/validatingadmissionpolicy-sta` |
| 31 | `C-0054` | Cluster internal networking | `/v1//Namespace/test-application` |
| 32 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cluster-autoscaler/rbac.authoriz` |
| 33 | `C-0007` | Roles with delete capabilities | `/kubescape/ServiceAccount/node-agent/rbac.authorization.k8s.` |
| 34 | `C-0054` | Cluster internal networking | `/v1//Namespace/test-app` |
| 35 | `C-0034` | Automatic mapping of service account | `/v1/test-app/ServiceAccount/default` |
| 36 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-application-controller` |
| 37 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/Deployment/hubble-relay` |
| 38 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/cluster-autoscaler` |
| 39 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/Deployment/headlamp` |
| 40 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/Deployment/headlamp` |
| 41 | `C-0055` | Linux hardening | `apps/v1/kube-system/Deployment/headlamp` |
| 42 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/cilium-operator` |
| 43 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/leader-election-controller/rbac.` |
| 44 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/csi-do-controller-sa` |
| 45 | `C-0188` | Minimize access to create pods | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 46 | `C-0007` | Roles with delete capabilities | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 47 | `C-0002` | Prevent containers from allowing command execution | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 48 | `C-0037` | CoreDNS poisoning | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 49 | `C-0063` | Portforwarding privileges | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 50 | `C-0031` | Delete Kubernetes events | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 51 | `C-0015` | List Kubernetes secrets | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 52 | `C-0035` | Administrative Roles | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 53 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/volumeattributesclass-protect` |
| 54 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/doks-fluentbit` |
| 55 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cloud-controller-manager/rbac.au` |
| 56 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/csi-do-controller-sa/rbac.author` |
| 57 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/do-agent` |
| 58 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 59 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 60 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 61 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 62 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/snapshot-controller` |
| 63 | `C-0036` | Validate admission controller (validating) | `admissionregistration.k8s.io/v1//ValidatingWebhookConfigurat` |
| 64 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/csi-do-controller-sa/rbac.author` |
| 65 | `C-0054` | Cluster internal networking | `/v1//Namespace/zelyo-test` |
| 66 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-redis` |
| 67 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-notifications-controller` |
| 68 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/cloud-controller-manager` |
| 69 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 70 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 71 | `C-0057` | Privileged container | `apps/v1/kube-system/DaemonSet/cilium` |
| 72 | `C-0044` | Container hostPort | `apps/v1/kube-system/DaemonSet/cilium` |
| 73 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/cilium` |
| 74 | `C-0046` | Insecure capabilities | `apps/v1/kube-system/DaemonSet/cilium` |
| 75 | `C-0048` | HostPath mount | `apps/v1/kube-system/DaemonSet/cilium` |
| 76 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/cilium` |
| 77 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/cilium` |
| 78 | `C-0045` | Writable hostPath mount | `apps/v1/kube-system/DaemonSet/cilium` |
| 79 | `C-0188` | Minimize access to create pods | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 80 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 81 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 82 | `C-0002` | Prevent containers from allowing command execution | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 83 | `C-0037` | CoreDNS poisoning | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 84 | `C-0063` | Portforwarding privileges | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 85 | `C-0031` | Delete Kubernetes events | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 86 | `C-0015` | List Kubernetes secrets | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 87 | `C-0035` | Administrative Roles | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 88 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/csi-do-node-sa/rbac.authorizatio` |
| 89 | `C-0188` | Minimize access to create pods | `rbac.authorization.k8s.io//Group/do:modifier/rbac.authorizat` |
| 90 | `C-0002` | Prevent containers from allowing command execution | `rbac.authorization.k8s.io//Group/do:modifier/rbac.authorizat` |
| 91 | `C-0037` | CoreDNS poisoning | `rbac.authorization.k8s.io//Group/do:modifier/rbac.authorizat` |
| 92 | `C-0063` | Portforwarding privileges | `rbac.authorization.k8s.io//Group/do:modifier/rbac.authorizat` |
| 93 | `C-0015` | List Kubernetes secrets | `rbac.authorization.k8s.io//Group/do:modifier/rbac.authorizat` |
| 94 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-repo-server` |
| 95 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/selinux-warning-controller/rbac.` |
| 96 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/argocd-applicationset-controller` |
| 97 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cluster-autoscaler/rbac.authoriz` |
| 98 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 99 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 100 | `C-0015` | List Kubernetes secrets | `/kube-system/ServiceAccount/cilium-operator/rbac.authorizati` |
| 101 | `C-0057` | Privileged container | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 102 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 103 | `C-0048` | HostPath mount | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 104 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 105 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 106 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 107 | `C-0045` | Writable hostPath mount | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 108 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/legacy-service-account-token-` |
| 109 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/kubelet-rubber-stamp/rbac.author` |
| 110 | `C-0037` | CoreDNS poisoning | `/kube-system/ServiceAccount/kubelet-rubber-stamp/rbac.author` |
| 111 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/do-agent/rbac.authorization.k8s.` |
| 112 | `C-0188` | Minimize access to create pods | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 113 | `C-0053` | Access container service account | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 114 | `C-0007` | Roles with delete capabilities | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 115 | `C-0002` | Prevent containers from allowing command execution | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 116 | `C-0037` | CoreDNS poisoning | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 117 | `C-0063` | Portforwarding privileges | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 118 | `C-0031` | Delete Kubernetes events | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 119 | `C-0015` | List Kubernetes secrets | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 120 | `C-0035` | Administrative Roles | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |
| 121 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/validatingadmissionpolicy-status` |
| 122 | `C-0053` | Access container service account | `/argocd/ServiceAccount/argocd-server/rbac.authorization.k8s.` |
| 123 | `C-0007` | Roles with delete capabilities | `/argocd/ServiceAccount/argocd-server/rbac.authorization.k8s.` |
| 124 | `C-0037` | CoreDNS poisoning | `/argocd/ServiceAccount/argocd-server/rbac.authorization.k8s.` |
| 125 | `C-0031` | Delete Kubernetes events | `/argocd/ServiceAccount/argocd-server/rbac.authorization.k8s.` |
| 126 | `C-0015` | List Kubernetes secrets | `/argocd/ServiceAccount/argocd-server/rbac.authorization.k8s.` |
| 127 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/dosecret-operator/rbac.authoriza` |
| 128 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/dosecret-operator/rbac.authoriza` |
| 129 | `C-0031` | Delete Kubernetes events | `/kube-system/ServiceAccount/dosecret-operator/rbac.authoriza` |
| 130 | `C-0015` | List Kubernetes secrets | `/kube-system/ServiceAccount/dosecret-operator/rbac.authoriza` |
| 131 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/kubelet-rubber-stamp/rbac.author` |
| 132 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/kubelet-rubber-stamp` |
| 133 | `C-0034` | Automatic mapping of service account | `/v1/test-application/ServiceAccount/default` |
| 134 | `C-0256` | External facing | `apps/v1/argocd/Deployment/argocd-server` |
| 135 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/resource-claim-controller` |
| 136 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/legacy-service-account-token-cle` |
| 137 | `C-0007` | Roles with delete capabilities | `/kube-system/ServiceAccount/legacy-service-account-token-cle` |
| 138 | `C-0034` | Automatic mapping of service account | `/v1/default/ServiceAccount/zelyo-sa` |
| 139 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/dataplane-operator-controller` |
| 140 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/Deployment/hubble-ui` |
| 141 | `C-0055` | Linux hardening | `apps/v1/kube-system/Deployment/hubble-ui` |
| 142 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/headlamp` |
| 143 | `C-0057` | Privileged container | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 144 | `C-0034` | Automatic mapping of service account | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 145 | `C-0016` | Allow privilege escalation | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 146 | `C-0017` | Immutable container filesystem | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 147 | `C-0055` | Linux hardening | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 148 | `C-0007` | Roles with delete capabilities | `rbac.authorization.k8s.io//User/cilium-operator/rbac.authori` |
| 149 | `C-0015` | List Kubernetes secrets | `rbac.authorization.k8s.io//User/cilium-operator/rbac.authori` |
| 150 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/volumeattributesclass-protection` |
| 151 | `C-0034` | Automatic mapping of service account | `/v1/kube-system/ServiceAccount/csi-do-node-sa` |
| 152 | `C-0012` | Applications credentials in configuration files | `/v1/kube-system/ConfigMap/cilium-config` |
| 153 | `C-0057` | Privileged container | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 154 | `C-0041` | HostNetwork access | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 155 | `C-0046` | Insecure capabilities | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 156 | `C-0048` | HostPath mount | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 157 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 158 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 159 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 160 | `C-0037` | CoreDNS poisoning | `/kubescape/ServiceAccount/operator/rbac.authorization.k8s.io` |
| 161 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/service-cidrs-controller/rbac.au` |
| 162 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/resource-claim-controller/rbac.a` |
| 163 | `C-0053` | Access container service account | `/argocd/ServiceAccount/argocd-applicationset-controller/rbac` |
| 164 | `C-0015` | List Kubernetes secrets | `/argocd/ServiceAccount/argocd-applicationset-controller/rbac` |
| 165 | `C-0016` | Allow privilege escalation | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 166 | `C-0017` | Immutable container filesystem | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 167 | `C-0055` | Linux hardening | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 168 | `C-0034` | Automatic mapping of service account | `/v1/argocd/ServiceAccount/default` |
| 169 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/csi-do-controller-sa/rbac.author` |
| 170 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/dataplane-operator-controller-ma` |
| 171 | `C-0053` | Access container service account | `/kube-system/ServiceAccount/csi-do-controller-sa/rbac.author` |
| 172 | `C-0053` | Access container service account | `/default/ServiceAccount/zelyo-sa/rbac.authorization.k8s.io/v` |
| 173 | `C-0015` | List Kubernetes secrets | `/default/ServiceAccount/zelyo-sa/rbac.authorization.k8s.io/v` |

---

## 🔧 Configuration Findings (75)

*Detects: Missing resource limits, network policy gaps, non-root enforcement failures*

| # | Control | Description | Resource |
|---|---------|-------------|----------|
| 1 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 2 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 3 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 4 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 5 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/csi-do-node` |
| 6 | `C-0030` | Ingress and Egress blocked | `apps/v1/default/StatefulSet/zelyo-agent` |
| 7 | `C-0013` | Non-root containers | `apps/v1/default/StatefulSet/zelyo-agent` |
| 8 | `C-0270` | Ensure CPU limits are set | `apps/v1/default/StatefulSet/zelyo-agent` |
| 9 | `C-0271` | Ensure memory limits are set | `apps/v1/default/StatefulSet/zelyo-agent` |
| 10 | `C-0260` | Missing network policy | `apps/v1/default/StatefulSet/zelyo-agent` |
| 11 | `C-0013` | Non-root containers | `apps/v1/argocd/StatefulSet/argocd-application-controller` |
| 12 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/StatefulSet/argocd-application-controller` |
| 13 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/StatefulSet/argocd-application-controller` |
| 14 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 15 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 16 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 17 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/do-node-agent` |
| 18 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-redis` |
| 19 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-redis` |
| 20 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-redis` |
| 21 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/Deployment/hubble-relay` |
| 22 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/Deployment/hubble-relay` |
| 23 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/Deployment/hubble-relay` |
| 24 | `C-0260` | Missing network policy | `apps/v1/kube-system/Deployment/hubble-relay` |
| 25 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/Deployment/headlamp` |
| 26 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/Deployment/headlamp` |
| 27 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/Deployment/headlamp` |
| 28 | `C-0260` | Missing network policy | `apps/v1/kube-system/Deployment/headlamp` |
| 29 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 30 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 31 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 32 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 33 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/cpc-bridge-proxy-ebpf` |
| 34 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-dex-server` |
| 35 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-dex-server` |
| 36 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-dex-server` |
| 37 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-repo-server` |
| 38 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-repo-server` |
| 39 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-repo-server` |
| 40 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/cilium` |
| 41 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/cilium` |
| 42 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/cilium` |
| 43 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/DaemonSet/cilium` |
| 44 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/cilium` |
| 45 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-notifications-controller` |
| 46 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-notifications-controller` |
| 47 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-notifications-controller` |
| 48 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 49 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 50 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 51 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/do-node-agent-amd-device-metri` |
| 52 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-server` |
| 53 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-server` |
| 54 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-server` |
| 55 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/Deployment/hubble-ui` |
| 56 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/Deployment/hubble-ui` |
| 57 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/Deployment/hubble-ui` |
| 58 | `C-0260` | Missing network policy | `apps/v1/kube-system/Deployment/hubble-ui` |
| 59 | `C-0030` | Ingress and Egress blocked | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 60 | `C-0013` | Non-root containers | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 61 | `C-0270` | Ensure CPU limits are set | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 62 | `C-0271` | Ensure memory limits are set | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 63 | `C-0260` | Missing network policy | `/v1/zelyo-test/Pod/vulnerable-pod` |
| 64 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 65 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 66 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 67 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/do-node-agent-nvidia-dcgm-expo` |
| 68 | `C-0013` | Non-root containers | `apps/v1/argocd/Deployment/argocd-applicationset-controller` |
| 69 | `C-0270` | Ensure CPU limits are set | `apps/v1/argocd/Deployment/argocd-applicationset-controller` |
| 70 | `C-0271` | Ensure memory limits are set | `apps/v1/argocd/Deployment/argocd-applicationset-controller` |
| 71 | `C-0030` | Ingress and Egress blocked | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 72 | `C-0013` | Non-root containers | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 73 | `C-0270` | Ensure CPU limits are set | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 74 | `C-0271` | Ensure memory limits are set | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |
| 75 | `C-0260` | Missing network policy | `apps/v1/kube-system/DaemonSet/konnectivity-agent` |

---

## 📋 Other Findings (3)

| # | Control | Description | Resource |
|---|---------|-------------|----------|
| 1 | `C-0187` | Minimize wildcard use in Roles and ClusterRoles | `rbac.authorization.k8s.io//Group/k8saas:authenticated/rbac.a` |
| 2 | `C-0187` | Minimize wildcard use in Roles and ClusterRoles | `/kube-system/ServiceAccount/headlamp/rbac.authorization.k8s.` |
| 3 | `C-0187` | Minimize wildcard use in Roles and ClusterRoles | `/argocd/ServiceAccount/argocd-application-controller/rbac.au` |

---

## 📊 Real-Time Monitoring (Planned)

| Anomaly Type | Use Case | Status |
|--------------|----------|--------|
| Request Spikes | DDOS detection | 🔜 |
| Privilege Escalation | Malicious behavior | 🔜 |
| Excessive Syscalls | Exploit attempts | 🔜 |
| Bandwidth Spikes | Data exfiltration | 🔜 |
| CPU/Memory Spikes | Resource abuse | 🔜 |

---

## 🔄 GitOps Remediation Flow

```
Detect → Analyze → Generate Fix → Create PR → Senior Approval → Apply via ArgoCD
```

**Principle:** All fixes require human validation (Human-in-the-Loop).

---

## ✅ Test Results

| Category | Passed | Skipped |
|----------|--------|---------|
| Configuration Scanning | 5 | 0 |
| Security Scanning | 6 | 0 |
| Real-Time Monitoring | 0 | 6 |
| GitOps Remediation | 4 | 0 |
| Integration | 3 | 0 |
| **Total** | **18** | **6** |

---

*Generated by Zelyo Config Guardian v0.1.0*
