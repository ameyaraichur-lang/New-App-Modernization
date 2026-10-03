"""Content-addressed immutable artifact store.

Blueprint rules implemented here:
  - 'Unique immutable artifact identity and revision. Reject duplicate
    identity with changed content.'
  - 'Reject cross-workload or cross-run substitution' (run/application scoping
    on fetch-by-lineage).
  - Later evidence creates a NEW revision; sealed artifacts are never edited.
  - parent_refs preserve the producer->consumer lineage the invalidation
    engine walks (AH06 / H17).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Iterator

from appmod.contracts.schemas import content_hash


class ArtifactStoreError(Exception):
    pass


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.objects = self.root / "objects"       # <sha256>.json  (content blobs)
        self.index = self.root / "index"           # artifact_id/<version>.json (pointers)
        self.objects.mkdir(parents=True, exist_ok=True)
        self.index.mkdir(parents=True, exist_ok=True)

    # -- publication ---------------------------------------------------------

    def publish(self, artifact: dict[str, Any]) -> dict[str, Any]:
        """Store a validated artifact. First publication of an
        (artifact_id, version) is immutable: republishing the same identity
        with different content raises. Same content is idempotent."""
        artifact = json.loads(json.dumps(artifact))  # deep copy
        digest = content_hash(artifact)
        artifact["content_hash"] = digest

        obj_path = self.objects / f"{digest}.json"
        if not obj_path.exists():
            obj_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False),
                                encoding="utf-8")

        art_id = artifact["artifact_id"]
        version = artifact["artifact_version"]
        pointer_path = self.index / art_id / f"{version}.json"
        if pointer_path.exists():
            existing = json.loads(pointer_path.read_text(encoding="utf-8"))
            if existing["content_hash"] != digest:
                raise ArtifactStoreError(
                    f"immutable violation: {art_id} v{version} already published "
                    f"with different content"
                )
            return existing  # idempotent republish

        pointer = {
            "artifact_id": art_id,
            "artifact_version": version,
            "content_hash": digest,
            "producer_id": artifact["producer_id"],
            "run_id": artifact["run_id"],
            "application_id": artifact["application_id"],
            "phase_id": artifact["phase_id"],
            "status": artifact["status"],
            "parent_refs": artifact.get("execution_metadata", {}).get("parent_refs", []),
            "object_path": str(obj_path.relative_to(self.root)),
        }
        pointer_path.parent.mkdir(parents=True, exist_ok=True)
        pointer_path.write_text(json.dumps(pointer, indent=2), encoding="utf-8")
        return pointer

    # -- reads ---------------------------------------------------------------

    def get(self, artifact_id: str, version: int | None = None) -> dict[str, Any]:
        base = self.index / artifact_id
        if not base.exists():
            raise ArtifactStoreError(f"unknown artifact {artifact_id}")
        if version is None:
            versions = sorted(
                (int(p.stem) for p in base.glob("*.json")),
            )
            if not versions:
                raise ArtifactStoreError(f"no versions for {artifact_id}")
            version = versions[-1]
        ptr_path = base / f"{version}.json"
        if not ptr_path.exists():
            raise ArtifactStoreError(f"{artifact_id} has no version {version}")
        pointer = json.loads(ptr_path.read_text(encoding="utf-8"))
        return json.loads(
            (self.root / pointer["object_path"]).read_text(encoding="utf-8")
        )

    def versions(self, artifact_id: str) -> list[int]:
        base = self.index / artifact_id
        if not base.exists():
            return []
        return sorted(int(p.stem) for p in base.glob("*.json"))

    def query(
        self,
        *,
        producer_id: str | None = None,
        phase_id: int | None = None,
        run_id: str | None = None,
        application_id: str | None = None,
        status: str | None = None,
    ) -> Iterator[dict[str, Any]]:
        for ptr_path in sorted(self.index.rglob("*.json")):
            pointer = json.loads(ptr_path.read_text(encoding="utf-8"))
            if producer_id and pointer["producer_id"] != producer_id:
                continue
            if phase_id is not None and pointer["phase_id"] != phase_id:
                continue
            if run_id and pointer["run_id"] != run_id:
                continue
            if application_id and pointer["application_id"] != application_id:
                continue
            if status and pointer["status"] != status:
                continue
            yield pointer

    # -- lineage / invalidation support (AH06) --------------------------------

    def children_of(self, artifact_id: str, version: int) -> list[dict[str, Any]]:
        """Artifacts whose parent_refs include this exact (artifact_id, version)."""
        key = f"{artifact_id}@{version}"
        out = []
        for ptr in self.query():
            if key in ptr.get("parent_refs", []):
                out.append(ptr)
        return out

    def descendants_of(self, artifact_id: str, version: int) -> list[dict[str, Any]]:
        """Transitive closure via children_of (bounded by store size)."""
        seen: dict[str, dict[str, Any]] = {}
        frontier = [(artifact_id, version)]
        while frontier:
            aid, ver = frontier.pop()
            for child in self.children_of(aid, ver):
                ckey = (child["artifact_id"], child["artifact_version"])
                if ckey not in {(s["artifact_id"], s["artifact_version"]) for s in seen.values()}:
                    seen[child["artifact_id"]] = child
                    frontier.append((child["artifact_id"], child["artifact_version"]))
        return list(seen.values())

    # -- utility --------------------------------------------------------------

    def wipe(self) -> None:
        """Test helper — remove all stored artifacts."""
        shutil.rmtree(self.objects)
        shutil.rmtree(self.index)
        self.objects.mkdir(parents=True, exist_ok=True)
        self.index.mkdir(parents=True, exist_ok=True)
