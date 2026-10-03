"""Deterministic repository intelligence tools (P1 foundation).

Evidence-first, mirroring the cursor-skill's source-file exclusions and
manifest knowledge. Nothing here calls a model: every fact is machine-checked
so downstream agents inherit OBSERVED/DOCUMENTED evidence, never invention.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

EXCLUDE_DIRS = {
    "vendor", "storage", ".nx", "tmp", ".cache", "target", "toolchains",
    "node_modules", ".git", "__pycache__", "dist", "build", ".venv", "obj",
    "bin", ".idea", ".vscode", "coverage", ".pytest_cache", "site-packages",
}
EXCLUDE_SUFFIXES = {
    ".sqlite", ".sqlite3", ".log", ".pyc", ".class", ".jar", ".war",
    ".zip", ".gz", ".7z", ".exe", ".dll", ".pdf", ".png", ".jpg", ".gif",
    ".ico", ".woff", ".woff2", ".ttf", ".eot", ".svg", ".min.js", ".map",
}

LANG_BY_EXT = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript", ".ts": "typescript",
    ".tsx": "typescript", ".java": "java", ".rb": "ruby", ".go": "go",
    ".php": "php", ".cs": "csharp", ".cshtml": "csharp", ".razor": "csharp",
    ".vb": "vb", ".sql": "sql", ".sh": "shell", ".ps1": "powershell",
    ".html": "html", ".htm": "html", ".css": "css", ".scss": "css",
    ".xml": "xml", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".cfg": "ini", ".ini": "ini", ".rst": "doc", ".md": "doc",
    ".txt": "doc", ".gradle": "gradle", ".kt": "kotlin", ".scala": "scala",
}

MANIFEST_FILES = [
    "setup.py", "setup.cfg", "pyproject.toml", "requirements.txt",
    "requirements-dev.txt", "dev-requirements.txt", "package.json",
    "pom.xml", "build.gradle", "build.gradle.kts", "go.mod", "Gemfile",
    "composer.json", "packages.config",
]

LICENSE_PATTERNS = [
    ("BSD", r"\bBSD\b|\bRedistribution and use in source and binary forms"),
    ("MIT", r"\bMIT\b|Permission is hereby granted, free of charge"),
    ("Apache-2.0", r"Apache License|ASL"),
    ("GPL", r"\bGNU General Public License|\bGPL\b"),
    ("LGPL", r"\bGNU Lesser General Public License|\bLGPL\b"),
    ("MPL", r"\bMozilla Public License|\bMPL\b"),
    ("ISC", r"\bISC\b"),
    ("EPL", r"\bEclipse Public License"),
]

SECRET_PATTERNS = [
    ("aws-access-key", r"AKIA[0-9A-Z]{16}"),
    ("private-key-block", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("password-assignment", r"""(?i)(password|passwd|pwd)\s*[:=]\s*['"][^'"]{6,}['"]"""),
    ("api-key-assignment", r"""(?i)(api[_-]?key|secret[_-]?key)\s*[:=]\s*['"][^'"]{8,}['"]"""),
]

ROUTE_PATTERNS = [
    ("flask", r"@\w+\.(?:get|post|put|delete|patch|route)\(\s*['\"]([^'\"]+)['\"]"),
    ("django-urls", r"""(?:path|re_path|url)\(\s*r?['"]([^'"]+)['"]"""),
    ("express", r"""(?:app|router)\.(?:get|post|put|delete|patch)\(\s*['"]([^'"]*)['"]"""),
    ("spring", r"""@(?:Request|Get|Post|Put|Delete|Patch)Mapping\((?:value\s*=\s*)?["']([^"']*)["']?"""),
    ("sinatra", r"""(?:get|post|put|delete|patch)\s+['"]([^'"]+)['"]\s+do"""),
    ("aspnet-controller", r"""Map(?:Controller)?Route\("""),
    ("go-http", r"""(?:http|\w+)\.HandleFunc\(\s*["'`]([^"'`]+)["'`]"""),
    ("go-chi", r"""[rRmM]\.(?:Get|Post|Put|Delete|Handle)\(\s*["']/([^"']*)["']?"""),
    ("php-route", r"""(?:Route::|\$app->)(?:get|post|put|delete|patch)\(\s*['"]([^'"]+)['"]"""),
]

UI_FRAMEWORK_HINTS = {
    "react": ("package.json", ["react"]),
    "vue": ("package.json", ["vue"]),
    "angular": ("package.json", ["@angular/core"]),
    "jquery": ("package.json", ["jquery"]),
    "flask-templates": ("flask", ["templates"]),
    "django-templates": ("django", ["templates"]),
    "erb-templates": ("rails", ["views"]),
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class RepoScan:
    root: Path
    files: list[dict[str, Any]] = field(default_factory=list)
    languages: dict[str, int] = field(default_factory=dict)   # lang -> LOC
    manifests: list[dict[str, Any]] = field(default_factory=list)
    license: dict[str, Any] = field(default_factory=dict)
    tests: list[str] = field(default_factory=list)
    templates: list[str] = field(default_factory=list)
    static_assets: list[str] = field(default_factory=list)
    routes: list[dict[str, str]] = field(default_factory=list)
    sql_files: list[str] = field(default_factory=list)
    model_files: list[str] = field(default_factory=list)
    migrations: list[str] = field(default_factory=list)
    infra_files: list[str] = field(default_factory=list)
    secret_findings: list[dict[str, str]] = field(default_factory=list)
    ui_frameworks: list[str] = field(default_factory=list)
    entry_candidates: list[str] = field(default_factory=list)
    commit: str = ""

    @property
    def loc(self) -> int:
        return sum(self.languages.values())

    def has_ui(self) -> bool:
        return bool(self.templates or self.ui_frameworks)

    def has_data_layer(self) -> bool:
        return bool(self.sql_files or self.model_files or self.migrations)


def scan_repo(root: Path, max_bytes: int = 1_000_000) -> RepoScan:
    root = Path(root).resolve()
    scan = RepoScan(root=root)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if path.suffix.lower() in EXCLUDE_SUFFIXES:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        lang = LANG_BY_EXT.get(path.suffix.lower(), "")
        rec = {
            "path": str(rel).replace("\\", "/"),
            "language": lang,
            "bytes": size,
        }
        scan.files.append(rec)

        if lang:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore") if size <= max_bytes else ""
            except OSError:
                text = ""
            if text:
                scan.languages[lang] = scan.languages.get(lang, 0) + text.count("\n") + 1
                _scan_text(scan, path, rel, text)

        name = path.name.lower()
        if name in MANIFEST_FILES or path.suffix.lower() in (".csproj",):
            scan.manifests.append({"path": str(rel).replace("\\", "/"),
                                   "sha256": _sha(path.read_bytes())})
        if name.startswith("dockerfile") or name in {
            "docker-compose.yml", "docker-compose.yaml", "jenkinsfile", "procfile",
        } or name.endswith(".tf") or name.endswith(".toml") and "workflow" in str(rel):
            scan.infra_files.append(str(rel).replace("\\", "/"))
        if ".github" in parts and "workflows" in parts:
            scan.infra_files.append(str(rel).replace("\\", "/"))
        if name.startswith("license") or name.startswith("copying") or name == "notice":
            _scan_license(scan, path, rel)
        if re.match(r"test_.*\.py$|.*_test\.go$|.*test\.java$|.*test\.cs$|.*_spec\.rb$|.*test\.js$|.*test\.ts$",
                    name) or "tests" in parts or "test" in parts:
            scan.tests.append(str(rel).replace("\\", "/"))
        if any(d.lower() in ("templates", "views") for d in parts) and path.suffix.lower() in (
            ".html", ".htm", ".jinja", ".j2", ".erb", ".hbs", ".cshtml", ".razor",
            ".jsp", ".twig", ".php",
        ):
            scan.templates.append(str(rel).replace("\\", "/"))
        if "static" in parts or "assets" in parts or "public" in parts:
            scan.static_assets.append(str(rel).replace("\\", "/"))
        if path.suffix.lower() == ".sql":
            scan.sql_files.append(str(rel).replace("\\", "/"))
        if re.match(r"models\.py$|model\.go$|.*models\.ts$", name) or "entities" in parts or "models" in parts:
            scan.model_files.append(str(rel).replace("\\", "/"))
        if "migrations" in parts or "migrate" in parts:
            scan.migrations.append(str(rel).replace("\\", "/"))
        if re.match(r"(app|main|manage|server|index|wsgi|asgi|program)\.(py|js|ts|go|rb|php|cs|java)$",
                    name):
            scan.entry_candidates.append(str(rel).replace("\\", "/"))

    _detect_ui_frameworks(scan)
    return scan


def _scan_text(scan: RepoScan, path: Path, rel: Path, text: str) -> None:
    rel_s = str(rel).replace("\\", "/")
    for kind, pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            scan.secret_findings.append({"file": rel_s, "kind": kind})
    if path.suffix.lower() in (".py", ".js", ".ts", ".java", ".rb", ".go", ".cs", ".php"):
        for framework, pattern in ROUTE_PATTERNS:
            for m in re.finditer(pattern, text):
                scan.routes.append({"file": rel_s, "framework": framework,
                                    "route": m.group(1) if m.groups() else ""})
    # ORM/model hints
    if re.search(r"class\s+\w+\s*\(\s*(models\.Model|db\.Model|Base\))", text):
        scan.model_files.append(rel_s)
    if re.search(r"SQLAlchemy|sqlalchemy|EntityFramework|Entity\(|ActiveRecord", text):
        scan.model_files.append(rel_s)


def _scan_license(scan: RepoScan, path: Path, rel: Path) -> None:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return
    for name, pattern in LICENSE_PATTERNS:
        if re.search(pattern, head):
            scan.license = {"file": str(rel).replace("\\", "/"), "type": name,
                            "evidence": "DOCUMENTED"}
            return
    scan.license = {"file": str(rel).replace("\\", "/"), "type": "UNKNOWN",
                    "evidence": "UNKNOWN"}


def _detect_ui_frameworks(scan: RepoScan) -> None:
    pkg = next((f for f in scan.files if f["path"] == "package.json"), None)
    if pkg:
        try:
            data = __import__("json").loads((scan.root / "package.json").read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for fw in ("react", "vue", "@angular/core", "jquery"):
                if fw in deps:
                    scan.ui_frameworks.append(fw)
        except Exception:
            pass
    if scan.templates:
        scan.ui_frameworks.append("server-templates")


def parse_dependencies(scan: RepoScan) -> list[dict[str, Any]]:
    """Best-effort dependency extraction from the manifests found (direct
    deps only; unknown/unparseable manifests become explicit gaps)."""
    deps: list[dict[str, Any]] = []
    gaps: list[str] = []
    for m in scan.manifests:
        p = scan.root / m["path"]
        name = p.name.lower()
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            gaps.append(m["path"])
            continue
        found: list[dict[str, Any]] = []
        if name == "requirements.txt":
            for line in text.splitlines():
                line = line.strip()
                if line and not line.startswith(("#", "-")):
                    pkg = re.split(r"[=<>!\[]", line)[0].strip()
                    if pkg:
                        found.append({"name": pkg, "source": m["path"]})
        elif name == "setup.py":
            for m2 in re.finditer(r"""install_requires\s*=\s*\[(.*?)\]""", text, re.S):
                for mm in re.finditer(r"""['"]([^'"]+)['"]""", m2.group(1)):
                    found.append({"name": mm.group(1), "source": m["path"]})
        elif name == "package.json":
            import json
            data = json.loads(text)
            for scope in ("dependencies", "devDependencies"):
                for k in data.get(scope, {}):
                    found.append({"name": k, "source": m["path"], "scope": scope})
        elif name == "pom.xml":
            for mm in re.finditer(r"<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>", text):
                found.append({"name": f"{mm.group(1)}:{mm.group(2)}", "source": m["path"]})
        elif name == "go.mod":
            for mm in re.finditer(r"^\s+([\w./-]+)\s+v[\w.-]+", text, re.M):
                found.append({"name": mm.group(1), "source": m["path"]})
        elif name == "gemfile":
            for mm in re.finditer(r"""gem\s+['"]([^'"]+)['"]""", text):
                found.append({"name": mm.group(1), "source": m["path"]})
        elif name == "composer.json":
            import json
            data = json.loads(text)
            for scope in ("require", "require-dev"):
                for k in data.get(scope, {}):
                    found.append({"name": k, "source": m["path"]})
        if found:
            deps.extend(found)
        elif name not in ("setup.cfg",):  # setup.cfg often metadata-only
            gaps.append(m["path"])
    for d in deps:
        d["evidence"] = "DOCUMENTED"
    return deps
