import logging
import random

from kubernetes import client, config


class PodKillChaosConfig:
    def __init__(self, namespace: str, label_selector: str, kill_count: int = 1, timeout: int = 60):
        self.namespace = namespace
        self.label_selector = label_selector
        self.kill_count = kill_count
        self.timeout = timeout


class PodKillChaos:
    def __init__(self, kubeconfig_path: str = None):
        if kubeconfig_path:
            config.load_kube_config(kubeconfig_path)
        else:
            config.load_incluster_config()
        self.v1 = client.CoreV1Api()

    def _list_pods(self, namespace: str, label_selector: str) -> list:
        pods = self.v1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
        return [p.metadata.name for p in pods.items if p.status.phase == "Running"]

    def inject(self, cfg: PodKillChaosConfig) -> dict:
        pods = self._list_pods(cfg.namespace, cfg.label_selector)
        if not pods:
            logging.warning("no running pods matched selector %s in %s", cfg.label_selector, cfg.namespace)
            return {"killed": [], "recovered": []}

        targets = random.sample(pods, min(cfg.kill_count, len(pods)))
        killed = []
        for pod in targets:
            self.v1.delete_namespaced_pod(name=pod, namespace=cfg.namespace)
            logging.info("deleted pod %s/%s", cfg.namespace, pod)
            killed.append(pod)

        recovered = self._wait_recovery(cfg.namespace, cfg.label_selector, len(killed), cfg.timeout)
        return {"killed": killed, "recovered": recovered}

    def _wait_recovery(self, namespace: str, label_selector: str, expected: int, timeout: int) -> list:
        import time
        deadline = time.time() + timeout
        while time.time() < deadline:
            running = self._list_pods(namespace, label_selector)
            if len(running) >= expected:
                return running
            time.sleep(5)
        return []

    def run(self, cfg: PodKillChaosConfig) -> None:
        result = self.inject(cfg)
        logging.info("pod kill chaos complete: killed=%s recovered=%s", result["killed"], result["recovered"])
