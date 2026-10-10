"""Code retrieval: syntax-aware chunks + Astra embeddings + cosine search.

Chunks follow top-level definitions (tree-sitter) for the main languages and
fall back to overlapping line windows. Vectors come from the embedding tier
(text-embedding-ada-002, 1536-d) and are persisted per repo fingerprint under
``runs/index``. Without Astra the index degrades to lexical (token-overlap)
scoring so tools still answer — the result says which mode served it.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import threading
from pathlib import Path
from typing import Any

import numpy as np

from appmod.config import get_settings

CHUNK_LINES = 80
TS_LANGS = {".py": "python", ".java": "java", ".js": "javascript", ".ts": "typescript",
            ".tsx": "tsx", ".go": "go", ".rb": "ruby", ".php": "php", ".cs": "csharp"}
TEXT_EXT = set(TS_LANGS) | {".html", ".sql", ".kt", ".scala", ".yml", ".yaml", ".xml",
                            ".properties", ".jsx", ".vue", ".sh"}
MAX_CHUNKS = 2500

_indexes: dict[str, "CodeIndex"] = {}
_lock = threading.Lock()


def _tokens(text: str) -> list[str]:
    parts = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text)
    out = []
    for p in parts:
        out.extend(x.lower() for x in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", p) or [p])
        out.append(p.lower())
    return out


def chunk_file(rel: str, text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    if not lines:
        return []
    spans: list[tuple[int, int]] = []
    lang = TS_LANGS.get(Path(rel).suffix.lower())
    if lang:
        try:
            from tree_sitter_language_pack import get_parser
            tree = get_parser(lang).parse(text.encode("utf-8", "ignore"))
            cur_s, cur_e = None, None
            for node in tree.root_node.children:
                s, e = node.start_point[0], node.end_point[0]
                if cur_s is None:
                    cur_s, cur_e = s, e
                elif e - cur_s + 1 <= CHUNK_LINES:
                    cur_e = e
                else:
                    spans.append((cur_s, cur_e))
                    cur_s, cur_e = s, e
            if cur_s is not None:
                spans.append((cur_s, cur_e))
        except Exception:
            spans = []
    if not spans:
        spans = [(i, min(i + CHUNK_LINES, len(lines)) - 1) for i in range(0, len(lines), CHUNK_LINES - 10)]
    out = []
    for s, e in spans:
        for ss in range(s, e + 1, CHUNK_LINES):     # split oversized top-level nodes
            ee = min(e, ss + CHUNK_LINES - 1)
            body = "\n".join(lines[ss:ee + 1]).strip()
            if body:
                out.append({"path": rel, "start": ss + 1, "end": ee + 1, "text": body[:6000]})
    return out


class CodeIndex:
    def __init__(self, root: Path):
        from appmod.tools.builtin import _scan
        self.root = Path(root).resolve()
        scan = _scan(self.root)
        self.commit = scan.commit
        chunks: list[dict[str, Any]] = []
        for f in scan.files:
            if Path(f["path"]).suffix.lower() not in TEXT_EXT or f["bytes"] > 400_000:
                continue
            try:
                text = (self.root / f["path"]).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            chunks.extend(chunk_file(f["path"], text))
            if len(chunks) >= MAX_CHUNKS:
                break
        self.chunks = chunks[:MAX_CHUNKS]
        self.vectors: np.ndarray | None = None
        self.mode = "lexical"
        self._df: dict[str, int] = {}
        self._toks = [set(_tokens(c["path"] + " " + c["text"])) for c in self.chunks]
        for t in self._toks:
            for w in t:
                self._df[w] = self._df.get(w, 0) + 1
        self._embed()

    def _cache_path(self) -> Path:
        key = hashlib.sha256(f"{self.root}|{self.commit}|{len(self.chunks)}".encode()).hexdigest()[:24]
        return get_settings().runs_dir / "index" / key

    def _embed(self) -> None:
        s = get_settings()
        if not s.llm_enabled or not self.chunks:
            return
        base = self._cache_path()
        npy, meta = base.with_suffix(".npy"), base.with_suffix(".json")
        if npy.exists() and meta.exists():
            self.vectors = np.load(npy)
            self.mode = "embedding"
            return
        try:
            from appmod.llm.astra import AstraClient
            texts = [f"{c['path']} L{c['start']}-{c['end']}\n{c['text']}" for c in self.chunks]
            vecs = np.array(AstraClient(s).embed(texts), dtype=np.float32)
        except Exception:
            return   # lexical fallback; search() reports the mode
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9
        base.parent.mkdir(parents=True, exist_ok=True)
        np.save(npy, vecs)
        meta.write_text(json.dumps({"root": str(self.root), "commit": self.commit,
                                    "chunks": len(self.chunks)}))
        self.vectors = vecs
        self.mode = "embedding"

    def search(self, query: str, k: int = 8) -> list[dict[str, Any]]:
        if not self.chunks:
            return []
        if self.vectors is not None:
            from appmod.llm.astra import AstraClient
            q = np.array(AstraClient().embed([query])[0], dtype=np.float32)
            q /= np.linalg.norm(q) + 1e-9
            scores = self.vectors @ q
        else:
            qt = set(_tokens(query))
            n = len(self.chunks)
            scores = np.array([sum(math.log(1 + n / self._df[w]) for w in qt & t) for t in self._toks])
        top = np.argsort(-scores)[:k]
        return [{"path": self.chunks[i]["path"], "lines": f"{self.chunks[i]['start']}-{self.chunks[i]['end']}",
                 "score": round(float(scores[i]), 4), "mode": self.mode,
                 "snippet": self.chunks[i]["text"][:1500]} for i in top if scores[i] > 0]


NEAR_DUPLICATE = 0.92


def app_similarity(roots: dict[str, Path], top: int = 3) -> dict[str, Any]:
    """Pairwise code similarity between applications from their chunk embeddings.

    ``overlap`` is the share of the smaller app's chunks whose best match in the
    other app reaches NEAR_DUPLICATE (copied code); ``mean_best_match`` is the
    mean best-match cosine of those chunks (same capability, any language);
    ``centroid_cosine`` compares whole-app profiles. Lexical mode (no Astra)
    uses token-set Jaccard instead.
    """
    idx = {app: get_index(r) for app, r in sorted(roots.items())}
    mode = "embedding" if all(i.vectors is not None for i in idx.values()) else "lexical"
    apps = list(idx)
    pairs = []
    for i, a in enumerate(apps):
        for b in apps[i + 1:]:
            ia, ib = idx[a], idx[b]
            if not ia.chunks or not ib.chunks:
                continue
            if mode == "embedding":
                sim = ia.vectors @ ib.vectors.T
                small_axis = 1 if len(ia.chunks) <= len(ib.chunks) else 0
                best = sim.max(axis=small_axis)
                ca, cb = ia.vectors.mean(axis=0), ib.vectors.mean(axis=0)
                centroid = float(ca @ cb / (np.linalg.norm(ca) * np.linalg.norm(cb) + 1e-9))
                overlap = float((best >= NEAR_DUPLICATE).mean())
                mean_best = float(best.mean())
                flat = np.argsort(-sim, axis=None)[:top]
                matches = [{"a": f"{ia.chunks[x]['path']}:{ia.chunks[x]['start']}",
                            "b": f"{ib.chunks[y]['path']}:{ib.chunks[y]['start']}",
                            "cosine": round(float(sim[x, y]), 4)}
                           for x, y in (np.unravel_index(f, sim.shape) for f in flat)]
            else:
                ta, tb = set().union(*ia._toks), set().union(*ib._toks)
                centroid = len(ta & tb) / max(1, len(ta | tb))
                overlap, mean_best, matches = centroid, centroid, []
            pairs.append({"apps": [a, b], "overlap": round(overlap, 4),
                          "mean_best_match": round(mean_best, 4),
                          "centroid_cosine": round(centroid, 4), "top_matches": matches})
    pairs.sort(key=lambda p: (-p["overlap"], -p["mean_best_match"]))
    return {"mode": mode, "near_duplicate_threshold": NEAR_DUPLICATE, "pairs": pairs}


def get_index(root: Path) -> CodeIndex:
    key = str(Path(root).resolve())
    with _lock:
        idx = _indexes.get(key)
        if idx is None:
            idx = _indexes[key] = CodeIndex(Path(root))
        return idx
