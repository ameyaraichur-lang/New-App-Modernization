"""Install the analyzer CLIs into .tools/bin (no Homebrew required).

    python scripts/install_tools.py            # scc, syft, osv-scanner, gitleaks (+ semgrep via uv tool)

Downloads the latest GitHub release asset for this OS/arch. Re-running is a
no-op for tools already present. Missing tools only degrade the matching
agent evidence to NOT_ASSESSED — the pipeline never requires them.
"""

from __future__ import annotations

import io
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / ".tools" / "bin"

TOOLS = {
    # name: (repo, asset matcher tokens)
    "scc": ("boyter/scc", ["{os_cap}", "{arch_x}"]),
    "syft": ("anchore/syft", ["{os}", "{arch}", ".tar.gz"]),
    "osv-scanner": ("google/osv-scanner", ["{os}", "{arch}"]),
    "gitleaks": ("gitleaks/gitleaks", ["{os}", "{arch_x}", ".tar.gz"]),
}


def _plat() -> dict[str, str]:
    osn = {"darwin": "darwin", "linux": "linux"}[sys.platform if sys.platform != "darwin" else "darwin"]
    m = platform.machine().lower()
    arch = "arm64" if m in ("arm64", "aarch64") else "amd64"
    return {"os": osn, "os_cap": osn.capitalize(), "arch": arch,
            "arch_x": "arm64" if arch == "arm64" else "x86_64" if osn != "darwin" else "x64"}


def _latest_assets(repo: str) -> list[dict]:
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest",
                                 headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["assets"]


def _pick(assets: list[dict], tokens: list[str], p: dict[str, str]) -> dict | None:
    toks = [t.format(**p).lower() for t in tokens]
    alt = {"x64": ["x86_64", "amd64"], "x86_64": ["amd64", "x64"], "arm64": ["aarch64"]}
    for a in assets:
        name = a["name"].lower()
        if name.endswith((".sha256", ".sig", ".pem", ".sbom", ".json", ".txt", ".deb", ".rpm", ".apk")):
            continue
        if all(t in name or any(x in name for x in alt.get(t, [])) for t in toks):
            return a
    return None


def _extract(name: str, data: bytes, tool: str) -> bytes:
    if name.endswith((".tar.gz", ".tgz")):
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            for m in tf.getmembers():
                if m.isfile() and Path(m.name).name == tool:
                    return tf.extractfile(m).read()
    elif name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for n in zf.namelist():
                if Path(n).name == tool:
                    return zf.read(n)
    else:
        return data
    raise RuntimeError(f"{tool} binary not found in {name}")


# Asset-name templates used when the GitHub API is rate limited; {v} = tag without "v".
FALLBACK_ASSETS = {
    "scc": "scc_{os_cap}_{arch_x}.tar.gz",
    "syft": "syft_{v}_{os}_{arch}.tar.gz",
    "osv-scanner": "osv-scanner_{os}_{arch}",
    "gitleaks": "gitleaks_{v}_{os}_{arch_g}.tar.gz",
}


def _latest_tag(repo: str) -> str:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(f"https://github.com/{repo}/releases/latest", timeout=60)
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location", "")
        if "/tag/" in loc:
            return loc.rsplit("/tag/", 1)[1]
    raise RuntimeError(f"cannot resolve latest tag for {repo}")


def _fallback_asset(tool: str, repo: str, p: dict[str, str]) -> dict:
    tag = _latest_tag(repo)
    q = dict(p, v=tag.lstrip("v"), arch_g="arm64" if p["arch"] == "arm64" else "x64")
    if tool == "scc" and p["os"] == "darwin":
        q["arch_x"] = "arm64" if p["arch"] == "arm64" else "x86_64"
    name = FALLBACK_ASSETS[tool].format(**q)
    return {"name": name, "browser_download_url": f"https://github.com/{repo}/releases/download/{tag}/{name}"}


def install(tool: str) -> str:
    target = BIN / tool
    if target.exists():
        return f"{tool}: present"
    repo, tokens = TOOLS[tool]
    p = _plat()
    try:
        asset = _pick(_latest_assets(repo), tokens, p)
    except urllib.error.HTTPError:
        asset = _fallback_asset(tool, repo, p)
    if asset is None:
        return f"{tool}: no asset for {p}"
    with urllib.request.urlopen(asset["browser_download_url"], timeout=300) as r:
        data = r.read()
    target.write_bytes(_extract(asset["name"], data, tool))
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return f"{tool}: installed from {asset['name']}"


def main() -> None:
    BIN.mkdir(parents=True, exist_ok=True)
    for tool in TOOLS:
        try:
            print(install(tool), flush=True)
        except Exception as exc:  # keep installing the rest
            print(f"{tool}: FAILED {type(exc).__name__}: {exc}", flush=True)
    if shutil.which("semgrep") is None and shutil.which("uv"):
        r = subprocess.run(["uv", "tool", "install", "semgrep"], capture_output=True, text=True)
        print("semgrep:", "installed (uv tool)" if r.returncode == 0 else f"FAILED {r.stderr[-300:]}")
    else:
        print("semgrep:", "present" if shutil.which("semgrep") else "uv missing — skipped")
    os.environ["PATH"] = str(BIN) + os.pathsep + os.environ["PATH"]


if __name__ == "__main__":
    main()
