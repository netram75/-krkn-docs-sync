import logging
import subprocess

from kubernetes import client, config


class NodeCpuHogConfig:
    def __init__(self, node_name: str, duration: int = 60, cpu_percent: int = 90, workers: int = 4):
        self.node_name = node_name
        self.duration = duration
        self.cpu_percent = cpu_percent
        self.workers = workers


class NodeCpuHog:
    def __init__(self, kubeconfig_path: str = None):
        if kubeconfig_path:
            config.load_kube_config(kubeconfig_path)
        else:
            config.load_incluster_config()
        self.v1 = client.CoreV1Api()

    def _node_exists(self, node_name: str) -> bool:
        nodes = self.v1.list_node(field_selector=f"metadata.name={node_name}")
        return len(nodes.items) > 0

    def inject(self, cfg: NodeCpuHogConfig) -> bool:
        if not self._node_exists(cfg.node_name):
            logging.error("node %s not found", cfg.node_name)
            return False

        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": f"cpu-hog-{cfg.node_name}", "namespace": "default"},
            "spec": {
                "nodeName": cfg.node_name,
                "restartPolicy": "Never",
                "containers": [{
                    "name": "stress",
                    "image": "polinux/stress",
                    "args": ["stress", "--cpu", str(cfg.workers), "--timeout", str(cfg.duration)],
                    "resources": {"requests": {"cpu": "100m"}},
                }],
            },
        }

        self.v1.create_namespaced_pod(namespace="default", body=pod_manifest)
        logging.info("cpu hog started on node %s for %ds at %d%%", cfg.node_name, cfg.duration, cfg.cpu_percent)
        return True

    def cleanup(self, cfg: NodeCpuHogConfig) -> None:
        try:
            self.v1.delete_namespaced_pod(name=f"cpu-hog-{cfg.node_name}", namespace="default")
        except Exception as exc:
            logging.warning("cleanup failed: %s", exc)

    def run(self, cfg: NodeCpuHogConfig) -> None:
        if self.inject(cfg):
            import time
            time.sleep(cfg.duration + 5)
            self.cleanup(cfg)
