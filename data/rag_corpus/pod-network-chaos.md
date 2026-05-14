---
title: Pod Network Chaos
description: Injects network faults such as packet loss, latency, and bandwidth limits on a target pod
weight: 3
---

## Scenario Description

The Pod Network Chaos scenario injects network faults directly on a target pod using Linux traffic control (`tc netem`). It supports packet loss, artificial latency, and bandwidth throttling. Use this scenario to validate how your application behaves under degraded network conditions.

## Prerequisites

- A running OpenShift/Kubernetes cluster
- krkn-chaos installed and configured
- Target pod must be running and accessible

## Scenario Configuration

```yaml
pod_network_chaos_scenario:
  namespace: "default"     # namespace of the target pod
  pod_label: ""            # label selector e.g. app=frontend
  interface: "eth0"        # network interface inside the pod
  loss: 0                  # packet loss percentage (0-100)
  latency: 0               # added latency in milliseconds
  bandwidth: ""            # bandwidth limit e.g. "100mbit"
  duration: 60             # chaos duration in seconds
  wait_timeout: 300
```

### Example

```yaml
pod_network_chaos_scenario:
  namespace: "production"
  pod_label: "app=payment-service"
  interface: "eth0"
  loss: 10
  latency: 200
  duration: 120
  wait_timeout: 600
```

## Scenario Execution

### krkn

```bash
python run_kraken.py --config config/pod_network_chaos.yaml
```

### krkn-hub

```bash
krkn-hub run pod-network-chaos \
  --namespace production \
  --pod-label app=payment-service \
  --loss 10 \
  --latency 200 \
  --duration 120
```

### krknctl

```bash
krknctl run pod-network-chaos \
  --namespace production \
  --pod-label app=payment-service \
  --loss 10 \
  --latency 200 \
  --duration 120
```
