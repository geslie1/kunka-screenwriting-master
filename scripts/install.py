#!/usr/bin/env python3
"""Install Kunka skills locally; no network or third-party dependencies."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / "kunka-screenwriting" / "skills"


def inventory(folder):
    """Reject symlinks instead of following them into unrelated data."""
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError(f"Not a regular skill directory: {folder}")
    result = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not supported: {path}")
        if path.is_file():
            result[str(path.relative_to(folder))] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise ValueError(f"Unsupported file type: {path}")
    return result


def select_skills(source, names=None):
    available = {p.name: p for p in source.iterdir() if p.is_dir() or p.is_symlink()}
    names = sorted(set(names or available))
    if not names:
        raise ValueError("No skills found")
    result = []
    for name in names:
        if not re.fullmatch(r"kunka-[a-z0-9]+(?:-[a-z0-9]+)*", name) or name not in available:
            raise ValueError(f"Unknown skill: {name}")
        path = available[name]
        files = inventory(path)
        if "SKILL.md" not in files:
            raise ValueError(f"Missing SKILL.md: {path}")
        text = (path / "SKILL.md").read_text(encoding="utf-8")
        if not text.startswith(f"---\nname: {name}\n"):
            raise ValueError(f"Skill name does not match directory: {path}")
        result.append((name, path, files))
    return result


@contextmanager
def install_lock(destination):
    lock = destination / ".kunka-install.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"Another install may be active: {lock}. Check it before removing a stale lock.") from exc
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def plan_install(skills, destination, update):
    plan = []
    for name, source, files in skills:
        target = destination / name
        if target.is_symlink():
            raise ValueError(f"Refusing a symbolic-link target: {target}")
        exists = target.exists()
        if exists and inventory(target) == files:
            action = "unchanged"
        elif exists:
            if not update:
                raise ValueError(f"Existing files differ: {target}. Use --update to back up and replace this skill.")
            action = "update"
        else:
            action = "install"
        plan.append((name, source, target, action, files))
    return plan


def install(source, destination, names=None, update=False, dry_run=False):
    source = Path(source).resolve()
    destination = Path(destination).expanduser().resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Source and destination must not contain each other")
    skills = select_skills(source, names)
    if dry_run:
        plan = plan_install(skills, destination, update)
        return {"destination": str(destination), "actions": {p[0]: p[3] for p in plan}, "backup": None, "dry_run": True}
    destination.mkdir(parents=True, exist_ok=True)
    with install_lock(destination):
        plan = plan_install(skills, destination, update)
        changes = [p for p in plan if p[3] != "unchanged"]
        result = {"destination": str(destination), "actions": {p[0]: p[3] for p in plan}, "backup": None, "dry_run": False}
        if not changes:
            return result
        # Stage every source before moving any existing installation.
        with tempfile.TemporaryDirectory(prefix=".kunka-stage-", dir=destination) as temporary:
            stage = Path(temporary)
            for name, src, target, action, files in changes:
                shutil.copytree(src, stage / name)
                if inventory(stage / name) != files:
                    raise ValueError(f"Source changed during installation: {name}")
            backup = None
            if any(p[3] == "update" for p in changes):
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                backup = destination.parent / (destination.name + "-kunka-backups") / (stamp + "-" + uuid.uuid4().hex[:8])
                backup.mkdir(parents=True, exist_ok=False)
                result["backup"] = str(backup)
            moved = []
            installed = []
            try:
                for name, src, target, action, files in changes:
                    # Recheck the target before moving staged files into place.
                    if action == "install" and (target.exists() or target.is_symlink()):
                        raise ValueError(f"Destination appeared during installation: {target}")
                    if action == "update":
                        if target.is_symlink():
                            raise ValueError(f"Destination became a symbolic link: {target}")
                        target.rename(backup / name)
                        moved.append((backup / name, target))
                    (stage / name).rename(target)
                    installed.append(target)
            except BaseException:
                # Restore only this invocation's changes; unrelated skills stay intact.
                for target in reversed(installed):
                    shutil.rmtree(target)
                for saved, target in reversed(moved):
                    saved.rename(target)
                raise
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    parser.add_argument("--dest", type=Path, default=default_home / "skills")
    parser.add_argument("--skill", action="append", dest="names", help="Install only this skill; repeat for multiple skills")
    parser.add_argument("--update", action="store_true", help="Back up differing installed skills before replacing them")
    parser.add_argument("--dry-run", action="store_true", help="Check and print the plan without writing files")
    args = parser.parse_args()
    try:
        result = install(SOURCE, args.dest, args.names, args.update, args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Install failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
