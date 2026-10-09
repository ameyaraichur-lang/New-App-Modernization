"""Runtime settings: environment + `.env` (never committed).

Secrets are `SecretStr` and are masked by `redact()` / `RedactingFilter`
wherever text may reach logs, artifacts, audit lines or the model.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"), env_prefix="APPMOD_", extra="ignore",
    )

    # Astra (Azure OpenAI, Responses API)
    astra_endpoint: str = ""
    astra_api_version: str = "2025-04-01-preview"
    astra_api_key: SecretStr = SecretStr("")
    astra_deployment: str = "gpt-6-astra"
    astra_model_version: str = ""

    # model tiers -> deployments
    tier_reasoning: str = ""
    tier_coding: str = "gpt-5.3-codex-PlayWright"
    tier_fast: str = "gpt-4.1-mini"
    tier_fallback: str = "gpt-5.4"
    tier_embedding: str = "text-embedding-ada-002"

    llm_mode: str = "auto"            # auto (use Astra when configured) | off
    llm_cache: str = "read"           # off | read | record | replay
    llm_timeout_s: float = 240.0
    llm_tpm_limit: int = 400_000      # client-side tokens-per-minute ceiling
    max_parallel_agents: int = 4

    # API
    auth_mode: str = "token"          # token | none
    api_tokens: str = ""              # "token=user:role1,role2;token2=user2:role"
    repo_roots: str = ""              # os.pathsep-separated allowlist ("" = any local dir)
    git_hosts: str = "github.com,gitlab.com"
    max_active_runs_per_user: int = 3

    runs_dir: Path = ROOT / "runs"
    tools_dir: Path = ROOT / ".tools" / "bin"

    @property
    def astra_configured(self) -> bool:
        return bool(self.astra_endpoint and self.astra_api_key.get_secret_value())

    @property
    def llm_enabled(self) -> bool:
        return self.llm_mode != "off" and self.astra_configured

    @property
    def reasoning_deployment(self) -> str:
        return self.tier_reasoning or self.astra_deployment

    def deployment_for(self, tier: str) -> str:
        return {
            "reasoning": self.reasoning_deployment,
            "coding": self.tier_coding,
            "fast": self.tier_fast,
            "fallback": self.tier_fallback,
            "embedding": self.tier_embedding,
        }.get(tier, self.reasoning_deployment)

    def secret_values(self) -> list[str]:
        vals = [self.astra_api_key.get_secret_value()]
        vals += [t.split("=", 1)[0] for t in self.api_tokens.split(";") if "=" in t]
        return [v for v in vals if v and len(v) >= 8]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    tools = str(s.tools_dir)
    if tools not in os.environ.get("PATH", ""):
        os.environ["PATH"] = tools + os.pathsep + os.environ.get("PATH", "")
    return s


def redact(text: str, settings: Settings | None = None) -> str:
    s = settings or get_settings()
    for v in s.secret_values():
        text = text.replace(v, "[REDACTED]")
    return text


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact(str(record.msg))
        if record.args:
            record.args = tuple(redact(str(a)) for a in record.args)
        return True


def install_log_redaction() -> None:
    f = RedactingFilter()
    for name in ("", "uvicorn", "uvicorn.access", "uvicorn.error", "httpx", "openai"):
        logging.getLogger(name).addFilter(f)
