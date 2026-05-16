import os

import yaml


def load(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_with_env(path: str) -> dict:
    data = load(path)
    for key, value in data.items():
        if isinstance(value, str) and value.startswith("$"):
            env_key = value[1:]
            data[key] = os.environ.get(env_key, value)
    return data
