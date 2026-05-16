"""
Smoke tests for the docs-sync pipeline.
5 positive cases (should be doc-relevant) + 3 negative cases (should not).
Requires GEMINI_API_KEY in environment.
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from diff_parser import ScenarioChange, extract_symbols
from relevance_gate import is_doc_relevant

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")

POSITIVE_CASES = [
    "vmi_network_chaos.py",
    "cpu_hog_chaos.py",
    "disk_fill_chaos.py",
    "pod_kill_chaos.py",
    "node_cpu_hog.py",
]

NEGATIVE_CASES = [
    os.path.join("negative", "utils_helper.py"),
    os.path.join("negative", "config_loader.py"),
    os.path.join("negative", "base_scenario.py"),
]


def load_fixture(rel_path: str) -> ScenarioChange:
    path = os.path.join(FIXTURES, rel_path)
    source_bytes = open(path, "rb").read()
    classes, functions = extract_symbols(source_bytes)
    return ScenarioChange(
        file_path=path,
        classes=classes,
        functions=functions,
        source=source_bytes.decode(errors="replace"),
    )


def run_tests() -> None:
    passed = 0
    failed = 0

    print("=== positive cases (expect: doc-relevant) ===")
    for fixture in POSITIVE_CASES:
        change = load_fixture(fixture)
        result = is_doc_relevant(change)
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {fixture}")
        time.sleep(4)

    print("\n=== negative cases (expect: not doc-relevant) ===")
    for fixture in NEGATIVE_CASES:
        change = load_fixture(fixture)
        result = is_doc_relevant(change)
        status = "PASS" if not result else "FAIL"
        if not result:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {os.path.basename(fixture)}")
        time.sleep(4)

    print(f"\n{passed}/{passed + failed} passed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
