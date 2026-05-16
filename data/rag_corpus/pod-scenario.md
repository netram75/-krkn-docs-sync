---
title: Pod Scenarios
description: Disrupts pods matching label selectors or name patterns to validate application resilience and recovery
date: 2017-01-04
weight: 3
---

This scenario disrupts the pods matching the label, excluded label or pod name in the specified namespace on a Kubernetes/OpenShift cluster.

## Why Pod Scenarios Are Important

Modern applications demand high availability, low downtime, and resilient infrastructure. Pod disruption scenarios test reliability under various conditions, validating that the application and infrastructure respond as expected.

## Key Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `namespace_pattern` | string | yes | - | Regex pattern to match target namespaces |
| `label_selector` | string | one of | "" | Label selector to match pods |
| `name_pattern` | string | one of | "" | Regex pattern to match pod names |
| `kill` | number | no | 1 | Number of pods to kill per iteration |
| `krkn_pod_recovery_time` | number | no | 120 | Max seconds to wait for pod recovery |
| `exclude_label` | string | no | "" | Label selector for pods to exclude |

## How to Run Pod Scenarios

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
