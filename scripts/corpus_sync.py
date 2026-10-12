"""Clone or verify the evaluation corpus pinned in evals/corpus.json.

    python scripts/corpus_sync.py                 # clone missing repos at their pinned commit
    python scripts/corpus_sync.py --verify        # check every repo is present at its pin
    python scripts/corpus_sync.py --split holdout --names   # print repo names (for --repos)

Repos land in ../corpus/<name> (override with --dir or APPMOD_CORPUS). A repo with `subdir`
is stored as a one-commit snapshot of that subdirectory whose message names the upstream
commit. Licence files found in each checkout are reported so `license: unverified` entries
can be resolved by reading them.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evals" / "corpus.json"


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout.strip()


def fetch_at(url: str, commit: str, dest: Path) -> None:
    dest.mkdir(parents=True)
    git("init", "-q", cwd=dest)
    git("remote", "add", "origin", url, cwd=dest)
    git("fetch", "-q", "--depth", "1", "origin", commit, cwd=dest)
    git("-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD", cwd=dest)


def snapshot_message(e: dict[str, Any]) -> str:
    repo = e["url"].removeprefix("https://github.com/").removesuffix(".git")
    return f"{e['subdir']} snapshot from {repo}@{e['commit']}"


def sync(e: dict[str, Any], dest: Path) -> str:
    if dest.exists():
        return "present"
    if "subdir" not in e:
        fetch_at(e["url"], e["commit"], dest)
        return "cloned"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src"
        fetch_at(e["url"], e["commit"], src)
        shutil.copytree(src / e["subdir"], dest)
    git("init", "-q", cwd=dest)
    git("add", "-A", cwd=dest)
    git("-c", "user.name=corpus-sync", "-c", "user.email=corpus-sync@localhost",
        "commit", "-q", "-m", snapshot_message(e), cwd=dest)
    return "snapshot"


def verify(e: dict[str, Any], dest: Path) -> str | None:
    """Return a problem description, or None when the checkout matches its pin."""
    if not (dest / ".git").exists():
        return "missing"
    if "subdir" in e:
        msg = git("log", "-1", "--format=%s", cwd=dest)
        short = e["commit"][:7]
        return None if e["commit"] in msg or f"@{short}" in msg else f"snapshot is not of {short}: {msg!r}"
    head = git("rev-parse", "HEAD", cwd=dest)
    if head != e["commit"]:
        return f"HEAD {head[:12]} != pinned {e['commit'][:12]}"
    return None


def licence_files(dest: Path) -> list[str]:
    if not dest.exists():
        return []
    return sorted(p.name for p in dest.iterdir()
                  if p.is_file() and p.name.lower().startswith(("licen", "copying")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path,
                    default=Path(os.environ.get("APPMOD_CORPUS", ROOT.parent / "corpus")))
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--split", choices=["tune", "holdout"])
    ap.add_argument("--names", action="store_true", help="print repo names and exit")
    args = ap.parse_args()
    repos = [e for e in json.loads(MANIFEST.read_text())["repos"]
             if args.split is None or e["split"] == args.split]
    if args.names:
        print(" ".join(e["name"] for e in repos))
        return 0
    problems = 0
    for e in repos:
        dest = args.dir / e["name"]
        if args.verify:
            problem = verify(e, dest)
            problems += problem is not None
            status = problem or "ok"
        else:
            try:
                status = sync(e, dest)
            except subprocess.CalledProcessError as exc:
                problems += 1
                status = f"FAILED: {exc.stderr.strip()[:200]}"
        print(f"{e['name']:<36} {e['split']:<8} {e['license']:<14} {status} "
              f"{','.join(licence_files(dest)) or '(no licence file)'}")
    print(f"{len(repos) - problems}/{len(repos)} ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
