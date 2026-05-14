"""
VMI Network Chaos scenario plugin for krkn-chaos.
Injects network faults (packet loss, latency, bandwidth limits) on Virtual Machine
Interfaces running on OpenShift Virtualization (KubeVirt).
"""

import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VmiNetworkChaosConfig:
    namespace: str
    vmi_name: str
    interface: str = "eth0"
    loss: int = 0           # packet loss percentage (0-100)
    latency: int = 0        # latency in milliseconds
    bandwidth: str = ""     # bandwidth limit e.g. "100mbit"
    duration: int = 60      # chaos duration in seconds
    wait_timeout: int = 300


class VmiNetworkChaos:
    def __init__(self, kubecli, telemetry_api=None):
        self.kubecli = kubecli
        self.telemetry = telemetry_api

    def inject(self, config: VmiNetworkChaosConfig) -> None:
        logger.info(
            "injecting network chaos on VMI %s/%s interface %s",
            config.namespace, config.vmi_name, config.interface,
        )
        self._apply_tc_rules(config)
        time.sleep(config.duration)
        self._clear_tc_rules(config)
        logger.info("network chaos cleared on VMI %s/%s", config.namespace, config.vmi_name)

    def _apply_tc_rules(self, config: VmiNetworkChaosConfig) -> None:
        cmds = [f"tc qdisc add dev {config.interface} root netem"]
        if config.loss:
            cmds.append(f"loss {config.loss}%")
        if config.latency:
            cmds.append(f"delay {config.latency}ms")
        if config.bandwidth:
            cmds.append(f"rate {config.bandwidth}")
        cmd = " ".join(cmds)
        self.kubecli.exec_cmd_in_vmi(config.namespace, config.vmi_name, cmd)

    def _clear_tc_rules(self, config: VmiNetworkChaosConfig) -> None:
        cmd = f"tc qdisc del dev {config.interface} root"
        self.kubecli.exec_cmd_in_vmi(config.namespace, config.vmi_name, cmd)

    def run(self, scenario_config: dict) -> None:
        config = VmiNetworkChaosConfig(**scenario_config)
        self.inject(config)
