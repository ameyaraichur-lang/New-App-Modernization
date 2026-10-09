"""Content-addressed LLM response cache — the reproducibility mechanism.

Reasoning deployments reject ``temperature``, so determinism comes from
record/replay: the request (deployment, instructions, input items, tools,
effort, format) hashes to a key and the full response is stored on disk.

Modes: ``off`` (never touch), ``read`` (read-through: hit returns, miss calls
and records), ``record`` (always call, overwrite), ``replay`` (hit or raise).
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Any, Callable

from appmod.llm.errors import ReplayMissError
from appmod.llm.types import ModelResponse

MODES = ("off", "read", "record", "replay")


def request_key(request: dict[str, Any]) -> str:
    blob = json.dumps(request, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode()).hexdigest()


class ResponseCache:
    def __init__(self, root: Path, mode: str = "read"):
        if mode not in MODES:
            raise ValueError(f"cache mode must be one of {MODES}")
        self.root = Path(root)
        self.mode = mode
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def _path(self, key: str) -> Path:
        return self.root / key[:2] / f"{key}.json"

    def get_or_call(self, request: dict[str, Any],
                    call: Callable[[], ModelResponse]) -> ModelResponse:
        if self.mode == "off":
            return call()
        key = request_key(request)
        path = self._path(key)
        if self.mode in ("read", "replay") and path.exists():
            with self._lock:
                self.hits += 1
            resp = ModelResponse.from_json(json.loads(path.read_text()))
            resp.cached = True
            return resp
        if self.mode == "replay":
            raise ReplayMissError(f"no recorded response for request {key[:16]}")
        with self._lock:
            self.misses += 1
        resp = call()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(resp.to_json(), sort_keys=True))
        os.replace(tmp, path)
        return resp
