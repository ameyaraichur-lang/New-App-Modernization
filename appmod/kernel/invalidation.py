"""Invalidation engine (AH06 / H17).

Blueprint: 'A late upstream decision/build/schema/checkpoint change cannot
reuse stale downstream permission.' When an upstream artifact is superseded
by a new version, every artifact whose parent lineage includes an older
version is STALE; affected approvals/handoffs must be re-run. Old records
stay in the audit trail — nothing is silently edited.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from appmod.store.artifact_store import ArtifactStore


@dataclass
class InvalidationRecord:
    origin: tuple[str, int]                    # (artifact_id, superseded version)
    new_version: int
    stale: list[dict[str, Any]] = field(default_factory=list)   # descendant pointers


class InvalidationEngine:
    def __init__(self, store: ArtifactStore):
        self.store = store

    def supersede(self, artifact_id: str) -> InvalidationRecord:
        """Announce that `artifact_id` gained a new version. Everything
        transitively consuming any OLDER version is stale."""
        versions = self.store.versions(artifact_id)
        if len(versions) < 2:
            # nothing superseded yet
            return InvalidationRecord(
                (artifact_id, versions[-1] if versions else 0),
                versions[-1] if versions else 0,
                [],
            )
        latest = versions[-1]
        stale: dict[tuple[str, int], dict[str, Any]] = {}
        for older in versions[:-1]:
            for desc in self.store.descendants_of(artifact_id, older):
                stale.setdefault(
                    (desc["artifact_id"], desc["artifact_version"]), desc
                )
        return InvalidationRecord((artifact_id, latest - 1), latest, list(stale.values()))

    def stale_for_run(self, run_id: str, record: InvalidationRecord) -> list[str]:
        return [d["artifact_id"] for d in record.stale if d.get("run_id") == run_id]
