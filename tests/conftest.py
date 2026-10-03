"""Shared fixtures: compiled registry (module-scoped)."""

from pathlib import Path

import pytest

from appmod.registry.compiler import resolve_registry


@pytest.fixture(scope="session")
def registry():
    return resolve_registry()


@pytest.fixture()
def tmp_store(tmp_path):
    from appmod.store.artifact_store import ArtifactStore
    return ArtifactStore(tmp_path / "store")
