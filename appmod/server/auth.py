"""Bearer-token auth with roles.

Roles: viewer (read), operator (start/cancel/resume/rerun runs), reviewer
(release-gate decisions), stakeholder (answer A8 questions), admin (all).
Tokens come from ``APPMOD_API_TOKENS`` ("tok=user:role1,role2;..."). With
auth enabled and no tokens configured, an admin token is generated once into
``runs/.admin_token`` (mode 600) — it is never logged or returned by the API.
"""

from __future__ import annotations

import os
import secrets
import threading
from dataclasses import dataclass, field

from fastapi import HTTPException, Request

from appmod.config import get_settings

ROLES = ("viewer", "operator", "reviewer", "stakeholder", "admin")


@dataclass(frozen=True)
class Principal:
    user: str
    roles: frozenset[str] = field(default_factory=frozenset)

    def has(self, role: str) -> bool:
        return "admin" in self.roles or role in self.roles or role == "viewer"


ANON_ADMIN = Principal("local", frozenset({"admin"}))
_tokens: dict[str, Principal] | None = None
_lock = threading.Lock()


def _parse(spec: str) -> dict[str, Principal]:
    out = {}
    for entry in spec.split(";"):
        if "=" not in entry:
            continue
        tok, rest = entry.split("=", 1)
        user, _, roles = rest.partition(":")
        rs = frozenset(r.strip() for r in roles.split(",") if r.strip() in ROLES) or frozenset({"viewer"})
        out[tok.strip()] = Principal(user.strip() or "user", rs)
    return out


def tokens() -> dict[str, Principal]:
    global _tokens
    with _lock:
        if _tokens is None:
            s = get_settings()
            _tokens = _parse(s.api_tokens)
            if not _tokens and s.auth_mode == "token":
                path = s.runs_dir / ".admin_token"
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                    with os.fdopen(fd, "w") as fh:
                        fh.write(secrets.token_urlsafe(32))
                _tokens = {path.read_text().strip(): Principal("admin", frozenset({"admin"}))}
        return _tokens


def reset() -> None:
    global _tokens
    with _lock:
        _tokens = None


def principal(request: Request) -> Principal:
    if get_settings().auth_mode == "none":
        return ANON_ADMIN
    hdr = request.headers.get("authorization", "")
    tok = hdr[7:].strip() if hdr.lower().startswith("bearer ") else request.query_params.get("token", "")
    p = tokens().get(tok) if tok else None
    if p is None:
        raise HTTPException(401, "missing or invalid bearer token",
                            headers={"WWW-Authenticate": "Bearer"})
    return p


def require(role: str):
    def dep(request: Request) -> Principal:
        p = principal(request)
        if not p.has(role):
            raise HTTPException(403, f"role {role!r} required")
        return p
    return dep
