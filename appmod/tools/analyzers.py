"""External static analyzers (scc, syft, osv-scanner, gitleaks, semgrep).

Each adapter returns a normalized dict ``{"tool", "version", "status", ...}``
where status is ``OK`` | ``UNAVAILABLE`` | ``ERROR`` | ``TIMEOUT``. A missing
binary never fails the pipeline: callers turn non-OK into NOT_ASSESSED gaps.
Results are cached on disk per (tool, repo, commit|tree fingerprint).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Any, Callable

from appmod.config import get_settings

_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def _bin(name: str) -> str | None:
    s = get_settings()
    local = s.tools_dir / name
    return str(local) if local.exists() else shutil.which(name)


def tool_version(name: str) -> str | None:
    exe = _bin(name)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=30)
        line = (out.stdout or out.stderr).strip().splitlines()
        return line[0][:80] if line else "unknown"
    except (OSError, subprocess.SubprocessError):
        return None


def _fingerprint(root: Path) -> str:
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                               capture_output=True, text=True, timeout=30)
        if head.returncode == 0:
            return head.stdout.strip() + hashlib.sha1(dirty.stdout.encode()).hexdigest()[:8]
    except (OSError, subprocess.SubprocessError):
        pass
    h = hashlib.sha1()
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts:
            st = p.stat()
            h.update(f"{p.relative_to(root)}:{st.st_size}:{int(st.st_mtime)}".encode())
    return h.hexdigest()


def _cached(tool: str, root: Path, fn: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    root = Path(root).resolve()
    key = hashlib.sha256(f"{tool}|{root}|{_fingerprint(root)}".encode()).hexdigest()[:32]
    path = get_settings().runs_dir / "analyzer_cache" / f"{tool}-{key}.json"
    with _locks_guard:
        lock = _locks.setdefault(key, threading.Lock())
    with lock:
        if path.exists():
            return json.loads(path.read_text())
        result = fn()
        if result.get("status") in ("OK",):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result))
        return result


def _run(cmd: list[str], timeout: int, cwd: Path | None = None,
         ok_codes: tuple[int, ...] = (0,)) -> tuple[str, dict[str, Any] | None]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired:
        return "", {"status": "TIMEOUT", "detail": f"exceeded {timeout}s"}
    except OSError as exc:
        return "", {"status": "ERROR", "detail": str(exc)}
    if p.returncode not in ok_codes:
        return p.stdout, {"status": "ERROR", "detail": (p.stderr or p.stdout)[-600:]}
    return p.stdout, None


def _unavailable(tool: str) -> dict[str, Any]:
    return {"tool": tool, "status": "UNAVAILABLE",
            "detail": f"{tool} not installed (scripts/install_tools.py)"}


# -- adapters ------------------------------------------------------------------


def loc_metrics(root: Path) -> dict[str, Any]:
    exe = _bin("scc")
    if not exe:
        return _unavailable("scc")

    def go():
        out, err = _run([exe, "-f", "json", "--no-cocomo", str(root)], 120)
        if err:
            return {"tool": "scc", **err}
        langs = [{"language": d["Name"], "files": d["Count"], "code": d["Code"],
                  "comment": d["Comment"], "blank": d["Blank"], "complexity": d["Complexity"]}
                 for d in json.loads(out or "[]")]
        langs.sort(key=lambda x: -x["code"])
        return {"tool": "scc", "version": tool_version("scc"), "status": "OK", "languages": langs,
                "total_code": sum(x["code"] for x in langs),
                "total_complexity": sum(x["complexity"] for x in langs)}
    return _cached("scc", root, go)


def sbom(root: Path) -> dict[str, Any]:
    exe = _bin("syft")
    if not exe:
        return _unavailable("syft")

    def go():
        out, err = _run([exe, f"dir:{root}", "-o", "syft-json", "-q"], 300)
        if err:
            return {"tool": "syft", **err}
        d = json.loads(out or "{}")
        pkgs = []
        for a in d.get("artifacts", []):
            lic = [x.get("value") if isinstance(x, dict) else x for x in a.get("licenses", [])]
            pkgs.append({"name": a.get("name"), "version": a.get("version"), "type": a.get("type"),
                         "purl": a.get("purl"), "licenses": [x for x in lic if x][:3]})
        by_type: dict[str, int] = {}
        for p in pkgs:
            by_type[p["type"]] = by_type.get(p["type"], 0) + 1
        return {"tool": "syft", "version": tool_version("syft"), "status": "OK",
                "format": "syft-json", "package_count": len(pkgs), "by_type": by_type,
                "packages": pkgs[:400]}
    return _cached("syft", root, go)


def vulnerabilities(root: Path) -> dict[str, Any]:
    exe = _bin("osv-scanner")
    if not exe:
        return _unavailable("osv-scanner")

    def go():
        out, err = _run([exe, "scan", "source", "-r", "--format", "json", str(root)], 900,
                        ok_codes=(0, 1, 128))
        if err:
            return {"tool": "osv-scanner", **err}
        try:
            d = json.loads(out or "{}")
        except json.JSONDecodeError:
            return {"tool": "osv-scanner", "status": "OK", "version": tool_version("osv-scanner"),
                    "packages_scanned": 0, "vulnerabilities": [], "note": "no supported manifests"}
        vulns = []
        for r in d.get("results", []):
            src = r.get("source", {}).get("path", "")
            for p in r.get("packages", []):
                sev = {g.get("ids", [""])[0]: g.get("max_severity") for g in p.get("groups", [])}
                for v in p.get("vulnerabilities", []):
                    vulns.append({
                        "id": v.get("id"), "aliases": v.get("aliases", [])[:3],
                        "package": p["package"].get("name"), "version": p["package"].get("version"),
                        "ecosystem": p["package"].get("ecosystem"),
                        "severity": sev.get(v.get("id")) or "",
                        "summary": (v.get("summary") or "")[:200],
                        "manifest": str(Path(src).relative_to(root)) if src.startswith(str(root)) else src,
                    })
        return {"tool": "osv-scanner", "version": tool_version("osv-scanner"), "status": "OK",
                "vulnerability_count": len(vulns), "vulnerabilities": vulns[:300]}
    return _cached("osv", root, go)


def secrets(root: Path) -> dict[str, Any]:
    exe = _bin("gitleaks")
    if not exe:
        return _unavailable("gitleaks")

    def go():
        out, err = _run([exe, "dir", str(root), "--report-format", "json", "--report-path", "-",
                         "--redact", "--no-banner", "--exit-code", "0", "--log-level", "error"], 300)
        if err:
            return {"tool": "gitleaks", **err}
        try:
            items = json.loads(out or "[]")
        except json.JSONDecodeError:
            items = []
        leaks = [{"rule": i.get("RuleID"), "file": str(Path(i.get("File", "")).relative_to(root))
                  if str(i.get("File", "")).startswith(str(root)) else i.get("File"),
                  "line": i.get("StartLine"), "description": i.get("Description")} for i in items]
        return {"tool": "gitleaks", "version": tool_version("gitleaks"), "status": "OK",
                "finding_count": len(leaks), "findings": leaks[:200], "values": "redacted"}
    return _cached("gitleaks", root, go)


def static_analysis(root: Path) -> dict[str, Any]:
    exe = _bin("semgrep")
    if not exe:
        return _unavailable("semgrep")

    def go():
        out, err = _run([exe, "scan", "--config", "p/default", "--json", "--metrics", "off",
                         "--quiet", "--timeout", "20", "--max-target-bytes", "500000", str(root)],
                        900, ok_codes=(0, 1))
        if err:
            return {"tool": "semgrep", **err}
        d = json.loads(out or "{}")
        res = []
        for r in d.get("results", []):
            path = r.get("path", "")
            res.append({"rule": r.get("check_id", "").split(".")[-1], "check_id": r.get("check_id"),
                        "path": str(Path(path).relative_to(root)) if path.startswith(str(root)) else path,
                        "line": r.get("start", {}).get("line"),
                        "severity": r.get("extra", {}).get("severity"),
                        "message": (r.get("extra", {}).get("message") or "")[:240]})
        return {"tool": "semgrep", "version": tool_version("semgrep"), "status": "OK",
                "ruleset": "p/default", "finding_count": len(res), "findings": res[:200],
                "errors": len(d.get("errors", []))}
    return _cached("semgrep", root, go)


ANALYZERS = {"scc": loc_metrics, "syft": sbom, "osv-scanner": vulnerabilities,
             "gitleaks": secrets, "semgrep": static_analysis}


def doctor() -> dict[str, Any]:
    tools = {name: {"available": _bin(name) is not None, "version": tool_version(name)}
             for name in ANALYZERS}
    return {"tools": tools, "tools_dir": str(get_settings().tools_dir)}
