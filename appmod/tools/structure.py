"""Deterministic structure analyzers for portfolio and architecture agents.

Read-only, offline parsers over repository snapshots. Outputs are compact JSON
suitable for evidence citation (bounded size; no external tools required).
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import threading
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from appmod.tools.gateway import safe_path
from appmod.tools.repo_intel import CODE_LANGUAGES, EXCLUDE_DIRS, scan_repo

MAX_COMMITS = 2000
MAX_FILES_PER_COMMIT = 120
MAX_COUPLED_PAIRS = 80
MAX_HOTSPOTS = 40
MAX_TABLES = 120
MAX_ENDPOINTS = 200
MAX_GRAPH_NODES = 150
MAX_GRAPH_EDGES = 400
MAX_CYCLES = 20
MAX_IMPORT_FILES = 1200
MAX_IMPORT_BYTES = 48_000
IMPORT_SCAN_BYTES = 20_000
LARGE_REPO_LOC = 150_000

_scan_cache: dict[str, Any] = {}
_scan_lock = threading.Lock()


def _cached_scan(root: Path):
    key = str(Path(root).resolve())
    with _scan_lock:
        if key not in _scan_cache:
            _scan_cache[key] = scan_repo(Path(root))
        return _scan_cache[key]

IMPORT_RES = {
    "python": [
        (re.compile(r"^\s*import\s+([\w.]+)"), 1),
        (re.compile(r"^\s*from\s+([\w.]+)\s+import"), 1),
    ],
    "javascript": [
        (re.compile(r"""import\s+.*?from\s+['"]([^'"]+)['"]"""), 1),
        (re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)"""), 1),
    ],
    "typescript": [
        (re.compile(r"""import\s+.*?from\s+['"]([^'"]+)['"]"""), 1),
        (re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)"""), 1),
    ],
    "java": [(re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+)\s*;"), 1)],
    "go": [(re.compile(r'^\s*"([^"]+)"', re.M), 1)],  # inside import blocks — refined below
    "csharp": [(re.compile(r"^\s*using\s+([\w.]+)\s*;"), 1)],
    "php": [
        (re.compile(r"""^\s*use\s+([\w\\]+)\s*;"""), 1),
        (re.compile(r"""(?:require|include)(?:_once)?\s*\(?\s*['"]([^'"]+)['"]"""), 1),
    ],
    "ruby": [(re.compile(r"""^\s*require(?:_relative)?\s+['"]([^'"]+)['"]"""), 1)],
}

GO_IMPORT_BLOCK = re.compile(r"import\s+(?:\(\s*([\s\S]*?)\s*\)|(\S+))")
JAVA_PKG = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.M)
CS_NAMESPACE = re.compile(r"^\s*namespace\s+([\w.]+)", re.M)
PHP_NAMESPACE = re.compile(r"^\s*namespace\s+([\w\\]+)\s*;", re.M)

CREATE_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"']?(\w+)[`\"']?\s*\(([\s\S]*?)\)\s*;",
    re.I,
)
ALTER_FK = re.compile(
    r"FOREIGN\s+KEY\s*\(\s*[`\"']?(\w+)[`\"']?\s*\)\s*REFERENCES\s+[`\"']?(\w+)[`\"']?\s*\(\s*[`\"']?(\w+)[`\"']?\s*\)",
    re.I,
)
COL_LINE = re.compile(r"^\s*[`\"']?(\w+)[`\"']?\s+(\w+)", re.I)

RAILS_TABLE = re.compile(r"create_table\s+[:\"'](\w+)[\"']?", re.I)
DJANGO_MODEL = re.compile(r"migrations\.CreateModel\s*\(\s*name\s*=\s*['\"](\w+)['\"]", re.I)
LARAVEL_TABLE = re.compile(r"Schema::create\s*\(\s*['\"](\w+)['\"]", re.I)
ALEMBIC_TABLE = re.compile(r"op\.create_table\s*\(\s*['\"](\w+)['\"]", re.I)
EF_TABLE = re.compile(r"CreateTable\s*\(\s*name:\s*[\"'](\w+)[\"']", re.I)

ORM_CLASS = re.compile(
    r"class\s+(\w+)\s*\(\s*(?:models\.Model|db\.Model|Base|Document|Entity|gorm\.Model)\s*\)",
    re.I,
)
DJANGO_FIELD = re.compile(r"models\.(\w+)\(\s*(?:[^)]*,\s*)?(?:max_length=\d+\s*,\s*)?(?:primary_key=True\s*,\s*)?")
SQLALCHEMY_CLASS = re.compile(r"class\s+(\w+)\s*\([^)]*Base[^)]*\)\s*:", re.I)
SQLALCHEMY_COL = re.compile(r"^\s*(\w+)\s*=\s*Column\s*\(", re.M)

MSG_PATTERNS = [
    ("kafka", re.compile(r"""['"]([\w.-]+\.(?:events|commands|topic))['"]|Subscribe\s*\(\s*['"]([^'"]+)['"]""")),
    ("rabbitmq", re.compile(r"""Queue\s*\(\s*['"]([^'"]+)['"]|BasicPublish\s*\([^)]*routingKey:\s*['"]([^'"]+)['"]""")),
    ("grpc", re.compile(r"service\s+(\w+)\s*\{")),
]


def _read(root: Path, rel: str, limit: int = 400_000) -> str:
    p = safe_path(root, rel)
    if not p.is_file() or p.stat().st_size > limit:
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _module_id(root: Path, rel: str, lang: str, text: str) -> str:
    path = rel.replace("\\", "/")
    if lang == "java":
        m = JAVA_PKG.search(text[:2000])
        if m:
            return m.group(1)
        parts = Path(path).parts
        if "src" in parts:
            idx = parts.index("src")
            rest = parts[idx + 1:]
            if rest and rest[0] in ("main", "test"):
                rest = rest[1:]
            if rest and rest[0] == "java":
                rest = rest[1:]
            if rest:
                return ".".join(rest[:-1] + (Path(rest[-1]).stem,))
    if lang == "go":
        parts = Path(path).parts
        if "vendor" in parts:
            return path
        mod = _go_module(root)
        if mod and path.endswith(".go"):
            pkg_dir = str(Path(path).parent).replace("\\", "/")
            if pkg_dir == ".":
                return mod
            return f"{mod}/{pkg_dir}"
    if lang == "csharp":
        m = CS_NAMESPACE.search(text[:3000])
        if m:
            return m.group(1)
    if lang == "php":
        m = PHP_NAMESPACE.search(text[:3000])
        base = m.group(1).replace("\\", ".") if m else ""
        stem = Path(path).stem
        return f"{base}.{stem}" if base else path
    if lang in ("python", "javascript", "typescript", "ruby"):
        rel_path: Path = Path(path)
        if rel_path.name == "__init__.py":
            mod = ".".join(rel_path.parent.parts)
        elif rel_path.suffix:
            mod = ".".join(rel_path.with_suffix("").parts)
        else:
            mod = ".".join(rel_path.parts)
        return mod.replace("/", ".") or path
    return path.rsplit(".", 1)[0].replace("/", ".")


def _go_module(root: Path) -> str:
    text = _read(root, "go.mod", 32_000)
    m = re.search(r"^module\s+(\S+)", text, re.M)
    return m.group(1) if m else ""


def _resolve_import(root: Path, from_rel: str, lang: str, imp: str,
                    file_to_mod: dict[str, str], pkg_index: dict[str, str]) -> str | None:
    imp = imp.strip()
    if not imp or imp.startswith(("java.", "javax.", "org.junit", "org.springframework", "System",
                                  "Microsoft.", "Google.", "std", "testing", "fmt", "net/http")):
        return None
    if lang in ("javascript", "typescript"):
        if imp.startswith("."):
            base = Path(from_rel).parent
            target = (base / imp).with_suffix("")
            for ext in ("", ".ts", ".tsx", ".js", ".jsx"):
                cand = str((target.as_posix() + ext).replace("\\", "/"))
                if cand in file_to_mod:
                    return file_to_mod[cand]
            idx = str((target / "index").as_posix()).replace("\\", "/")
            for ext in (".ts", ".tsx", ".js", ".jsx"):
                if idx + ext in file_to_mod:
                    return file_to_mod[idx + ext]
        return None
    if lang == "python":
        key = imp.replace(".", "/")
        for suffix in (".py", "/__init__.py"):
            rel = f"{key}{suffix}"
            if rel in file_to_mod:
                return file_to_mod[rel]
        return pkg_index.get(imp)
    if lang == "go":
        mod = _go_module(root)
        if imp.startswith("./"):
            rel = str((Path(from_rel).parent / imp[2:]).with_suffix(".go")).replace("\\", "/")
            return file_to_mod.get(rel)
        if mod and imp.startswith(mod + "/"):
            return imp
        if mod and "/" not in imp:
            return f"{mod}/{imp}" if f"{mod}/{imp}" in pkg_index else None
        return None
    if lang == "java":
        return pkg_index.get(imp)
    if lang == "csharp":
        return pkg_index.get(imp)
    if lang == "php":
        return pkg_index.get(imp.replace("\\", "."))
    if lang == "ruby":
        rel = f"{imp.replace('.', '/')}.rb"
        return file_to_mod.get(rel)
    return None


def _parse_imports(root: Path, rel: str, lang: str, text: str) -> list[str]:
    out: list[str] = []
    if lang == "go":
        for block in GO_IMPORT_BLOCK.finditer(text):
            body = block.group(1) or block.group(2) or ""
            for line in body.splitlines():
                m = re.match(r'\s*"([^"]+)"', line)
                if m:
                    out.append(m.group(1))
        return out
    if lang == "python":
        if len(text) <= IMPORT_SCAN_BYTES:
            try:
                tree = ast.parse(text)
            except SyntaxError:
                tree = None
            if tree:
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        out.extend(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        out.append(node.module)
                if out:
                    return out
    for rx, grp in IMPORT_RES.get(lang, []):
        for m in rx.finditer(text):
            out.append(m.group(grp))
    return out


def _import_file_cap(scan) -> int:
    loc = getattr(scan, "code_loc", 0) or 0
    if loc > 500_000:
        return 350
    if loc > LARGE_REPO_LOC:
        return 550
    if loc > 50_000:
        return 850
    return MAX_IMPORT_FILES


def _code_files(scan) -> list[dict[str, Any]]:
    files = [f for f in scan.files if (f.get("language") or "") in CODE_LANGUAGES
             and f.get("language") != "sql"]
    files.sort(key=lambda f: ("/test" in f["path"] or f["path"].startswith("test"), f["path"]))
    return files[:_import_file_cap(scan)]


def _build_module_index(root: Path, scan, *, texts: dict[str, str] | None = None) -> tuple[
        dict[str, str], dict[str, str], dict[str, str]]:
    """file rel path -> module id; module id -> representative file; package/name -> module id."""
    file_to_mod: dict[str, str] = {}
    mod_to_file: dict[str, str] = {}
    pkg_index: dict[str, str] = {}
    for f in _code_files(scan):
        lang = f.get("language") or ""
        rel = f["path"]
        text = texts[rel] if texts and rel in texts else _read(root, rel, MAX_IMPORT_BYTES)
        mid = _module_id(root, rel, lang, text)
        file_to_mod[rel] = mid
        mod_to_file.setdefault(mid, rel)
        pkg_index[mid] = mid
    return file_to_mod, mod_to_file, pkg_index


def _migration_paths(scan) -> list[str]:
    paths = list(scan.migrations[:120])
    seen = set(paths)
    for f in scan.files:
        rel = f["path"].replace("\\", "/")
        if rel in seen:
            continue
        if rel.endswith(".rb") and (rel.startswith("db/") or "/db/" in rel):
            paths.append(rel)
            seen.add(rel)
    return paths[:140]


def _tools_bin(name: str) -> str | None:
    local = Path(__file__).resolve().parents[2] / ".tools" / "bin" / name
    if local.exists():
        return str(local)
    return shutil.which(name)


def _try_external_graph(root: Path, lang: str, *, code_loc: int = 0) -> dict[str, Any] | None:
    if code_loc > LARGE_REPO_LOC:
        return None
    if lang == "go":
        exe = _tools_bin("go")
        if not exe:
            return None
        try:
            p = subprocess.run([exe, "list", "-json", "./..."], cwd=root, capture_output=True,
                               text=True, timeout=90)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0:
            return None
        edges: list[dict[str, str]] = []
        for line in p.stdout.splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            frm = obj.get("ImportPath", "")
            for dep in obj.get("Imports") or []:
                if dep.startswith(str(obj.get("Module", {}).get("Path", "")) or frm.rsplit("/", 1)[0]):
                    edges.append({"from": frm, "to": dep, "kind": "import"})
        return {"source": "go list", "edges": edges[:MAX_GRAPH_EDGES]}
    if lang in ("javascript", "typescript"):
        exe = _tools_bin("madge")
        if not exe:
            return None
        try:
            p = subprocess.run([exe, "--json", str(root)], cwd=root, capture_output=True,
                               text=True, timeout=90)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0 or not p.stdout.strip():
            return None
        try:
            obj = json.loads(p.stdout)
        except json.JSONDecodeError:
            return None
        madge_edges = [{"from": a, "to": b, "kind": "import"}
                       for a, deps in obj.items() for b in (deps if isinstance(deps, list) else [])][:MAX_GRAPH_EDGES]
        return {"source": "madge", "edges": madge_edges}
    if lang == "python":
        exe = _tools_bin("pydeps")
        if not exe:
            return None
        try:
            p = subprocess.run([exe, "--show-deps", "--no-output", str(root)], cwd=root,
                               capture_output=True, text=True, timeout=90)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0:
            return None
        py_edges: list[dict[str, str]] = []
        for line in p.stdout.splitlines():
            if " -> " not in line:
                continue
            a, b = line.split(" -> ", 1)
            py_edges.append({"from": a.strip(), "to": b.strip(), "kind": "import"})
        if not py_edges:
            return None
        return {"source": "pydeps", "edges": py_edges[:MAX_GRAPH_EDGES]}
    if lang == "java":
        exe = _tools_bin("jdeps") or shutil.which("jdeps")
        if not exe:
            return None
        try:
            p = subprocess.run([exe, "-summary", "-R", str(root)], cwd=root, capture_output=True,
                               text=True, timeout=120)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0 or "Unable to find" in (p.stderr or p.stdout):
            return None
        jdeps_edges: list[dict[str, str]] = []
        for line in p.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0].endswith(".jar") is False and "." in parts[0]:
                jdeps_edges.append({"from": parts[0], "to": parts[-1], "kind": "import"})
        if not jdeps_edges:
            return None
        return {"source": "jdeps", "edges": jdeps_edges[:MAX_GRAPH_EDGES]}
    return None


def dependency_graph(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    scan = _cached_scan(root)
    lang = scan.primary_language
    ext = _try_external_graph(root, lang, code_loc=getattr(scan, "code_loc", 0) or 0)
    texts: dict[str, str] = {}
    edge_counts: Counter[tuple[str, str]] = Counter()
    code_files = _code_files(scan)
    for f in code_files:
        rel = f["path"]
        text = _read(root, rel, IMPORT_SCAN_BYTES)
        if text:
            texts[rel] = text
    file_to_mod, mod_to_file, pkg_index = _build_module_index(root, scan, texts=texts)
    for f in code_files:
        rel = f["path"]
        if rel not in texts:
            continue
        lang_f = f.get("language") or ""
        text = texts[rel]
        src = file_to_mod[rel]
        for imp in _parse_imports(root, rel, lang_f, text):
            tgt = _resolve_import(root, rel, lang_f, imp, file_to_mod, pkg_index)
            if tgt and tgt != src:
                edge_counts[(src, tgt)] += 1
    fan_out: Counter[str] = Counter()
    fan_in: Counter[str] = Counter()
    for (a, b), _ in edge_counts.items():
        fan_out[a] += 1
        fan_in[b] += 1
    ranked = sorted(edge_counts.items(), key=lambda kv: -kv[1])
    edges = [{"from": a, "to": b, "weight": w} for (a, b), w in ranked[:MAX_GRAPH_EDGES]]
    nodes = sorted(set(fan_in) | set(fan_out), key=lambda n: -(fan_in[n] + fan_out[n]))[:MAX_GRAPH_NODES]
    node_set = set(nodes)
    adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        if e["from"] in node_set and e["to"] in node_set:
            adj[e["from"]].append(e["to"])
    cycles: list[list[str]] = []
    stack: list[str] = []
    on_stack: set[str] = set()
    seen: set[str] = set()

    def dfs(u: str) -> None:
        seen.add(u)
        on_stack.add(u)
        stack.append(u)
        for v in adj.get(u, ()):
            if v not in seen:
                dfs(v)
            elif v in on_stack:
                if len(cycles) < MAX_CYCLES:
                    i = stack.index(v)
                    cycles.append(stack[i:] + [v])
        stack.pop()
        on_stack.remove(u)

    for n in nodes:
        if n not in seen:
            dfs(n)
    modules = [
        {"module": n, "fan_in": fan_in[n], "fan_out": fan_out[n], "sample_file": mod_to_file.get(n)}
        for n in nodes
    ]
    out: dict[str, Any] = {
        "repo": root.name,
        "commit": scan.commit,
        "primary_language": lang,
        "modules_sampled": len(file_to_mod),
        "internal_edges": len(edge_counts),
        "modules": modules,
        "edges": edges,
        "cycles": cycles,
        "method": "ast/regex",
    }
    if ext:
        out["external_hint"] = ext
    return out


def change_coupling(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    scan = scan_repo(root)
    file_to_mod, _, _ = _build_module_index(root, scan)
    git_dir = root / ".git"
    if not git_dir.is_dir():
        return {"repo": root.name, "status": "ERROR", "detail": "not a git repository"}
    try:
        p = subprocess.run(
            ["git", "-C", str(root), "log", f"-{MAX_COMMITS}", "--name-only", "--pretty=format:%H"],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"repo": root.name, "status": "ERROR", "detail": str(exc)}
    if p.returncode != 0:
        return {"repo": root.name, "status": "ERROR", "detail": (p.stderr or p.stdout)[-400:]}
    pair_counts: Counter[tuple[str, str]] = Counter()
    file_churn: Counter[str] = Counter()
    commits_used = skipped = 0
    cur_files: list[str] = []
    for line in p.stdout.splitlines():
        if re.fullmatch(r"[0-9a-f]{7,40}", line):
            if cur_files:
                mods = sorted({file_to_mod.get(f, f) for f in cur_files if f})
                if 1 < len(mods) <= MAX_FILES_PER_COMMIT:
                    commits_used += 1
                    for f in cur_files:
                        file_churn[f] += 1
                    for i, a in enumerate(mods):
                        for b in mods[i + 1:]:
                            pair_counts[(a, b)] += 1
                else:
                    skipped += 1
            cur_files = []
        elif line.strip():
            rel = line.strip().replace("\\", "/")
            if any(part in EXCLUDE_DIRS for part in Path(rel).parts):
                continue
            cur_files.append(rel)
    if cur_files:
        mods = sorted({file_to_mod.get(f, f) for f in cur_files if f})
        if 1 < len(mods) <= MAX_FILES_PER_COMMIT:
            commits_used += 1
            for f in cur_files:
                file_churn[f] += 1
            for i, a in enumerate(mods):
                for b in mods[i + 1:]:
                    pair_counts[(a, b)] += 1
    pairs = []
    for (a, b), n in pair_counts.most_common(MAX_COUPLED_PAIRS):
        support = n
        confidence = round(n / max(commits_used, 1), 4)
        pairs.append({"modules": [a, b], "co_changes": n, "support": support, "confidence": confidence})
    hotspots = [
        {"file": f, "commits": n, "module": file_to_mod.get(f, f)}
        for f, n in file_churn.most_common(MAX_HOTSPOTS)
    ]
    return {
        "repo": root.name,
        "commit": scan.commit,
        "commits_scanned": commits_used,
        "commits_skipped_large": skipped,
        "coupled_pairs": pairs,
        "hotspots": hotspots,
    }


def _parse_sql_schema(text: str, source: str, tables: dict[str, dict[str, Any]]) -> None:
    for m in CREATE_TABLE.finditer(text):
        name, body = m.group(1), m.group(2)
        cols = []
        fks = []
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.upper().startswith(("PRIMARY", "UNIQUE", "KEY", "CONSTRAINT", "INDEX")):
                fk = ALTER_FK.search(line)
                if fk:
                    fks.append({"column": fk.group(1), "ref_table": fk.group(2), "ref_column": fk.group(3)})
                continue
            cm = COL_LINE.match(line)
            if cm:
                cols.append({"name": cm.group(1), "type": cm.group(2)})
        rec = tables.setdefault(name, {"table": name, "columns": [], "foreign_keys": [], "sources": []})
        rec["columns"] = cols[:40] or rec["columns"]
        rec["foreign_keys"] = fks[:20] or rec["foreign_keys"]
        if source not in rec["sources"]:
            rec["sources"].append(source)


def db_schema(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    scan = scan_repo(root)
    tables: dict[str, dict[str, Any]] = {}
    for rel in scan.sql_files[:80]:
        _parse_sql_schema(_read(root, rel), rel, tables)
    for rel in _migration_paths(scan):
        text = _read(root, rel)
        if not text:
            continue
        src = rel
        for rx in (RAILS_TABLE, LARAVEL_TABLE, ALEMBIC_TABLE, EF_TABLE):
            for m in rx.finditer(text):
                name = m.group(1)
                rec = tables.setdefault(name, {"table": name, "columns": [], "foreign_keys": [], "sources": []})
                if src not in rec["sources"]:
                    rec["sources"].append(src)
        for m in DJANGO_MODEL.finditer(text):
            name = m.group(1).lower()
            rec = tables.setdefault(name, {"table": name, "columns": [], "foreign_keys": [], "sources": []})
            if src not in rec["sources"]:
                rec["sources"].append(src)
    for rel in scan.model_files[:100]:
        text = _read(root, rel)
        if not text:
            continue
        for m in ORM_CLASS.finditer(text):
            name = m.group(1)
            cols = [fm.group(1) for fm in DJANGO_FIELD.finditer(text)][:30]
            rec = tables.setdefault(name, {"table": name, "columns": [], "foreign_keys": [], "sources": []})
            if cols and not rec["columns"]:
                rec["columns"] = [{"name": c, "type": "orm"} for c in cols]
            if rel not in rec["sources"]:
                rec["sources"].append(rel)
        for m in SQLALCHEMY_CLASS.finditer(text):
            name = m.group(1)
            cols = [cm.group(1) for cm in SQLALCHEMY_COL.finditer(text)][:30]
            rec = tables.setdefault(name, {"table": name, "columns": [], "foreign_keys": [], "sources": []})
            if cols and not rec["columns"]:
                rec["columns"] = [{"name": c, "type": "column"} for c in cols]
            if rel not in rec["sources"]:
                rec["sources"].append(rel)
    ordered = sorted(tables.values(), key=lambda t: t["table"])[:MAX_TABLES]
    return {
        "repo": root.name,
        "commit": scan.commit,
        "tables": ordered,
        "table_count": len(tables),
        "truncated": len(tables) > MAX_TABLES,
    }


def api_surface(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    scan = scan_repo(root)
    by_module: dict[str, list[dict[str, str]]] = defaultdict(list)
    endpoints: list[dict[str, str]] = []
    for r in scan.routes[:MAX_ENDPOINTS]:
        rel = r.get("file", "")
        mod = str(Path(rel).parent).replace("\\", "/") if rel else "root"
        ep = {"method": _guess_method(r.get("framework", ""), r.get("route", "")),
              "path": r.get("route") or "", "framework": r.get("framework", ""), "file": rel}
        endpoints.append(ep)
        by_module[mod].append(ep)
    messaging: list[dict[str, str]] = []
    for f in scan.files:
        if f.get("language") not in CODE_LANGUAGES:
            continue
        rel = f["path"]
        if f.get("language") not in ("java", "csharp", "go", "python", "typescript", "javascript"):
            continue
        text = _read(root, rel, 80_000)
        for kind, rx in MSG_PATTERNS:
            for m in rx.finditer(text):
                topic = next((g for g in m.groups() if g), "")
                if topic:
                    messaging.append({"kind": kind, "name": topic, "file": rel})
        if len(messaging) >= 60:
            break
    exports: list[dict[str, str]] = []
    for f in scan.files:
        if not f["path"].endswith((".ts", ".tsx", ".js")):
            continue
        if "index." not in Path(f["path"]).name:
            continue
        text = _read(root, f["path"], 40_000)
        if re.search(r"export\s+(?:default\s+)?(?:class|function|const)\s+\w+", text):
            exports.append({"module": str(Path(f["path"]).parent), "file": f["path"]})
        if len(exports) >= 30:
            break
    grouped = {k: v[:25] for k, v in sorted(by_module.items(), key=lambda kv: -len(kv[1]))[:40]}
    return {
        "repo": root.name,
        "commit": scan.commit,
        "http_endpoints": endpoints[:MAX_ENDPOINTS],
        "by_module": grouped,
        "messaging": messaging[:60],
        "exported_interfaces": exports,
        "endpoint_count": len(scan.routes),
    }


def _guess_method(framework: str, route: str) -> str:
    fw = framework.lower()
    if "post" in fw:
        return "POST"
    if "get" in fw and "forget" not in fw:
        return "GET"
    if "put" in fw:
        return "PUT"
    if "delete" in fw:
        return "DELETE"
    if "patch" in fw:
        return "PATCH"
    return "ANY"
