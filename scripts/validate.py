#!/usr/bin/env python3
"""Validate this repository's deliberately small YAML subset and local links."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "kunka-screenwriting" / "skills"


def validate(root=ROOT):
    root = Path(root).resolve()
    skills = root / "plugins" / "kunka-screenwriting" / "skills"
    errors = []
    folders = sorted(skills.iterdir())
    if len(folders) != 13:
        errors.append(f"Expected 13 skills, found {len(folders)}")
    names = {p.name for p in folders}
    sizes = {}
    for folder in folders:
        if folder.is_symlink() or not folder.is_dir():
            errors.append(f"Invalid skill folder: {folder}")
            continue
        path = folder / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing SKILL.md: {folder}")
            continue
        text = path.read_text(encoding="utf-8")
        sizes[folder.name] = len(text.encode("utf-8"))
        # This project uses plain names and JSON-quoted descriptions (valid YAML).
        match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ("[^\n]+")\n---\n', text)
        if not match or match[1] != folder.name:
            errors.append(f"Invalid or mismatched frontmatter: {path}")
        else:
            try:
                description = json.loads(match[2])
                if not 15 <= len(description) <= 240:
                    errors.append(f"Description must be 15–240 characters: {path}")
            except json.JSONDecodeError:
                errors.append(f"Invalid quoted description: {path}")
        if sizes[folder.name] > 8000:
            errors.append(f"Entrypoint exceeds 8,000 bytes; split optional material: {path}")
        for target in re.findall(r'`(kunka-[a-z0-9-]+)`', text):
            if target not in names:
                errors.append(f"Unknown skill reference {target}: {path}")
        ui = folder / "agents" / "openai.yaml"
        if not ui.is_file():
            errors.append(f"Missing UI metadata: {ui}")
        else:
            values = {}
            for line in ui.read_text(encoding="utf-8").splitlines():
                item = re.fullmatch(r'  ([a-z_]+): (".*")', line)
                if item:
                    try:
                        values[item[1]] = json.loads(item[2])
                    except json.JSONDecodeError:
                        errors.append(f"Invalid UI string: {ui}")
            if not values.get("display_name") or not 25 <= len(values.get("short_description", "")) <= 64:
                errors.append(f"Invalid UI title or description: {ui}")
            if "$" + folder.name not in values.get("default_prompt", ""):
                errors.append(f"UI prompt must mention skill: {ui}")
    for path in root.rglob("*.md"):
        if ".git" in path.relative_to(root).parts:
            continue
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+://", link) or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            if root != target and root not in target.parents:
                errors.append(f"Link escapes repository: {path}: {link}")
            elif not target.exists():
                errors.append(f"Broken local link: {path}: {link}")
    try:
        marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text())
        plugin = json.loads((root / "plugins/kunka-screenwriting/.claude-plugin/plugin.json").read_text())
        entry = marketplace["plugins"][0]
        if entry["source"] != "./plugins/kunka-screenwriting" or entry["name"] != plugin["name"]:
            errors.append("Marketplace source or plugin name mismatch")
        if marketplace["name"] != "kunka-screenwriting-master" or plugin["version"] != "1.0.0":
            errors.append("Unexpected marketplace name or release version")
    except (OSError, KeyError, IndexError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid plugin packaging: {exc}")
    return errors, sizes


if __name__ == "__main__":
    issues, sizes = validate()
    for issue in issues:
        print(issue, file=sys.stderr)
    print(json.dumps({"skills": len(sizes), "entrypoint_bytes": sum(sizes.values()), "largest_bytes": max(sizes.values(), default=0), "errors": len(issues)}, indent=2))
    sys.exit(bool(issues))
