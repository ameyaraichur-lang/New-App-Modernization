"""Shared fixtures: compiled registry (module-scoped)."""

import os

if os.environ.get("APPMOD_LIVE") != "1":
    os.environ.setdefault("APPMOD_LLM_MODE", "off")
    os.environ.setdefault("APPMOD_ANALYZERS", "off")

import pytest  # noqa: E402

from appmod.registry.compiler import resolve_registry


@pytest.fixture(scope="session")
def registry():
    return resolve_registry()


@pytest.fixture()
def tmp_store(tmp_path):
    from appmod.store.artifact_store import ArtifactStore
    return ArtifactStore(tmp_path / "store")
