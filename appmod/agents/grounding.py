"""Grounding checks for model claims against the pinned repository snapshot.

Shared by the agent loop (claims that fail become repairable submission problems) and by
``scripts/eval_run.py`` (Step 33: hallucinated paths/symbols must be 0)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

FILE_EXTS = ("java|kt|groovy|gradle|xml|properties|ya?ml|json|toml|ini|cfg|conf|env|py|rb|php|go|mod|sum|"
             "js|jsx|ts|tsx|mjs|cjs|vue|cs|csproj|sln|props|targets|cshtml|razor|html?|css|scss|less|sql|"
             "sqlite|db|md|txt|rst|lock|sh|ps1|cmd|bat|tf|jsp|twig|erb|slim|map|log")
PATH_RE = re.compile(rf"(?<![\w/.:-])((?:[\w@.-]+/)+[\w.-]+\.(?:{FILE_EXTS}))(?![\w/])", re.I)
_EXT_SUFFIX = re.compile(rf"\.(?:{FILE_EXTS})$", re.I)
SYMBOL_RE = re.compile(r"^[A-Za-z_$][\w$]*$")
TEXT_SKIP = {".git", "node_modules", "bower_components", "vendor", "dist", "obj", "bin"}
GROUNDED_CLASSES = ("OBSERVED", "DOCUMENTED")
# Prose often lists ``Dockerfile`` and a script as ``Dockerfile/boot.sh``.
STANDALONE_PATH_SEGMENTS = frozenset({"Dockerfile", "Containerfile", "Makefile", "Jenkinsfile", "Gemfile"})


class RepoIndex:
    _cache: dict[Path, RepoIndex] = {}

    def __init__(self, root: Path):
        self.root = root
        self.files = [p.relative_to(root).as_posix() for p in root.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(root).parts]
        self.dirs = {Path(f).parent.as_posix() for f in self.files}
        self._text: str | None = None

    @classmethod
    def of(cls, root: Path) -> RepoIndex:
        root = Path(root).resolve()
        if root not in cls._cache:
            cls._cache[root] = cls(root)
        return cls._cache[root]

    @property
    def text(self) -> str:
        if self._text is None:
            parts = []
            for f in self.files:
                p = self.root / f
                if not (set(Path(f).parts) & TEXT_SKIP) and p.stat().st_size < 1_000_000:
                    parts.append(p.read_text("utf-8", "ignore"))
            self._text = "\n".join(parts)
        return self._text

    def has_path(self, token: str) -> bool:
        """A file or directory in the snapshot, or a runtime path the code itself names —
        literally (``./data/gorm.db``) or by parts (``storage_path('logs/laravel.log')``,
        ``os.path.join(app.instance_path, "flaskr.sqlite")``)."""
        t = re.sub(rf"^(\./|{re.escape(self.root.name)}/)", "", token)
        if any(f == t or f.endswith("/" + t) for f in self.files):
            return True
        tl = t.lower()
        if any(f.lower() == tl or f.lower().endswith("/" + tl) for f in self.files):
            return True
        if any(d == t or d.endswith("/" + t) for d in self.dirs):
            return True
        if any(d.lower() == tl or d.lower().endswith("/" + tl) for d in self.dirs):
            return True
        if t in self.text:
            return True
        *dirs, base = t.split("/")
        return base in self.text and all(re.search(rf"\b{re.escape(d)}", self.text) for d in dirs)

    def has_symbol(self, name: str, file: str | None = None) -> bool:
        pat = re.compile(rf"(?<![\w$]){re.escape(name)}(?![\w$])")
        if file:
            p = (self.root / file).resolve()
            if p.is_file() and p.is_relative_to(self.root) and pat.search(p.read_text("utf-8", "ignore")):
                return True
        return pat.search(self.text) is not None


def strings(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def walk(obj: Any) -> Iterable[dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def split_compound_path(token: str) -> list[str]:
    """Split prose that lists files back-to-back (``auth.py/blog.py``) into separate paths."""
    if "/" not in token:
        return [token]
    parts = token.split("/")
    out: list[str] = []
    cur: list[str] = []
    for part in parts:
        cur.append(part)
        if _EXT_SUFFIX.search(part) or part in STANDALONE_PATH_SEGMENTS:
            out.append("/".join(cur))
            cur = []
    if cur:
        out.append("/".join(cur))
    return out or [token]


def path_tokens(obj: Any) -> list[str]:
    seen: list[str] = []
    for s in strings(obj):
        for tok in PATH_RE.findall(s):
            for piece in split_compound_path(tok):
                if piece not in seen and not (piece.startswith(("http", "www.")) or re.match(r"^\d", piece)):
                    seen.append(piece)
    return seen


def grounded_claims(findings: list[dict[str, Any]], payload: dict[str, Any], phase: int) -> list[Any]:
    """Claims that must name only real paths: all of a P1 payload (discovery is observational)
    plus OBSERVED/DOCUMENTED findings and payload items in every phase."""
    claims: list[Any] = [payload] if phase == 1 else []
    claims += [i for i in walk([findings, payload]) if i.get("evidence_class") in GROUNDED_CLASSES]
    return claims


def ungrounded_paths(index: RepoIndex, claims: list[Any]) -> list[str]:
    return [t for t in path_tokens(claims) if not index.has_path(t)]


def check_function_names(payload: dict[str, Any], index: RepoIndex,
                         keys: tuple[str, ...] = ("processes", "business_rules")) -> list[str]:
    """Verify ``function`` fields name declared code symbols; unverifiable names are removed."""
    problems: list[str] = []
    for key in keys:
        for it in payload.get(key) or []:
            if not isinstance(it, dict):
                continue
            keep = []
            for name in (n.strip() for n in re.split(r"[;,]", str(it.get("function") or ""))):
                if not name:
                    continue
                leaf = re.split(r"::|->|#|\.", re.sub(r"\(.*", "", name))[-1].strip()
                if not SYMBOL_RE.match(leaf):
                    problems.append(f"{key}: function {name!r} is not a declared code name — list exact "
                                    "names only, or '' for an anonymous handler")
                elif not index.has_symbol(leaf, it.get("file")):
                    problems.append(f"{key}: function {name!r} not found in {it.get('file') or 'the repo'}")
                else:
                    keep.append(name)
            it["function"] = "; ".join(keep)
    return problems
