"""appmod — executable App Modernization pipeline (blueprint v3 Review).

Layers:
  registry   — blueprint XLSX -> canonical machine registry (+ parity checks)
  contracts  — IA04 canonical envelope + payload JSON Schemas + validators
  store      — content-addressed immutable artifact store
  kernel     — orchestrator: DAG scheduler, gate service, invalidation engine,
               policy service, audit journal, run engine
  agents     — agent runtime harness (charter, tool allowlist, output validator)
"""

__version__ = "0.1.0"
