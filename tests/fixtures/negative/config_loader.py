"""Config loader — internal module, not a user-facing chaos scenario."""

import yaml


def load(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)
