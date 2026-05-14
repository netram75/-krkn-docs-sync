import re
from dataclasses import dataclass, field

REQUIRED_FIELDS = ("title", "description", "weight")


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


def validate(content: str) -> ValidationResult:
    errors = []

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return ValidationResult(valid=False, errors=["missing YAML frontmatter block"])

    frontmatter = match.group(1)

    for field_name in REQUIRED_FIELDS:
        if not re.search(rf"^{field_name}\s*:", frontmatter, re.MULTILINE):
            errors.append(f"missing required field: {field_name}")

    weight_match = re.search(r"^weight\s*:\s*(.+)$", frontmatter, re.MULTILINE)
    if weight_match:
        val = weight_match.group(1).strip()
        if val.startswith(('"', "'")):
            errors.append(f"weight must be an integer, not a string: {val}")
        elif not val.lstrip("-").isdigit():
            errors.append(f"weight must be an integer: {val}")

    return ValidationResult(valid=len(errors) == 0, errors=errors)
