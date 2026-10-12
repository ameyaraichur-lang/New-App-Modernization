"""Golden facts: tool-derived ground truth for each corpus repo, and scoring of P1 output.

Facts come from the repository itself — scc for languages, manifests for dependencies,
source patterns for ORM entities and HTTP routes, files for CI/containers/licences — using
extraction written here, independently of the pipeline's scanner (only the directory scope
rules are shared). Each fact keeps its source location so a human can spot-check it;
review verdicts in evals/golden/review.json override generated labels.

Fact types and where P1 must report them:
  primary_language   A1 repositories[0].primary_language
  framework, dependency, test_framework, build_manifest   A1 dependencies (names / sources)
  has_tests          A1 repositories[0].test_files > 0
  datastore          A1/A3/A4 text
  has_data_layer     A3 entities or datasets non-empty
  entity             A3 entities / datasets
  route              A3 api_contract_refs, A5 journeys
  containerized, ci  A4 resources
  runtime_version    A1/A4/A6/A11 text
  license            A1/A6 text
  capability_route   A5 capability_route
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterator

from appmod.tools.repo_intel import EXCLUDE_DIRS, VENDORED_DIRS, VENDORED_FILE_RE

ROOT = Path(__file__).resolve().parents[2]
FACTS_DIR = ROOT / "evals" / "golden" / "facts"
REVIEW = ROOT / "evals" / "golden" / "review.json"
SKIP_DIRS = EXCLUDE_DIRS | VENDORED_DIRS
TEST_DIR_RE = re.compile(r"(^|/)(tests?|spec|specs|__tests__|testing|e2e|src/test)(/|$)", re.I)
TEST_FILE_RE = re.compile(r"(Tests?\.(java|cs|kt)|_test\.(go|py)|^test_.*\.py|_spec\.rb|\.(spec|test)\.[jt]sx?"
                          r"|Test\.php|\.t)$", re.I)
DOCS_DIR_RE = re.compile(r"(^|/)docs?/", re.I)
CAPS = {"entity": 20, "route": 15, "dependency": 15}
MAX_BYTES = 1_000_000
CODE_EXTS = {".java", ".kt", ".scala", ".groovy", ".py", ".js", ".jsx", ".ts", ".tsx", ".cs", ".vb", ".php",
             ".rb", ".go", ".pl", ".pm", ".t", ".cbl", ".cob"}

SCC_LANG = {"Java": "java", "Python": "python", "JavaScript": "javascript", "TypeScript": "typescript",
            "C#": "csharp", "PHP": "php", "Ruby": "ruby", "Go": "go", "COBOL": "cobol", "Perl": "perl",
            "Kotlin": "kotlin", "Scala": "scala", "Groovy": "groovy", "Visual Basic for Applications": "vb",
            "Visual Basic": "vb"}

FRAMEWORKS: list[tuple[str, str]] = [
    ("spring-boot", r"spring-boot"), ("spring-mvc", r"spring-webmvc"), ("struts2", r"struts2-core"),
    ("jakarta-ee", r"jakartaee-api|javaee-api|jakarta\.platform|javaee-web-api"),
    ("django", r"^django$"), ("flask", r"^flask$"), ("fastapi", r"^fastapi$"),
    ("express", r"^express$"), ("nestjs", r"^@nestjs/core$"), ("react", r"^react$"),
    ("angular", r"^@angular/core$|^angular$"), ("vue", r"^vue$"),
    ("laravel", r"^laravel/framework$"), ("symfony", r"^symfony/framework-bundle$"),
    ("sinatra", r"^sinatra$"), ("rails", r"^rails$"),
    ("gin", r"gin-gonic/gin"), ("echo", r"labstack/echo"), ("chi", r"go-chi/chi"),
    ("aspnetcore", r"^microsoft\.aspnetcore"), ("aspnet-mvc", r"^microsoft\.aspnet\.mvc$"),
    ("entity-framework", r"^entityframework$|^microsoft\.entityframeworkcore"),
]
TEST_FRAMEWORKS = r"junit|testng|^pytest$|^jest$|^mocha$|^jasmine|^karma$|^rspec|minitest|phpunit|xunit|^nunit|mstest"
DATASTORES: dict[str, str] = {
    "postgresql": r"postgres|psycopg|\bpg\b|npgsql",
    "mysql": r"mysql|mariadb",
    "sqlite": r"sqlite",
    "h2": r"\bh2\b|h2database",
    "sqlserver": r"sql ?server|mssql|sqlclient|localdb",
    "mongodb": r"mongo",
    "redis": r"redis",
    "vsam": r"\bvsam\b|\bksds\b|\besds\b",
    "db2": r"\bdb2\b",
}
DATASTORE_CONFIG = re.compile(r"(application[\w-]*\.(properties|ya?ml)|settings\.py|database\.php|appsettings[\w.]*\.json"
                              r"|web\.config|\.env\.example|config\.php|app\.ini|database\.yml|docker-compose[\w.-]*\.ya?ml)$",
                              re.I)
MAINFRAME_SOURCE = re.compile(r"\.(jcl|cbl|cob|csd|prc)$", re.I)
TEMPLATE_RE = re.compile(r"\.(jsp|cshtml|aspx|erb|twig|tmpl|hbs|ejs|xhtml|blade\.php|jinja2?|haml|vue|tsx|jsx)$"
                         r"|(^|/)(templates|views)/.+\.html?$|(^|/)index\.html$", re.I)
CI_RE = re.compile(r"(^|/)(\.github/workflows/.+\.ya?ml|\.travis\.yml|jenkinsfile|\.gitlab-ci\.yml|"
                   r"azure-pipelines\.ya?ml|appveyor\.yml|\.circleci/config\.yml)$", re.I)
LICENSES = [("apache", r"apache license"), ("mit", r"\bmit license|permission is hereby granted, free of charge"),
            ("bsd", r"\bbsd\b|redistribution and use in source and binary forms"),
            ("lgpl", r"lesser general public license"), ("gpl", r"gnu general public license"),
            ("mpl", r"mozilla public license")]

ENTITY_PATTERNS: list[tuple[re.Pattern[str], re.Pattern[str]]] = [
    (re.compile(r"\.(java|kt)$"), re.compile(r"@Entity\b[\s\S]{0,400}?\bclass\s+(\w+)")),
    (re.compile(r"\.cs$"), re.compile(r"\bDbSet<(\w+)>")),
    (re.compile(r"\.py$"), re.compile(r"^class\s+(\w+)\((?:[\w.]*\.)?(?:Model|db\.Model|Base|DeclarativeBase)\)", re.M)),
    (re.compile(r"\.rb$"), re.compile(r"^\s*class\s+(\w+)\s*<\s*(?:ApplicationRecord|ActiveRecord::Base)", re.M)),
    (re.compile(r"\.php$"), re.compile(r"\bclass\s+(\w+)\s+extends\s+(?:Model|Eloquent|Authenticatable)\b")),
    (re.compile(r"\.go$"), re.compile(r"type\s+(\w+)\s+struct\s*\{[^}]{0,300}?gorm\.Model")),
    (re.compile(r"\.prisma$"), re.compile(r"^model\s+(\w+)\s*\{", re.M)),
    (re.compile(r"\.[jt]s$"), re.compile(r"@Entity\([^)]*\)\s*(?:export\s+)?class\s+(\w+)|mongoose\.model\(\s*['\"](\w+)")),
]
ROUTE_PATTERNS: list[tuple[re.Pattern[str], re.Pattern[str]]] = [
    (re.compile(r"\.(java|kt)$"), re.compile(r"@(?:Get|Post|Put|Delete|Patch|Request)Mapping\(\s*(?:(?:value|path)\s*=\s*)?\{?\s*\"(/[^\"]*)\"")),
    (re.compile(r"\.(java|kt)$"), re.compile(r"@Path\(\s*\"(/[^\"]*)\"")),
    (re.compile(r"\.py$"), re.compile(r"\.(?:route|get|post|put|delete|patch)\(\s*['\"](/[^'\"]*)['\"]")),
    (re.compile(r"(^|/)urls\.py$"), re.compile(r"\bpath\(\s*['\"]([^'\"]+)['\"]")),
    (re.compile(r"(^|/)urls\.py$"), re.compile(r"\b(?:re_path|url)\(\s*r?['\"]\^?([a-z][\w/-]*)")),
    (re.compile(r"\.[jt]s$"), re.compile(r"\b(?:router|app|api)\.(?:get|post|put|delete|patch)\(\s*['\"`](/[^'\"`]*)")),
    (re.compile(r"\.php$"), re.compile(r"Route::(?:get|post|put|delete|patch|any|match)\(\s*['\"]([^'\"]+)['\"]")),
    (re.compile(r"\.rb$"), re.compile(r"^\s*(?:get|post|put|delete|patch)\s+['\"](/[^'\"]*)['\"]", re.M)),
    (re.compile(r"(^|/)config/routes\.rb$"), re.compile(r"^\s*resources?\s+:(\w+)", re.M)),
    (re.compile(r"\.go$"), re.compile(r"\.(?:GET|POST|PUT|DELETE|PATCH|Get|Post|Put|Delete|Patch|Group|Combo)\(\s*\"(/[^\"]*)\"")),
    (re.compile(r"\.cs$"), re.compile(r"\[(?:Http(?:Get|Post|Put|Delete|Patch)|Route)\(\s*\"([^\"]+)\"")),
]


@dataclass
class Fact:
    type: str
    key: str
    expected: Any
    source: str
    snippet: str = ""
    review: str | None = None

    @property
    def id(self) -> str:
        return f"{self.type}:{self.key}"


def _files(root: Path) -> Iterator[tuple[str, Path]]:
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        for p in entries:
            if p.is_symlink():
                continue
            if p.is_dir():
                if p.name not in SKIP_DIRS and not p.name.startswith("."):
                    stack.append(p)
                elif p.name in (".github", ".circleci", ".devcontainer", ".docker"):
                    stack.append(p)
            elif p.is_file() and not VENDORED_FILE_RE.match(p.name) and ".min." not in p.name:
                yield p.relative_to(root).as_posix(), p


def _read(p: Path) -> str:
    try:
        if p.stat().st_size > MAX_BYTES:
            return ""
        return p.read_text(errors="ignore")
    except OSError:
        return ""


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _in_comment(text: str, pos: int) -> bool:
    """Match sits in a comment or prose line (e.g. Django's generated urls.py instructions)."""
    prefix = text[text.rfind("\n", 0, pos) + 1:pos].strip()
    return prefix.startswith(("#", "//", "*", "/*", "<!--")) or bool(re.search(r"[A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z]+", prefix))


def _pick(items: dict[str, Fact], cap: int) -> list[Fact]:
    keys = sorted(items, key=lambda k: hashlib.sha1(k.encode()).hexdigest())[:cap]
    return [items[k] for k in sorted(keys)]


def _deps(rel: str, text: str) -> list[str]:
    name = rel.rsplit("/", 1)[-1].lower()
    out: list[str] = []
    if name == "pom.xml":
        for m in re.finditer(r"<dependency>\s*<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>", text):
            out.append(f"{m.group(1).strip()}:{m.group(2).strip()}")
    elif name.startswith("build.gradle"):
        out += [m.group(1) for m in re.finditer(
            r"(?:implementation|api|compile|runtimeOnly|testImplementation|compileOnly)\s*\(?\s*['\"]([\w.\-]+:[\w.\-]+)", text)]
    elif name == "package.json":
        try:
            pj = json.loads(text)
        except ValueError:
            return out
        for k in ("dependencies", "devDependencies"):
            out += list((pj.get(k) or {}).keys())
    elif re.fullmatch(r"requirements[\w.-]*\.txt", name):
        out += [m.group(1) for m in re.finditer(r"^\s*([A-Za-z][\w.\-]*)", text, re.M)]
    elif name == "pyproject.toml":
        try:
            data = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            return out
        for d in data.get("project", {}).get("dependencies", []) or []:
            if dm := re.match(r"\s*([A-Za-z][\w.\-]*)", d):
                out.append(dm.group(1))
        out += [k for k in (data.get("tool", {}).get("poetry", {}).get("dependencies", {}) or {}) if k != "python"]
    elif name == "composer.json":
        try:
            cj = json.loads(text)
        except ValueError:
            return out
        for k in ("require", "require-dev"):
            out += [d for d in (cj.get(k) or {}) if d != "php" and not d.startswith("ext-")]
    elif name == "gemfile":
        out += [m.group(1) for m in re.finditer(r"^\s*gem\s+['\"]([\w\-]+)['\"]", text, re.M)]
    elif name == "go.mod":
        block = re.findall(r"require\s*\(([^)]*)\)", text)
        lines = "\n".join(block) + "\n" + "\n".join(re.findall(r"^require\s+(\S+\s+\S+)", text, re.M))
        out += [m.group(1) for m in re.finditer(r"^\s*([\w.\-]+/[\w.\-/]+)\s+v", lines, re.M)]
    elif name.endswith((".csproj", ".vbproj")):
        out += re.findall(r"<PackageReference\s+Include=\"([^\"]+)\"", text)
    elif name == "packages.config":
        out += re.findall(r"<package\s+id=\"([^\"]+)\"", text)
    elif name == "cpanfile":
        out += re.findall(r"^\s*(?:requires|recommends)\s+['\"]([\w:]+)['\"]", text, re.M)
    return [d.strip() for d in out if d.strip()]


def _runtime(rel: str, text: str) -> str | None:
    name = rel.rsplit("/", 1)[-1].lower()
    pats: list[tuple[str, str]] = []
    if name == "pom.xml":
        pats = [(r"<java\.version>\s*(?:1\.)?(\d+)", "java {}"), (r"<maven\.compiler\.(?:source|release)>\s*(?:1\.)?(\d+)", "java {}")]
    elif name.startswith("build.gradle"):
        pats = [(r"languageVersion\s*=?\s*JavaLanguageVersion\.of\((\d+)\)", "java {}"),
                (r"sourceCompatibility\s*=\s*['\"]?(?:JavaVersion\.VERSION_)?(?:1[._])?(\d+)", "java {}")]
    elif name == "go.mod":
        pats = [(r"^go\s+(\d+\.\d+)", "go {}")]
    elif name == "package.json":
        pats = [(r"\"node\"\s*:\s*\"[^\d\"]*(\d+)", "node {}")]
    elif name == "composer.json":
        pats = [(r"\"php\"\s*:\s*\"[^\d\"]*(\d+\.\d+)", "php {}")]
    elif name == "pyproject.toml":
        pats = [(r"requires-python\s*=\s*['\"][^\d'\"]*(3\.\d+)", "python {}"), (r"^python\s*=\s*['\"][^\d'\"]*(3\.\d+)", "python {}")]
    elif name in ("runtime.txt", ".python-version"):
        pats = [(r"(3\.\d+)", "python {}")]
    elif name == ".ruby-version":
        pats = [(r"(\d+\.\d+)", "ruby {}")]
    elif name.endswith(".csproj"):
        pats = [(r"<TargetFrameworks?>\s*([\w.]+)", "{}"), (r"<TargetFrameworkVersion>\s*v?([\d.]+)", "net{}")]
    for pat, fmt in pats:
        if m := re.search(pat, text, re.M):
            return fmt.format(m.group(1)).lower()
    return None


def _primary_language(root: Path, scc: str | None) -> tuple[str, str] | None:
    if not scc:
        return None
    args = [scc, "--format", "json", "--no-cocomo", "--exclude-dir", ",".join(sorted(SKIP_DIRS)),
            "--not-match", r"(\.min\.(js|css)$)|" + VENDORED_FILE_RE.pattern, str(root)]
    try:
        out = json.loads(subprocess.run(args, capture_output=True, text=True, timeout=900).stdout or "[]")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    langs = sorted(((x["Code"], SCC_LANG[x["Name"]]) for x in out if x["Name"] in SCC_LANG), reverse=True)
    return (langs[0][1], f"scc: {', '.join(f'{lang} {code}' for code, lang in langs[:3])}") if langs else None


def derive(root: Path, scc: str | None = None) -> list[Fact]:
    """Ground-truth facts for one repository checkout."""
    facts: list[Fact] = []
    deps: dict[str, Fact] = {}
    entities: dict[str, Fact] = {}
    routes: dict[str, Fact] = {}
    stores: dict[str, Fact] = {}
    manifests: dict[str, Fact] = {}
    runtime: Fact | None = None
    has_templates = False
    first: dict[str, str] = {}
    licence: Fact | None = None
    for rel, p in _files(root):
        name = p.name.lower()
        is_test = bool(TEST_DIR_RE.search(rel) or TEST_FILE_RE.search(p.name))
        has_templates |= bool(TEMPLATE_RE.search(rel)) and not is_test
        for kind, found in (("tests", is_test and p.suffix.lower() in CODE_EXTS),
                          ("docker", name == "dockerfile" or name.endswith(".dockerfile")),
                          ("ci", bool(CI_RE.search(rel))),
                          ("sql", name.endswith(".sql") or "/migrations/" in f"/{rel}")):
            if found:
                first.setdefault(kind, rel)
        if licence is None and rel.count("/") == 0 and name.startswith(("licen", "copying")):
            head = _read(p)[:3000].lower()
            for label, pat in LICENSES:
                if re.search(pat, head):
                    licence = Fact("license", "license", label, rel, head[:120].strip())
                    break
        manifest_like = (name in ("pom.xml", "package.json", "composer.json", "gemfile", "go.mod",
                                  "packages.config", "pyproject.toml", "runtime.txt", ".python-version",
                                  ".ruby-version", "cpanfile", "makefile.pl", "build.pl")
                         or name.startswith("build.gradle") or re.fullmatch(r"requirements[\w.-]*\.txt", name)
                         or name.endswith((".csproj", ".vbproj")))
        text = ""
        if manifest_like and "node_modules" not in rel and not DOCS_DIR_RE.search(rel):
            text = _read(p)
            if name in ("pom.xml", "package.json", "composer.json", "gemfile", "go.mod", "pyproject.toml",
                        "cpanfile", "makefile.pl", "build.pl") \
                    or name.startswith("build.gradle") or name.endswith(".csproj") or name.startswith("requirements"):
                kind = "*.csproj" if name.endswith(".csproj") else name
                manifests.setdefault(kind, Fact("build_manifest", kind, True, rel))
            for d in _deps(rel, text):
                pos = text.find(d.rsplit(":", 1)[-1])
                deps.setdefault(d.lower(), Fact("dependency", d.lower(), True,
                                                f"{rel}:{_line(text, pos)}" if pos >= 0 else rel, d))
            if runtime is None and (rt := _runtime(rel, text)):
                runtime = Fact("runtime_version", "runtime", rt, rel)
        if is_test:
            continue
        if DATASTORE_CONFIG.search(rel) or MAINFRAME_SOURCE.search(rel):
            low = (text or _read(p)).lower()
            for label, pat in DATASTORES.items():
                if label not in stores and (m := re.search(pat, low)):
                    stores[label] = Fact("datastore", label, True, f"{rel}:{_line(low, m.start())}",
                                         low[max(0, m.start() - 40):m.end() + 40].strip())
        for path_re, ent_re in ENTITY_PATTERNS:
            if path_re.search(rel):
                body = text or _read(p)
                for m in ent_re.finditer(body):
                    n = next(g for g in m.groups() if g)
                    if n.lower() not in ("model", "base") and n not in entities:
                        entities[n] = Fact("entity", n, True, f"{rel}:{_line(body, m.start())}", m.group(0)[-120:])
        for path_re, route_re in ROUTE_PATTERNS:
            if path_re.search(rel):
                body = text or _read(p)
                for m in route_re.finditer(body):
                    if _in_comment(body, m.start()):
                        continue
                    raw = m.group(1)
                    path = raw if raw.startswith("/") else f"/{raw}"
                    norm = normalize_route(path)
                    if norm not in ("", "/") and norm not in routes and len(static_segments(norm)) > 0:
                        routes[norm] = Fact("route", norm, True, f"{rel}:{_line(body, m.start())}", m.group(0)[:120])
    for d, f in deps.items():
        for label, pat in DATASTORES.items():
            if label not in stores and re.search(pat, d):
                stores[label] = Fact("datastore", label, True, f.source, f.snippet)
    lang = _primary_language(root, scc)
    if lang:
        facts.append(Fact("primary_language", "primary_language", lang[0], "scc", lang[1]))
    for label, pat in FRAMEWORKS:
        hit = next((f for d, f in deps.items() if re.search(pat, d)), None)
        if hit:
            facts.append(Fact("framework", label, hit.key, hit.source, hit.snippet))
    for d, f in sorted(deps.items()):
        if re.search(TEST_FRAMEWORKS, d.rsplit(":", 1)[-1]):
            facts.append(Fact("test_framework", d, True, f.source, f.snippet))
            break
    facts += list(manifests.values())
    facts.append(Fact("has_tests", "has_tests", "tests" in first, first.get("tests", "no test code found")))
    facts += list(stores.values())
    data_src = next(iter(entities.values()), None) or next(iter(stores.values()), None)
    facts.append(Fact("has_data_layer", "has_data_layer", bool(data_src or "sql" in first),
                      data_src.source if data_src else first.get("sql", "no entities, .sql, migrations or datastore")))
    facts += _pick(entities, CAPS["entity"])
    facts += _pick(routes, CAPS["route"])
    facts += _pick({k: v for k, v in deps.items()}, CAPS["dependency"])
    facts.append(Fact("containerized", "containerized", "docker" in first, first.get("docker", "no Dockerfile")))
    facts.append(Fact("ci", "ci", "ci" in first, first.get("ci", "no CI config")))
    if runtime:
        facts.append(runtime)
    if licence:
        facts.append(licence)
    route = "UI" if has_templates else ("API_ONLY" if routes else "HEADLESS")
    facts.append(Fact("capability_route", "capability_route", route,
                      "templates/views" if has_templates else "routes without templates"))
    return facts


PATH_LIKE = re.compile(r"(?<![\w.])/[\w\-{}<>:*.]+(?:/[\w\-{}<>:*.]*)*")


FS_PREFIXES = ("/users/", "/home/", "/private/", "/tmp/", "/var/", "/opt/", "/volumes/")


def route_candidates(payloads: dict[str, dict[str, Any]]) -> list[str]:
    """Path-like strings anywhere in P1 output, minus file-system paths and source files."""
    out = []
    for c in PATH_LIKE.findall(_text(*payloads.values())):
        c = c.rstrip(".,;:")
        if c.startswith(FS_PREFIXES) or Path(c).suffix.lower() in CODE_EXTS:
            continue
        out.append(c)
    return out


def normalize_route(path: str) -> str:
    p = path.strip().lower().split("?")[0]
    p = re.sub(r"\(\?p<\w+>[^)]*\)|<[^>]+>|\{[^}]+\}|:\w+|\*\w*|\$\w+", "*", p)
    p = re.sub(r"[\^$]", "", p)
    p = re.sub(r"/+", "/", p).rstrip("/")
    return p or "/"


def static_segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s and s != "*"]


