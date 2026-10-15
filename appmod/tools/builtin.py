"""Builtin read-only tools exposed to agents through the gateway.

All schemas are Azure strict-mode compatible: every property is required,
optional values are nullable, ``additionalProperties`` is false.
"""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import threading
from pathlib import Path
from typing import Any

from appmod.tools import analyzers
from appmod.tools.gateway import ToolDef, ToolEnv, ToolGateway, safe_path
from appmod.tools.repo_intel import parse_dependencies, scan_repo

_scan_cache: dict[str, Any] = {}
_scan_lock = threading.Lock()


def _obj(props: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "properties": props, "required": list(props),
            "additionalProperties": False}


APP = {"type": ["string", "null"],
       "description": "Application id (portfolio phases); null = the current application."}


def _root(env: ToolEnv, app: str | None) -> Path:
    if app and app in env.repo_roots:
        return Path(env.repo_roots[app])
    if app and env.repo_roots and app not in env.repo_roots and app != env.application_id:
        raise KeyError(f"unknown application '{app}'; known: {sorted(env.repo_roots)}")
    if env.repo_root is not None:
        return Path(env.repo_root)
    if len(env.repo_roots) == 1:
        return Path(next(iter(env.repo_roots.values())))
    raise ValueError("application_id required: " + ", ".join(sorted(env.repo_roots)))


def _scan(root: Path):
    key = str(root.resolve())
    with _scan_lock:
        if key not in _scan_cache:
            _scan_cache[key] = scan_repo(root)
        return _scan_cache[key]


# -- repository tools ----------------------------------------------------------


