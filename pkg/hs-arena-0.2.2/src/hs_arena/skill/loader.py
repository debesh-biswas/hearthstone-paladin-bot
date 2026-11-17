"""Skill submissions: SKILL.md plus optional scripts, references and deck recipes.

A skill picks the model that plays it in the SKILL.md frontmatter:

    ---
    name: frostbolt-enjoyer
    description: Tempo Mage that trades early and burns face late.
    model: haiku            # haiku = Claude Haiku 5.5 in Claude Code, luna = GPT-6-Luna in Codex
    ---
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# model key -> harness and model id; reasoning effort is medium for everyone
MODELS = {
    "haiku": {"harness": "claude", "model_id": "claude-haiku-5-5", "label": "Claude Haiku 5.5 (Claude Code)"},
    "luna": {"harness": "codex", "model_id": "gpt-6-luna", "label": "GPT-6-Luna (Codex)"},
}
EFFORT = "medium"
FRONTMATTER_FIELDS = ("name", "description", "model")
RESERVED_NAMES = ("game", "scratch")  # created by the skill seat inside the agent's folder
NOT_SHOWN = ("README.md",)  # notes for the staff; never copied into the agent's folder


class SkillError(ValueError):
    def __init__(self, errors: list[str], warnings: list[str] | None = None):
        self.errors = list(errors)
        self.warnings = list(warnings or [])
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class Skill:
    path: Path
    name: str
    description: str
    model: str
    body: str  # SKILL.md without the frontmatter
    requirements: tuple[str, ...] = ()
    warnings: tuple[str, ...] = field(default=())

    @property
    def harness(self) -> str:
        return MODELS[self.model]["harness"]

    @property
    def model_id(self) -> str:
        return MODELS[self.model]["model_id"]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    """Split SKILL.md into (frontmatter fields, body, errors). Supports simple `key: value` lines."""
    errors: list[str] = []
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["SKILL.md: must start with a '---' frontmatter block (name, description, model)"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text, ["SKILL.md: the frontmatter block is not closed with '---'"]
    fields: dict[str, str] = {}
    for n, raw in enumerate(lines[1:end], 2):
        line = raw.split(" #", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            errors.append(f"SKILL.md line {n}: expected 'key: value', got {raw.strip()!r}")
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    body = "\n".join(lines[end + 1:]).strip("\n")
    return fields, body, errors


def load_skill(path: str | Path) -> Skill:
    """Load and validate a skill directory; raises SkillError listing every problem."""
    path = Path(path).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_dir():
        raise SkillError([f"{path}: not a directory"])
    fields: dict[str, str] = {}
    body = ""
    skill_md = path / "SKILL.md"
    try:
        fields, body, fm_errors = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        errors += fm_errors
    except FileNotFoundError:
        errors.append("SKILL.md: file not found")
    except UnicodeDecodeError as e:
        errors.append(f"SKILL.md: not UTF-8 text ({e})")
    if skill_md.exists() and not errors:
        for key in FRONTMATTER_FIELDS:
            if not fields.get(key):
                errors.append(f"SKILL.md: frontmatter field '{key}' is missing or empty")
        model = fields.get("model", "").strip().lower()
        if fields.get("model") and model not in MODELS:
            errors.append(f"SKILL.md: model {fields['model']!r} must be one of: {', '.join(MODELS)}")
        for key in fields:
            if key not in FRONTMATTER_FIELDS:
                warnings.append(f"SKILL.md: frontmatter field '{key}' is ignored")
        if not body.strip():
            warnings.append("SKILL.md: the playbook (text after the frontmatter) is empty")
    for name in RESERVED_NAMES:
        if (path / name).exists():
            errors.append(f"'{name}' is reserved: the skill seat creates {name}/ in the agent's folder; rename yours")
    requirements: list[str] = []
    req = path / "requirements.txt"
    if req.exists():
        try:
            requirements = [ln.strip() for ln in req.read_text(encoding="utf-8").splitlines()
                            if ln.strip() and not ln.strip().startswith("#")]
        except UnicodeDecodeError as e:
            errors.append(f"requirements.txt: not UTF-8 text ({e})")
    if errors:
        raise SkillError(errors, warnings)
    return Skill(path=path, name=fields["name"], description=fields["description"],
                 model=fields["model"].strip().lower(), body=body, requirements=tuple(requirements),
                 warnings=tuple(warnings))


def is_skill_dir(path: str | Path) -> bool:
    return (Path(path) / "SKILL.md").exists()