def _contains_route(expected: str, candidates: list[str]) -> bool:
    want = static_segments(expected)
    for c in candidates:
        have = static_segments(normalize_route(c))
        for i in range(len(have) - len(want) + 1):
            if have[i:i + len(want)] == want:
                return True
    return False


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _entity_forms(name: str) -> list[str]:
    n = _norm(name)
    forms = [n, n + "s", n + "es"]
    if n.endswith("y"):
        forms.append(n[:-1] + "ies")
    return forms


def _text(*parts: Any) -> str:
    return json.dumps(parts, ensure_ascii=False).lower()


def load(repo: str) -> list[Fact]:
    """Facts for one repo with human review verdicts applied (rejected facts are dropped)."""
    path = FACTS_DIR / f"{repo}.json"
    if not path.exists():
        return []
    facts = [Fact(**f) for f in json.loads(path.read_text())["facts"]]
    verdicts = json.loads(REVIEW.read_text()).get(repo, {}) if REVIEW.exists() else {}
    out = []
    for f in facts:
        v = verdicts.get(f.id)
        if v is None:
            out.append(f)
        elif v["verdict"] == "accept":
            out.append(Fact(**{**asdict(f), "review": "accepted"}))
        elif v["verdict"] == "correct":
            out.append(Fact(**{**asdict(f), "expected": v["value"], "review": "corrected"}))
    return out


