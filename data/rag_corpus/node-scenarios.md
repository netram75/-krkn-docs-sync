---
title: Node Scenarios
description: Disrupts cluster nodes via stop, reboot, crash, or kubelet actions to test node-level resilience
date: 2017-01-04
weight: 3
---

This scenario disrupts the node(s) matching the label or node name(s) on a Kubernetes/OpenShift cluster.

## Supported Actions

1. **node_start_scenario**: Start the node instance
2. **node_stop_scenario**: Stop the node instance
3. **node_stop_start_scenario**: Stop and then start the node instance
4. **node_termination_scenario**: Terminate the node instance
5. **node_reboot_scenario**: Reboot the node instance
6. **stop_kubelet_scenario**: Stop the kubelet of the node instance
7. **restart_kubelet_scenario**: Restart the kubelet of the node instance
8. **node_crash_scenario**: Crash the node instance

## Key Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `node_name` | string | one of | - | Name of the node to target |
| `label_selector` | string | one of | - | Label selector to match nodes |
| `action` | string | yes | - | The node scenario action to perform |
| `timeout` | number | no | 120 | Max seconds to wait for node recovery |
| `cloud_type` | string | no | generic | Cloud provider type (aws, azure, gcp, generic) |

## How to Run Node Scenarios

{{< tabpane text=true >}}
  {{< tab header="**Krkn**" lang="krkn" >}}
{{< readfile file="_tab-krkn.md" >}}
  {{< /tab >}}
  {{< tab header="**Krkn-hub**" lang="krkn-hub" >}}
{{< readfile file="_tab-krkn-hub.md" >}}
  {{< /tab >}}
  {{< tab header="**Krknctl**" lang="krknctl" >}}
{{< readfile file="_tab-krknctl.md" >}}
  {{< /tab >}}
{{< /tabpane >}}

{{% alert title="Note" %}}If the node does not recover from the node_crash_scenario injection, reboot the node to get it back to Ready state.{{% /alert %}}
