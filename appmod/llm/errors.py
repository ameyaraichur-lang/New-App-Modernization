"""LLM error taxonomy. Transient errors are retried/failed over; the rest are terminal."""

from __future__ import annotations


class LLMError(RuntimeError):
    pass


class LLMConfigError(LLMError):
    """Missing endpoint/key/deployment — never retried."""


class TransientLLMError(LLMError):
    def __init__(self, msg: str, retry_after: float | None = None):
        super().__init__(msg)
        self.retry_after = retry_after


class DeploymentUnavailableError(LLMError):
    """Deployment missing/not found — eligible for tier failover, not retry."""


class ContentFilteredError(LLMError):
    """Provider content filter rejected the prompt or completion."""


class ContextLengthError(LLMError):
    """Prompt exceeds the deployment context window."""


class ReplayMissError(LLMError):
    """Cache in replay mode and the exact request was never recorded."""
