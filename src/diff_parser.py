import os
import subprocess
from dataclasses import dataclass, field

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

_PY_LANGUAGE = Language(tspython.language())


@dataclass
class ScenarioChange:
    file_path: str
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    source: str = ""


def _changed_files(base: str = "HEAD~1", head: str = "HEAD") -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base, head],
            capture_output=True, text=True, check=True,
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip().endswith(".py")]
    except subprocess.CalledProcessError:
        return []


def _is_scenario_file(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    return any(p in ("scenario_plugins", "scenarios") for p in parts)


def extract_symbols(source_bytes: bytes) -> tuple[list[str], list[str]]:
    parser = Parser(_PY_LANGUAGE)
    tree = parser.parse(source_bytes)

    classes: list[str] = []
    functions: list[str] = []

    def walk(node):
        if node.type == "class_definition":
            name = node.child_by_field_name("name")
            if name:
                classes.append(source_bytes[name.start_byte:name.end_byte].decode())
        elif node.type == "function_definition":
            name = node.child_by_field_name("name")
            if name:
                functions.append(source_bytes[name.start_byte:name.end_byte].decode())
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return classes, functions


def parse_changed_scenarios(base: str = "HEAD~1", head: str = "HEAD") -> list[ScenarioChange]:
    changed = _changed_files(base, head)
    scenario_files = [f for f in changed if _is_scenario_file(f)]

    results = []
    for path in scenario_files:
        if not os.path.isfile(path):
            continue
        source_bytes = open(path, "rb").read()
        classes, functions = extract_symbols(source_bytes)
        results.append(ScenarioChange(
            file_path=path,
            classes=classes,
            functions=functions,
            source=source_bytes.decode(errors="replace"),
        ))

    return results
