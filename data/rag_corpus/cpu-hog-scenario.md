---
title: CPU Hog Scenario
description: Generates CPU pressure on cluster nodes to test application resilience under resource contention
date: 2017-01-04
weight: 2
---

## Overview

The CPU Hog scenario is designed to create CPU pressure on one or more nodes in your Kubernetes/OpenShift cluster for a specified duration. This scenario helps you test how your cluster and applications respond to high CPU utilization.

## How It Works

The scenario deploys a stress workload pod on targeted nodes. These pods use [stress-ng](https://github.com/ColinIanKing/stress-ng) to consume CPU resources according to your configuration. The workload runs for a specified duration and then terminates, allowing you to observe your cluster's behavior under CPU stress.

## When to Use

Use the CPU Hog scenario to:
- Test your cluster's ability to handle CPU resource contention
- Validate that CPU resource limits and quotas are properly configured
- Evaluate the impact of CPU pressure on application performance
- Test whether your monitoring and alerting systems properly detect CPU saturation
- Verify that the Kubernetes scheduler correctly handles CPU-constrained nodes

## Key Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `cpu-load-percentage` | number | The percentage of CPU that will be consumed by the hog |
| `cpu-method` | string | The CPU load strategy adopted by stress-ng |
| `duration` | number | Duration in seconds to run the CPU hog |
| `node-selectors` | string | Label selectors to target specific nodes |

## How to Run CPU Hog Scenarios

Choose your preferred method to run CPU hog scenarios:

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
