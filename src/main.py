import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from diff_parser import ScenarioChange, extract_symbols, parse_changed_scenarios
from doc_generator import generate_doc
from hugo_validator import validate
from pr_creator import raise_pr
from relevance_gate import is_doc_relevant


def _load_target_file(path: str) -> ScenarioChange:
    if not os.path.isfile(path):
        print(f"[docs-sync] target file not found: {path}")
        sys.exit(1)
    source_bytes = open(path, "rb").read()
    classes, functions = extract_symbols(source_bytes)
    return ScenarioChange(
        file_path=path,
        classes=classes,
        functions=functions,
        source=source_bytes.decode(errors="replace"),
    )


def run() -> None:
    target_file = os.environ.get("TARGET_FILE", "").strip()

    if target_file:
        changes = [_load_target_file(target_file)]
    else:
        changes = parse_changed_scenarios()

    if not changes:
        print("[docs-sync] no scenario changes detected")
        sys.exit(0)

    for change in changes:
        print(f"[docs-sync] detected: {change.file_path}")
        if change.classes:
            print(f"  classes   : {', '.join(change.classes)}")
        if change.functions:
            print(f"  functions : {', '.join(change.functions[:8])}")

        print("[docs-sync] checking relevance...")
        if not is_doc_relevant(change):
            print(f"[docs-sync] skipped (not doc-relevant): {change.file_path}")
            continue

        print("[docs-sync] generating documentation...")
        doc_content = generate_doc(change)

        print(f"\n{'='*60}")
        print(doc_content[:800])
        print(f"{'='*60}\n")

        result = validate(doc_content)
        if not result.valid:
            print(f"[docs-sync] validation failed: {result.errors}")
            continue

        print("[docs-sync] opening PR...")
        pr_url = raise_pr(change.file_path, doc_content)
        print(f"[docs-sync] PR opened: {pr_url}")

    print("[docs-sync] done")


if __name__ == "__main__":
    run()