def predict(f: Fact, p: dict[str, dict[str, Any]]) -> Any:
    """What P1 reported for this fact; p maps A1..A11 to artifact payloads."""
    a1, a3, a4, a5 = (p.get(k, {}) for k in ("A1", "A3", "A4", "A5"))
    deps = [str(d.get("name", "")).lower() for d in a1.get("dependencies", [])]
    sources = [str(d.get("source", "")).lower() for d in a1.get("dependencies", [])]
    resources = [str(r.get("path", "")).lower() for r in a4.get("resources", [])]
    t: Callable[[], str] = lambda: _text(a1, a3, a4, p.get("A6", {}), p.get("A11", {}))  # noqa: E731
    match f.type:
        case "primary_language":
            return (a1.get("repositories") or [{}])[0].get("primary_language")
        case "framework":
            return f.expected if any(str(f.expected) in d for d in deps) else None
        case "dependency" | "test_framework":
            art = f.key.rsplit(":", 1)[-1]
            return any(f.key in d or d.endswith(":" + art) or d == art for d in deps)
        case "build_manifest":
            if f.key == "*.csproj":
                return any(s.endswith(".csproj") for s in sources) or ".csproj" in t()
            return any(s.rsplit("/", 1)[-1] == f.key for s in sources) or f.key in t()
        case "has_tests":
            return ((a1.get("repositories") or [{}])[0].get("test_files") or 0) > 0
        case "datastore":
            return bool(re.search(DATASTORES[f.key], t()))
        case "has_data_layer":
            return bool(a3.get("entities") or a3.get("datasets"))
        case "entity":
            blob = _norm(_text([(e.get("name"), e.get("defined_in")) for e in a3.get("entities", [])],
                               [d.get("name") for d in a3.get("datasets", [])]))
            return any(form in blob for form in _entity_forms(f.key))
        case "route":
            return _contains_route(f.key, route_candidates(p))
        case "containerized":
            return any("dockerfile" in r for r in resources)
        case "ci":
            return any(CI_RE.search(r) for r in resources)
        case "runtime_version":
            lang, _, ver = str(f.expected).partition(" ")
            hit = (str(f.expected) in t() if not ver else
                   re.search(rf"{re.escape(lang)}\W{{0,12}}(?:se\W{{0,3}}|v)?{re.escape(ver)}\b", t()))
            return f.expected if hit else None
        case "license":
            hit = (re.search(dict(LICENSES)[f.expected], t())
                   or re.search(rf"\b{f.expected}\b[\s-]*(?:v?\d|licen[cs]e)", t()))
            return f.expected if hit else None
        case "capability_route":
            return a5.get("capability_route")
    return None


def score_app(facts: list[Fact], payloads: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for f in facts:
        got = predict(f, payloads)
        rows.append({"type": f.type, "key": f.key, "expected": f.expected, "got": got,
                     "ok": got == f.expected, "review": f.review, "source": f.source})
    return rows
