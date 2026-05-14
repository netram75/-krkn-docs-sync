---
title: Node Interface Down
description: Brings down a network interface on a target node to simulate NIC failure or network partition
weight: 2
---

## Scenario Description

The Node Interface Down scenario takes down a specified network interface on a target node using `ip link set <interface> down`. This simulates NIC failure or network partition conditions and validates application resilience when a node loses network connectivity.

## Prerequisites

- A running OpenShift/Kubernetes cluster
- krkn-chaos installed and configured
- SSH or exec access to target nodes

## Scenario Configuration

```yaml
node_interface_down_scenario:
  node_name: ""         # target node (empty = random worker node)
  interface: "eth0"     # network interface to bring down
  duration: 60          # seconds to hold interface down
  wait_timeout: 300     # seconds to wait for node recovery
```

### Example

```yaml
node_interface_down_scenario:
  node_name: "worker-0.example.com"
  interface: "eth0"
  duration: 120
  wait_timeout: 600
```

## Scenario Execution

### krkn

```bash
python run_kraken.py --config config/node_interface_down.yaml
```

### krkn-hub

```bash
krkn-hub run node-interface-down \
  --node worker-0.example.com \
  --interface eth0 \
  --duration 120
```

### krknctl

```bash
krknctl run node-interface-down \
  --node-name worker-0.example.com \
  --interface eth0 \
  --duration 120
```
