"""Hierarchical repository map, cached by content hash, with a retrieval budget.

Agents on a large repository start from module summaries instead of walking the tree.
A clean git checkout is identified by its commit: module hashes come from ``git ls-tree``
blob ids, so an unchanged module is not reread. A dirty or non-git tree is hashed from
file bytes. The run-4 median agent input was 49,656 tokens; the live budget is twice that.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

RUN4_MEDIAN_INPUT_TOKENS = 49_656
AGENT_INPUT_TOKEN_CAP = 2 * RUN4_MEDIAN_INPUT_TOKENS
MAP_BUDGET_CHARS = 4_000
MEMORY_VERSION = "repo-memory/1"

SKIP_DIRS = {".git", "node_modules", "vendor", "target", "build", "dist", ".idea",
             "__pycache__", ".gradle", ".mvn"}
MANIFESTS = {"pom.xml", "build.gradle", "build.gradle.kts", "package.json", "go.mod",
             "requirements.txt", "pyproject.toml", "composer.json", "gemfile", "cargo.toml",
             "web.xml", "application.yml", "application.properties"}


def _git(root: Path, args: list[str]) -> str | None:
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                              timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def _commit_if_clean(root: Path) -> str | None:
    commit = _git(root, ["rev-parse", "HEAD"])
    status = _git(root, ["status", "--porcelain"])
    if commit and status is not None and not status.strip():
        return commit.strip()
    return None


def _blobs_git(root: Path) -> list[tuple[str, str]] | None:
    raw = _git(root, ["ls-tree", "-r", "HEAD"])
    if raw is None:
        return None
    out: list[tuple[str, str]] = []
    for line in raw.splitlines():
        meta, _, path = line.partition("\t")
        if not path or any(part in SKIP_DIRS for part in Path(path).parts):
            continue
        blob = meta.split()[-1] if meta.split() else ""
        if blob:
            out.append((path, blob))
    return out


def _blobs_files(root: Path) -> list[tuple[str, str]]:
    from appmod.tools.gateway import path_under_root
    root = root.resolve()
    out: list[tuple[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        current = Path(dirpath)
        if not path_under_root(root, current):
            dirnames[:] = []
            continue
        for name in sorted(filenames):
            path = current / name
            if not path_under_root(root, path):
                continue
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
            out.append((str(path.relative_to(root)), digest))
    return out


def _module_of(path: str) -> str:
    parts = Path(path).parts
    return parts[0] if len(parts) > 1 else "."


def _summarize(blobs: list[tuple[str, str]]) -> dict[str, Any]:
    modules: dict[str, dict[str, Any]] = {}
    for path, blob in blobs:
        module = _module_of(path)
        slot = modules.setdefault(module, {"files": 0, "langs": {}, "children": {},
                                            "manifests": [], "lines": []})
        slot["files"] += 1
        slot["lines"].append(f"{blob} {path}")
        suffix = Path(path).suffix.lower().lstrip(".") or "(none)"
        slot["langs"][suffix] = slot["langs"].get(suffix, 0) + 1
        parts = Path(path).parts
        if len(parts) > 2:
            slot["children"][parts[1]] = slot["children"].get(parts[1], 0) + 1
        if Path(path).name.lower() in MANIFESTS and len(slot["manifests"]) < 8:
            slot["manifests"].append(path)
    result = []
    for name, slot in sorted(modules.items()):
        digest = hashlib.sha256("\n".join(sorted(slot["lines"])).encode()).hexdigest()
        langs = sorted(slot["langs"], key=lambda k: (-slot["langs"][k], k))[:4]
        children = sorted(slot["children"], key=lambda k: (-slot["children"][k], k))[:12]
        result.append({"module": name, "files": slot["files"], "content_hash": digest[:16],
                       "languages": langs, "children": children, "manifests": slot["manifests"]})
    whole = hashlib.sha256("".join(m["content_hash"] for m in result).encode()).hexdigest()[:16]
    return {"modules": result, "content_hash": whole, "files": sum(m["files"] for m in result)}


def repo_map(root: Path, *, cache_dir: Path | None = None) -> dict[str, Any]:
    """Module summaries for ``root``. A matching content hash is served from ``cache_dir``."""
    root = Path(root)
    if cache_dir is None:
        from appmod.config import get_settings
        cache_dir = get_settings().runs_dir / "memory"
    cache_dir.mkdir(parents=True, exist_ok=True)
    commit = _commit_if_clean(root)
    key = commit or "dirty"
    cache = cache_dir / f"{hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:16]}-{key[:16]}.json"
    if commit and cache.is_file():
        stored = json.loads(cache.read_text())
        stored["cached"] = True
        return stored
    blobs = _blobs_git(root) if commit else None
    if blobs is None:
        blobs = _blobs_files(root)
    summary = _summarize(blobs)
    summary["commit"] = commit
    summary["version"] = MEMORY_VERSION
    summary["cached"] = False
    if commit:
        cache.write_text(json.dumps(summary))
    return summary


def map_text(root: Path, budget_chars: int = MAP_BUDGET_CHARS, *,
             cache_dir: Path | None = None) -> str:
    """Bounded text form of the map. Never raises; a failure becomes one line."""
    try:
        data = repo_map(root, cache_dir=cache_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return f"(repository map unavailable: {type(exc).__name__})"
    lines = [f"# Repository map {data['content_hash']} ({data['files']} files, "
             f"{'cached' if data.get('cached') else 'built'})"]
    for module in data["modules"]:
        line = (f"- {module['module']}: {module['files']} files, "
                f"{'/'.join(module['languages']) or 'unknown'}, hash {module['content_hash']}")
        if module["children"]:
            line += "; children " + ", ".join(module["children"])
        if module["manifests"]:
            line += "; manifests " + ", ".join(module["manifests"][:3])
        if sum(len(x) + 1 for x in lines) + len(line) > budget_chars:
            lines.append(f"...[{len(data['modules']) - (len(lines) - 1)} modules omitted; "
                         "call repo_map for one module]")
            break
        lines.append(line)
    return "\n".join(lines)[:budget_chars]