def repo_summary(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    root = _root(env, a.get("application_id"))
    s = _scan(root)
    return {
        "repo": root.name, "commit": s.commit, "files": len(s.files), "loc": s.loc,
        "code_loc": s.code_loc, "primary_language": s.primary_language,
        "languages": dict(sorted(s.languages.items(), key=lambda kv: -kv[1])),
        "manifests": [m.get("path") for m in s.manifests][:30],
        "entry_candidates": s.entry_candidates[:15], "infra_files": s.infra_files[:30],
        "test_files": len(s.tests), "templates": len(s.templates), "routes": len(s.routes),
        "frameworks": getattr(s, "ui_frameworks", []),
        "license": s.license or {"type": "NONE"},
        "top_dirs": sorted({f["path"].split("/")[0] for f in s.files})[:40],
    }


def list_dir(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    root = _root(env, a.get("application_id"))
    p = safe_path(root, a.get("path") or ".")
    if not p.is_dir():
        raise FileNotFoundError(f"{a.get('path')} is not a directory")
    entries = []
    for c in sorted(p.iterdir())[:300]:
        if c.name == ".git":
            continue
        entries.append({"name": c.name + ("/" if c.is_dir() else ""),
                        "bytes": c.stat().st_size if c.is_file() else None})
    return {"path": str(p.relative_to(root.resolve())) or ".", "entries": entries}


def read_file(env: ToolEnv, a: dict[str, Any]) -> str:
    root = _root(env, a.get("application_id"))
    p = safe_path(root, a["path"])
    if not p.is_file():
        raise FileNotFoundError(a["path"])
    if p.stat().st_size > 2_000_000:
        raise ValueError("file larger than 2MB; use grep")
    if b"\x00" in p.read_bytes()[:8192]:
        raise ValueError("binary file; not readable as text")
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(1, int(a.get("start_line") or 1))
    end = min(len(lines), int(a.get("end_line") or start + 299), start + 399)
    body = "\n".join(f"{i:>5}| {lines[i - 1]}" for i in range(start, end + 1))
    return f"{a['path']} lines {start}-{end} of {len(lines)}\n{body}"


def grep(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    root = _root(env, a.get("application_id"))
    s = _scan(root)
    try:
        rx = re.compile(a["pattern"], re.I)
    except re.error as exc:
        raise ValueError(f"invalid regex: {exc}") from exc
    glob = a.get("glob") or "*"
    limit = min(int(a.get("max_results") or 60), 150)
    hits = []
    for f in s.files:
        if not fnmatch.fnmatch(f["path"], glob) and not fnmatch.fnmatch(Path(f["path"]).name, glob):
            continue
        try:
            text = safe_path(root, f["path"]).read_text(encoding="utf-8", errors="ignore")
        except (OSError, PermissionError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                hits.append(f"{f['path']}:{i}: {line.strip()[:200]}")
                if len(hits) >= limit:
                    return {"matches": hits, "truncated": True}
    return {"matches": hits, "truncated": False}


def list_dependencies(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    s = _scan(_root(env, a.get("application_id")))
    deps = parse_dependencies(s)
    return {"count": len(deps), "dependencies": deps[:300]}


def git_log(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    root = _root(env, a.get("application_id"))
    n = min(int(a.get("max_count") or 20), 100)
    p = subprocess.run(["git", "-C", str(root), "log", f"-{n}", "--date=short",
                        "--pretty=format:%h|%ad|%s"], capture_output=True, text=True, timeout=30)
    commits = [dict(zip(("hash", "date", "subject"), line.split("|", 2)))
               for line in p.stdout.splitlines() if line]
    note = "shallow clone: history truncated" if len(commits) <= 1 else None
    return {"commits": commits, "note": note}


def search_code(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    from appmod.retrieval import get_index
    root = _root(env, a.get("application_id"))
    idx = get_index(root)
    k = min(int(a.get("k") or 8), 20)
    return {"query": a["query"], "results": idx.search(a["query"], k)}


def app_similarity(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    from appmod.retrieval import app_similarity as sim
    roots = dict(env.repo_roots)
    if len(roots) < 2:
        raise ValueError("app_similarity needs a portfolio with at least two applications")
    return sim(roots)


# -- policy-gated HTTP tools -----------------------------------------------------

EOL_HOST = "endoflife.date"
EOL_CACHE_TTL_S = 7 * 24 * 3600


def eol_lookup(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    import datetime
    import re
    import time

    import httpx

    from appmod.config import get_settings
    s = get_settings()
    hosts = {h.strip() for h in s.http_hosts.split(",") if h.strip()}
    if s.http_tools != "on" or EOL_HOST not in hosts:
        raise PermissionError(f"outbound HTTP to {EOL_HOST} is not allowed by policy")
    product = (a.get("product") or "").strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9.+-]{0,60}", product):
        raise ValueError("product must be an endoflife.date slug such as 'spring-boot', 'python', 'nodejs'")
    cache = s.runs_dir / "http_cache" / "endoflife" / f"{product}.json"
    data = None
    if cache.is_file() and time.time() - cache.stat().st_mtime < EOL_CACHE_TTL_S:
        data = json.loads(cache.read_text())
    if data is None:
        try:
            r = httpx.get(f"https://{EOL_HOST}/api/{product}.json", timeout=10, follow_redirects=False)
        except httpx.HTTPError as exc:
            raise ValueError(f"{EOL_HOST} unavailable: {type(exc).__name__}") from exc
        if r.status_code == 404:
            raise ValueError(f"unknown product '{product}' on {EOL_HOST}")
        r.raise_for_status()
        data = r.json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data))
    today = datetime.date.today().isoformat()

    def is_eol(c: dict[str, Any]) -> bool | None:
        e = c.get("eol")
        return e if isinstance(e, bool) else (str(e) <= today if e else None)

    cycles = [{"cycle": str(c.get("cycle")), "release": c.get("releaseDate"), "eol": c.get("eol"),
               "latest": c.get("latest"), "lts": c.get("lts"), "is_eol": is_eol(c)} for c in data]
    version = (a.get("version") or "").strip()
    match = None
    if version:
        cands = [c for c in cycles if version == c["cycle"] or version.startswith(c["cycle"] + ".")]
        match = max(cands, key=lambda c: len(c["cycle"]), default=None)
    return {"product": product, "source": f"https://{EOL_HOST}/api/{product}.json", "as_of": today,
            "version": version or None, "match": match,
            "supported_cycles": [c for c in cycles if c["is_eol"] is False][:6]}


# -- artifact tools ------------------------------------------------------------


def _dig(obj: Any, path: str | None) -> Any:
    if not path:
        return obj
    for part in path.split("."):
        if isinstance(obj, dict):
            obj = obj.get(part)
        elif isinstance(obj, list) and part.isdigit():
            obj = obj[int(part)] if int(part) < len(obj) else None
        else:
            return None
    return obj


def get_artifact(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    aid = a["artifact_id"].strip()
    art = None
    if "/" not in aid:
        art = env.published.get(aid)
        if art is None:
            aid = f"P{env.phase}/{env.application_id}/{aid}"
    if art is None:
        if env.store is None:
            raise KeyError(aid)
        try:
            art = env.store.get(aid)
        except Exception as exc:
            raise KeyError(f"artifact {aid} not found") from exc
    if a.get("field"):
        return {"artifact_id": art["artifact_id"], "version": art["artifact_version"], "field": a["field"],
                "value": _dig(art.get("payload", {}), a["field"])}
    return {"artifact_id": art["artifact_id"], "version": art["artifact_version"],
            "status": art["status"], "payload": art.get("payload"),
            "findings": art.get("findings", [])[:40], "gaps": art.get("gaps", [])[:20]}


def list_artifacts(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
    out = [{"node": n, "artifact_id": x["artifact_id"], "status": x["status"]}
           for n, x in sorted(env.published.items())]
    phase = a.get("phase")
    if env.store is not None and phase:
        apps = env.portfolio_apps or [env.application_id]
        for ptr in env.store.query(phase_id=int(phase)):
            if ptr["application_id"] in apps or ptr["application_id"].startswith("PF"):
                out.append({"artifact_id": ptr["artifact_id"], "version": ptr["artifact_version"],
                            "status": ptr["status"]})
    return {"artifacts": out[:200]}


# -- analyzer tools ------------------------------------------------------------


def _analyzer(fn):
    def run(env: ToolEnv, a: dict[str, Any]) -> dict[str, Any]:
        return fn(_root(env, a.get("application_id")))
    return run


def build_gateway() -> ToolGateway:
    gw = ToolGateway()
    P = _obj
    gw.register(ToolDef("repo_summary", "Repository facts: languages, LOC, manifests, entry points, "
                        "infra files, tests, routes, license, commit.", P({"application_id": APP}),
                        repo_summary, needs_repo=True))
    gw.register(ToolDef("list_dir", "List a directory inside the repository.",
                        P({"application_id": APP, "path": {"type": "string"}}), list_dir, needs_repo=True))
    gw.register(ToolDef("read_file", "Read lines of a repository file (max 400 lines per call).",
                        P({"application_id": APP, "path": {"type": "string"},
                           "start_line": {"type": ["integer", "null"]},
                           "end_line": {"type": ["integer", "null"]}}), read_file, needs_repo=True))
    gw.register(ToolDef("grep", "Regex search across repository text files; glob filters paths "
                        "(e.g. '*.java', 'src/**').",
                        P({"application_id": APP, "pattern": {"type": "string"},
                           "glob": {"type": ["string", "null"]},
                           "max_results": {"type": ["integer", "null"]}}), grep, needs_repo=True))
    gw.register(ToolDef("list_dependencies", "Declared dependencies parsed from manifests.",
                        P({"application_id": APP}), list_dependencies, needs_repo=True))
    gw.register(ToolDef("git_log", "Recent commits (hash, date, subject).",
                        P({"application_id": APP, "max_count": {"type": ["integer", "null"]}}),
                        git_log, needs_repo=True))
    gw.register(ToolDef("search_code", "Semantic code search (embeddings) — returns the most "
                        "relevant code chunks for a natural-language query.",
                        P({"application_id": APP, "query": {"type": "string"},
                           "k": {"type": ["integer", "null"]}}), search_code, needs_repo=True))
    gw.register(ToolDef("app_similarity", "Pairwise code similarity across the portfolio from code "
                        "embeddings: near-duplicate chunk overlap, whole-app centroid cosine and the "
                        "closest chunk pairs.", P({}), app_similarity, needs_repo=True))
    gw.register(ToolDef("eol_lookup", "endoflife.date facts for a product (policy-gated HTTP): "
                        "release cycles, end-of-life dates, latest versions; with a version, the "
                        "matching cycle and whether it is end-of-life.",
                        P({"product": {"type": "string"}, "version": {"type": ["string", "null"]}}),
                        eol_lookup))
    gw.register(ToolDef("get_artifact", "Read a published pipeline artifact. artifact_id is a node "
                        "of the current phase (e.g. 'A1', 'G1') or a full id like 'P1/<app>/A3'. "
                        "field is an optional dotted payload path.",
                        P({"artifact_id": {"type": "string"}, "field": {"type": ["string", "null"]}}),
                        get_artifact))
    gw.register(ToolDef("list_artifacts", "List artifacts published in this run (and optionally "
                        "a prior phase).", P({"phase": {"type": ["integer", "null"]}}), list_artifacts))
    for name, fn, desc in (
        ("loc_metrics", analyzers.loc_metrics, "scc: per-language code/comment/blank lines and "
         "cyclomatic complexity."),
        ("sbom_packages", analyzers.sbom, "syft: software bill of materials (packages, versions, "
         "licenses)."),
        ("vulnerability_scan", analyzers.vulnerabilities, "osv-scanner: known vulnerabilities in "
         "declared and resolved dependencies."),
        ("secret_scan", analyzers.secrets, "gitleaks: hardcoded secret findings (values redacted)."),
        ("static_analysis", analyzers.static_analysis, "semgrep p/default: code security and "
         "correctness findings."),
    ):
        gw.register(ToolDef(name, desc, P({"application_id": APP}), _analyzer(fn), needs_repo=True))
    return gw


REPO_TOOLS = ["repo_summary", "list_dir", "read_file", "grep", "list_dependencies", "git_log",
              "search_code"]
ARTIFACT_TOOLS = ["get_artifact", "list_artifacts"]
ANALYZER_TOOLS = ["loc_metrics", "sbom_packages", "vulnerability_scan", "secret_scan",
                  "static_analysis"]


def tool_catalog() -> list[dict[str, Any]]:
    return [{"name": t.name, "description": t.description, "needs_repo": t.needs_repo}
            for t in build_gateway().tools.values()]


if __name__ == "__main__":
    print(json.dumps(tool_catalog(), indent=2))
