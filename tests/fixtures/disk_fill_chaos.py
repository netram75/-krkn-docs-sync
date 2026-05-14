"""
Disk Fill Chaos scenario plugin for krkn-chaos.
Fills disk space on a target node to simulate storage exhaustion.
"""

import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DiskFillConfig:
    node_name: str
    mount_path: str = "/var/lib/etcd"
    fill_percentage: int = 80   # fill disk up to this % capacity
    duration: int = 60
    wait_timeout: int = 300


class DiskFillChaos:
    def __init__(self, kubecli, telemetry_api=None):
        self.kubecli = kubecli
        self.telemetry = telemetry_api

    def inject(self, config: DiskFillConfig) -> None:
        logger.info(
            "filling disk on node %s at %s to %d%%",
            config.node_name, config.mount_path, config.fill_percentage,
        )
        self.kubecli.exec_cmd_on_node(
            config.node_name,
            f"fallocate -l $(df {config.mount_path} | awk 'NR==2 {{printf \"%d\", $2*{config.fill_percentage}/100-$3}}')K "
            f"{config.mount_path}/chaos_fill.tmp",
        )
        time.sleep(config.duration)
        self.kubecli.exec_cmd_on_node(config.node_name, f"rm -f {config.mount_path}/chaos_fill.tmp")
        logger.info("disk fill cleared on node %s", config.node_name)

    def run(self, scenario_config: dict) -> None:
        config = DiskFillConfig(**scenario_config)
        self.inject(config)
