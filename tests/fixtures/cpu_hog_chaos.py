"""
CPU Hog Chaos scenario plugin for krkn-chaos.
Stresses CPU on a target node or pod to simulate compute resource exhaustion.
"""

import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CpuHogConfig:
    namespace: str
    pod_label: str
    cores: int = 0          # 0 = all available cores
    duration: int = 60
    wait_timeout: int = 300


class CpuHogChaos:
    def __init__(self, kubecli, telemetry_api=None):
        self.kubecli = kubecli
        self.telemetry = telemetry_api

    def inject(self, config: CpuHogConfig) -> None:
        logger.info(
            "injecting CPU hog on pods matching %s in %s",
            config.pod_label, config.namespace,
        )
        pods = self.kubecli.list_pods(config.namespace, label_selector=config.pod_label)
        for pod in pods:
            cores = config.cores or self.kubecli.get_node_cpu_count(pod.spec.node_name)
            cmd = f"stress-ng --cpu {cores} --timeout {config.duration}s"
            self.kubecli.exec_cmd_in_pod(config.namespace, pod.metadata.name, cmd)
        time.sleep(config.duration)
        logger.info("CPU hog complete on %s/%s", config.namespace, config.pod_label)

    def run(self, scenario_config: dict) -> None:
        config = CpuHogConfig(**scenario_config)
        self.inject(config)
