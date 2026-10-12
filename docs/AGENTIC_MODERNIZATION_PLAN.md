# Agentic Modernization Plan — New-App-Modernization

**Status:** proposal · **Baseline analyzed:** commit `ef6b5a1` (single commit, `main`) · **Date:** 2026-10-09

This document is the result of an end-to-end analysis of the repository (every Python module, the
React console, the compiled registry, the test suite, and a live P1→P6 run) and a complete plan for
turning the pipeline into a *true agentic* system: real LLM reasoning, tool use, human-in-the-loop
approvals, durable long-running execution, and an interactive agent experience in the console.

---

## 1. Executive summary

**What the repo is today:** a well-engineered *governance kernel* (DAG scheduler, deterministic gates,
contract validation, an immutable content-addressed artifact store, an audit journal, and an
invalidation engine), compiled from a 78-role blueprint. It runs Phases 1–6 against any repo.

**What it is not (yet):** agentic. **There are zero model calls anywhere in the codebase.** Every
one of the 56 executable "agents" (P1–P6) is a hand-written Python function that either computes
facts with regex/file scanning or returns templated text. Verified evidence:

- `grep` for `openai|anthropic|llm|prompt` finds only comments; `build_charter()` and `ToolSandbox`
  in `appmod/agents/runtime.py` are **defined but never called**.
- A full P1→P6 run on a 45k-LOC repo completes in **3.8 seconds** and every release gate passes.
- P1 `A11` risk scores are hard-coded to `3` for every dimension; P3 `A4` emits the same two
  threats for every repo; P4 `A9` cross-plan checks are hard-coded `PASS`; P5 lanes write
  "change manifests" and never touch code; every human (stakeholders, reviewers, permit issuers) is
  simulated.
- The only *real* work: repo scanning (P1), and an actual SQLite row-copy + count/checksum
  reconciliation (P6 X1/A9).

**The good news:** the architecture was explicitly designed for LLM agents to plug in. The
`AgentRunner` protocol (`run(agent_spec, inputs, policy) -> AgentOutcome`) is the seam, the registry
already holds per-agent charters (activities, inputs, outputs, non-negotiable contract rules) and
typed payload contracts for **all 78 roles**, and the kernel — not the model — validates, publishes
and gates. That is exactly the right shape for safe agentic systems. We keep the kernel and gates
deterministic and replace the *runners* with LLM-driven, tool-using agents.

**Recommended path (7 stages, ~14–18 engineer-weeks for P1–P6 with 2–3 engineers):**

| Stage | Outcome |
|---|---|
| 0. Foundations & fixes | Fix defects found in analysis, pin Python 3.12, config/secrets, CI |
| 1. LLM connectivity + agent runtime | Provider-agnostic model client, tool-calling loop, structured output via `submit_outcome`, repair loop, record/replay |
| 2. Tool gateway + external analyzers | Sandboxed read-only repo tools + real scanners (scc, Syft, Trivy/OSV, Gitleaks, Semgrep, tree-sitter); evidence binding |
| 3. Human-in-the-loop + durable orchestration | Real approvals at gates, real stakeholder elicitation (A8), pause/resume, parallel dispatch, live event streaming |
| 4. LLM-led reasoning for P2–P4 | Strategy, architecture and planning agents that actually reason over evidence |
| 5. P5 depth 2: real code modernization | Coding agents editing a git worktree in a container sandbox, build/test loop, real differential validation |
| 6. Agentic UX + P6 real connectors (+ P8/P9 later) | Agent trace view, approvals inbox, copilot chat, MCP server; real DB connectors |

Evaluation, observability, cost control and security run across all stages, starting in Stage 1.

---

## 2. Current-state architecture map

```
                       ┌──────────────────────────── React console (ui/) ─────────────────────────┐
                       │ MasterMap · PhaseView (React Flow DAG) · AgentAnatomy · Findings · Runner │
                       │ Runner polls GET /api/runs/{id} every 1.2s                                │
                       └───────────────────────────────┬──────────────────────────────────────────┘
                                                       │ HTTP
appmod/server/api.py (FastAPI, 127.0.0.1:8600) ─ in-memory _jobs dict ─ PipelineJob thread per run
                                                       │
appmod/server/runner.py  PipelineJob._run_all(): hard-wired P1→P2→P3→P4→P5→P6 driver
   │  builds per-phase "briefs" from upstream artifacts, injects simulated permits/approvals
   ▼
appmod/kernel/orchestrator.py  PhaseOrchestrator.step(): ready nodes dispatched SERIALLY
   ├─ scheduler.py      hard-edge readiness, async lanes, blockage propagation
   ├─ gates.py          G0 intake / G1 snapshot seal / G2-G4 release (generic + phase overrides)
   ├─ policy.py         pilot-default policy bundle (rubric, budgets, simulated reviewers)
   ├─ audit.py          append-only JSONL journal
   ├─ invalidation.py   AH06 stale-descendant computation  (NOT wired into runs)
   └─ contracts/schemas.py  envelope + payload JSON Schemas, validator, normalizer
   │
   ├─ AgentRunner.run(spec, upstream, policy) ──▶ phases/p1..p6/engine.py  (deterministic Python)
   │                                               └─ tools/repo_intel.py (regex scanner)
   ▼
appmod/store/artifact_store.py  content-addressed objects/ + index/<artifact_id>/<version>.json
                                                       ▲
appmod/registry/compiler.py ── data/registry/*.json (78 roles, 190 hard edges, 17 master links)
```

### 2.1 Real vs. simulated, by phase

| Phase | Agents | What is real | What is simulated / templated |
|---|---|---|---|
| P1 Discovery | 11 | File inventory, LOC, manifests→deps, regex routes, secret-pattern scan, license detection | A8 stakeholders (simulated), A9 processes = routes renamed, A10 string templates, A11 scores hard-coded `3`, no vuln scan, no SBOM tool |
| P2 Portfolio | 7 | Arithmetic over P1 facts (complexity band, rate card) | 8R disposition = if/else heuristic; value = 4 booleans; runner builds a 1-app portfolio with `languages=3, tests=1` hard-coded |
| P3 Architecture | 8 | — | Target stack from a language→string dict; fixed threat list; NFRs always `UNSET`; A8 consistency loop is a no-op |
| P4 Planning | 9 | — | Fixed 4-task DAG for every app; A9 checks hard-coded `PASS` |
| P5 Code | 9 | — | No code is read, changed, built or tested; lane checks hard-coded `PASS`; runtime differential `NOT_RUN` |
| P6 Data | 12 | SQLite fixture from seed `INSERT`s, X1 row copy, reject journal, count/checksum reconciliation | Mapping = identity; classification/DQ/disposition templated; A11 flow tests `NOT_RUN` |
| All gates | — | Intake/seal/hash-binding logic | Every reviewer, permit and approval: `simulated: true` |

### 2.2 Strengths to preserve (do not rewrite these)

1. **Kernel-owned publication.** Runners return an `AgentOutcome`; the orchestrator assembles,
   hashes, validates and publishes. Invalid output becomes a stored `FAILED` artifact. This is the
   ideal guardrail for LLM output.
2. **Evidence discipline.** Closed enums for status, evidence class and criteria; `NOT_RUN ≠ PASS`;
   `HYPOTHETICAL` never satisfies human confirmation.
3. **Immutable lineage.** `parent_refs` + content hashes + `InvalidationEngine` give us replay,
   audit and "react to new evidence" almost for free.
4. **Registry-driven charters.** `activities`, `inputs`, `outputs`, `contract_rule`, `merge_tuning`
   per agent, plus run controls (Instruction boundary, Evidence privacy, Access authorization) —
   ready-made system prompts and policy.
5. **Gates are not models.** The blueprint mandates deterministic gates and human authority. Keep it.

---

## 3. Defects and gaps found during analysis

Fix these in Stage 0; several would silently corrupt LLM context later.

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| D1 | High | `tools/repo_intel.py` `LANG_BY_EXT`, `p1/engine.py` A1 | Primary language counts JSON/YAML/Markdown/HTML LOC. Live run on this repo reported **primary: `json`** (45k LOC is mostly registry JSON), so P3 could not pick a target stack. | Separate *code* languages from data/doc/markup; compute primary over code only; replace with `scc`/`tokei` in Stage 2 |
| D2 | High | `server/runner.py` L276–283, L338 | P2 `PortfolioApp(languages=3, tests=1)` and P5 `tests=["inventory"]` hard-coded | Derive from P1 A1 artifact (`languages`, `coverage.test_files`) |
| D3 | High | `p4/engine.py` `_run_a9`, `p5/engine.py` `_lane`/gates, `p3/engine.py` L287–290 | Validation "checks" hard-coded `PASS`; P3 A8 loop computes `art` and discards it | Implement real checks (task↔requirement coverage, context-hash equality, binding resolution) |
| D4 | High | `server/api.py` `POST /api/runs` | No auth; accepts any local path on the host or any git URL (local file disclosure / SSRF once not bound to localhost) | Auth (Stage 3), allowlisted repo roots and git hosts in policy |
| D5 | Medium | `kernel/orchestrator.py` `step()` | Ready nodes run serially; `max_parallel_agents` unused | Bounded parallel dispatch (Stage 3) — essential with LLM latency |
| D6 | Medium | `server/api.py` `_jobs` | Job state is in-memory; server restart loses all runs | Durable run store (Stage 3) |
| D7 | Medium | `kernel/audit.py` | Run control requires *"tool/model/prompt versions"*; not recorded | Add model/prompt/tool/cost fields (Stage 1) |
| D8 | Medium | `kernel/invalidation.py`, `audit.review()`, `budgets.max_revision_cycles` | Implemented but never used at runtime | Wire into re-run and repair flows (Stages 1, 3) |
| D9 | Medium | `agents/runtime.py` `ToolSandbox` | Allowlist only enforced if `allow()` was called; unknown agents pass | Deny-by-default; allowlist from policy (Stage 2) |
| D10 | Medium | Registry payload contracts | 327 of 530 payload fields are `array` with no item schema; 4 `enum` fields with no values | Add item schemas/enums for LLM structured output (Stage 1) |
| D11 | Low | `server/runner.py` `_build_fixture` | Only parses `INSERT INTO t VALUES (…)`; drops real column names (`c0..cn`) | Use `sqlglot` to parse DDL+DML; preserve columns (Stage 6) |
| D12 | Low | `p1/engine.py` L167, L338; `p6/engine.py` L493 | `"NOT_ASSESSED" if False else "UNKNOWN"` dead expressions | Clean up |
| D13 | Low | README vs reality | README says Python 3.12+, suite passes on 3.9; no `pyproject.toml`, no lockfile, no CI | Add `pyproject.toml` (requires-python ≥3.12), `uv` lock, GitLab CI |
| D14 | Low | `server/runner.py` | One unbounded thread per job; no cancellation | Worker pool + cancel endpoint (Stage 3) |

---

## 4. Target architecture

### 4.1 Design principles

1. **LLMs live only inside runners.** Scheduler, validator, store, gates and invalidation stay
   deterministic. A model can *propose*; only the kernel *publishes*; only gates (and humans) *release*.
2. **Hybrid by default.** Deterministic tools produce facts (`OBSERVED`/`DOCUMENTED`); the LLM
   interprets, connects and recommends (`INFERRED`), and must cite the tool calls it relied on.
3. **Evidence is enforced, not requested.** A finding may claim `OBSERVED`/`DOCUMENTED` only if it
   references an evidence record captured by the tool gateway or an upstream artifact hash in this
   run — otherwise the kernel downgrades it to `INFERRED`. `HUMAN_CONFIRMED` can only originate from
   the authenticated approvals service, never from model output.
4. **Policy decides capability.** Per-agent mode (deterministic / hybrid / llm), model tier, tool
   allowlist, token/cost/turn budgets, and data-egress level are versioned policy, recorded in every
   envelope.
5. **Build on the kernel, not a framework.** LangGraph/CrewAI/AutoGen would duplicate the DAG,
   state and gating that already exist and fight the deterministic-gate rule. Use thin provider
   adapters + the official SDKs + MCP for tools.
6. **Reproducible.** Every LLM exchange is cached by `(prompt hash, model, params, tool results
   hash)`; tests and re-runs can replay without network. (The chosen provider, Astra
   `gpt-6-astra`, rejects `temperature`/`top_p`, so replay — not temperature 0 — is the
   reproducibility mechanism.)

> **Provider decided: Astra (Azure OpenAI Responses API).** Verified capabilities, deployment tiers
> and the ordered execution steps are in [`ASTRA_STEP_BY_STEP_PLAN.md`](ASTRA_STEP_BY_STEP_PLAN.md).

### 4.2 Target component diagram

```
┌──────────────────────────────── Console (React) ────────────────────────────────────────────┐
│ Runner · Agent Trace (live tool calls, reasoning summary, cost) · Approvals Inbox ·          │
│ Stakeholder Questionnaire · Copilot Chat · Settings (providers/models, key status)           │
└───────────────┬─────────────────────────── SSE /api/runs/{id}/events ──────────────────────┘
                │ REST (OIDC/session auth)
┌───────────────▼─────────────── appmod/server ─────────────────────────────────────────────┐
│ api.py  · approvals.py · elicitation.py · copilot.py · events.py (SSE)                      │
│ RunService: durable runs (SQLite/Postgres) · worker pool · cancel · resume                  │
└───────────────┬────────────────────────────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────── appmod/kernel (deterministic, unchanged contract) ─────────┐
│ Orchestrator (parallel, pausable) · Scheduler · Gates (+AWAITING_REVIEW) · Policy v2 ·      │
│ Audit (+model/prompt/tool/cost) · Invalidation (wired) · EvidenceValidator (new)            │
└───────────────┬────────────────────────────────────────────────────────────────────────────┘
                │ AgentRunner protocol
┌───────────────▼─────────────── appmod/agents ─────────────────────────────────────────────┐
│ RunnerRouter → per-agent mode from policy                                                    │
│   ├─ DeterministicRunner (existing P1–P6 engines, now also usable as "fact tools")          │
│   └─ LLMAgentRunner: charter → context pack → tool loop → submit_outcome → repair loop      │
│ PromptRegistry (versioned templates) · ContextBuilder (budgeted) · ResponseCache            │
└──────┬──────────────────────────────┬──────────────────────────────────┬────────────────────┘
       │                              │                                  │
┌──────▼───────── appmod/llm ───┐ ┌───▼──────── appmod/tools (gateway) ──────┐ ┌──▼── appmod/retrieval ─┐
│ ModelClient protocol          │ │ deny-by-default allowlist · redaction ·   │ │ code chunk index       │
│  anthropic · openai-compatible│ │ evidence capture (hash every result)      │ │ (sqlite-vec / LanceDB) │
│  (Azure, Bedrock via proxy,   │ │ read-only repo tools · analyzers (CLI) ·  │ │ artifact/semantic      │
│  Ollama/vLLM local)           │ │ sandbox exec (Docker) · MCP client        │ │ search                 │
│ budgets · retries · tracing   │ └───────────────────────────────────────────┘ └────────────────────────┘
└───────────────────────────────┘
```

---

## 5. Workstreams — required modifications in detail

### A. LLM connectivity layer (new `appmod/llm/`)

**Files:** `appmod/llm/__init__.py`, `client.py`, `providers/anthropic.py`,
`providers/openai_compat.py`, `budget.py`, `cache.py`, `errors.py`.

```python
class ModelClient(Protocol):
    def complete(self, *, system: str, messages: list[Message], tools: list[ToolSpec],
                 model: str, max_tokens: int, reasoning_effort: str | None = None,
                 tool_choice: str | None = None) -> ModelResponse: ...
    # ModelResponse: content blocks, tool_calls, stop_reason, usage{in,out,cached}, model_id, latency
```

- **Providers:** native Anthropic SDK and one OpenAI-compatible adapter (`base_url` + key). The
  OpenAI-compatible adapter covers OpenAI, Azure OpenAI, a LiteLLM proxy (→ Bedrock, Vertex), and
  local Ollama/vLLM — the local option matters for code that must not leave the network.
- **Model tiers in policy, not code:** `fast` (extraction, classification), `reasoning`
  (synthesis, strategy, architecture), `coding` (P5 transformations). Model IDs come from env/policy.
- **Error mapping:** rate-limit / 5xx / timeout → `TransientAgentError` (reuses existing bounded
  retries in `orchestrator._handle_transient`); auth/config errors → `FAILED` with a clear gap.
- **Budgets:** per-agent and per-run token and cost ceilings (`budget.py`) enforced before each call;
  exhaustion → `PARTIAL` with an explicit gap, never a silent truncation.
- **Cache / replay:** `cache.py` keyed by SHA-256 of canonical request; modes `off | read | record |
  replay`. `replay` makes CI deterministic and free.
- **Config:** `.env` (already gitignored) + `appmod/config.py` (pydantic-settings):
  `APPMOD_LLM_PROVIDER`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`,
  `APPMOD_MODEL_FAST`, `APPMOD_MODEL_REASONING`, `APPMOD_MODEL_CODING`, `APPMOD_LLM_CACHE`.
- **Dependencies:** `anthropic`, `openai`, `pydantic-settings`, `tenacity` (optional), `tiktoken`
  or provider token counting.

### B. Agent runtime (rework `appmod/agents/`)

**Files:** `runtime.py` (keep protocol), new `llm_runner.py`, `router.py`, `context.py`,
`prompts/` (versioned templates), `repair.py`.

**`RunnerRouter`** implements `AgentRunner`; for each agent it reads policy
`agents["P1.A6"].mode` and dispatches to the deterministic engine, the LLM runner, or both (hybrid).
The orchestrator does not change — it still calls `runner.run(spec, upstream, policy)`.

**`LLMAgentRunner.run()` loop:**

```python
def run(self, spec, inputs, policy) -> AgentOutcome:
    cfg = policy.agent_cfg(spec["id"])                       # mode, tier, tools, budgets, egress
    seed = self.deterministic.run(spec, inputs, policy) if cfg.mode == "hybrid" else None
    system = build_charter(spec, self.phase_name) + prompts.rules(cfg)   # registry charter, versioned
    ctx = ContextBuilder(budget=cfg.context_tokens).pack(inputs, seed)   # upstream artifacts + facts
    tools = self.gateway.specs_for(spec["id"]) + [submit_outcome_tool(spec, self.schemas)]
    transcript = Transcript(system, ctx)
    for turn in range(cfg.max_turns):
        resp = self.model.complete(system=system, messages=transcript.messages, tools=tools,
                                   model=cfg.model, max_tokens=cfg.max_output_tokens,
                                   reasoning_effort=cfg.reasoning_effort)
        transcript.add(resp); self.trace.emit(spec["id"], resp)          # live UI + audit
        if call := resp.tool_call("submit_outcome"):
            outcome = to_agent_outcome(call.input, self.gateway.evidence_log(spec["id"]))
            errors = self.validator.preview(spec, outcome)                 # same rules as _publish
            if not errors:
                return outcome
            transcript.add_tool_result(call, {"validation_errors": errors})  # repair loop,
            continue                                                        # ≤ max_revision_cycles
        for call in resp.tool_calls:
            transcript.add_tool_result(call, self.gateway.invoke(spec["id"], call))
    return budget_exhausted_outcome(seed)                                   # PARTIAL + explicit gap
```

- **Structured output via a terminal tool.** `submit_outcome`'s input schema = `{status, payload,
  findings[], gaps[], evidence_refs[], scope, applicability}` with `payload` = the agent's compiled
  payload schema (`contracts.payload_schema`). Works across all providers with tool calling.
- **Contract tightening (D10):** add `appmod/contracts/overlays/phase_N.json` with item schemas,
  enum values and field descriptions for the fields LLM agents fill (start with P1 and P2). The
  overlay is merged into `payload_schema()`; the frozen registry stays untouched.
- **Hybrid seed:** the existing deterministic engine output is passed in as "pre-computed facts",
  so the LLM enriches instead of re-deriving — cheaper, and facts stay `OBSERVED`.
- **Charter:** `build_charter()` is already written; wire it in, append the policy-specific rules
  and the evidence-citation rule, and version it (`prompt_version` = hash of template + charter).
- **Execution metadata** (envelope `execution_metadata` is an open object, no schema change):
  `runner`, `mode`, `model_id`, `provider`, `prompt_version`, `tool_versions`, `turns`,
  `tokens_in/out`, `cost_usd`, `cache_hit`, `trace_ref`.

### C. Tool gateway + external tool setup (rework `appmod/tools/`)

Replace `ToolSandbox` with a **deny-by-default `ToolGateway`**:

- Allowlist per agent from policy; unknown agent ⇒ no tools. Out-of-allowlist call ⇒ refused,
  logged as an *Instruction boundary* incident (run control already defined).
- Every result is **hashed and recorded** as an evidence record
  `{source: "tool:<name>", ref: <call_id>, content_hash, method, captured_at, access_classification}`
  → returned to the agent as `evidence_id` it must cite.
- Output **redaction** (secrets via Gitleaks rules + existing patterns; optional PII via Presidio)
  before anything reaches the model; size caps and truncation markers.
- Results wrapped as `<evidence source=… id=… hash=…>…</evidence>` so retrieved content is data,
  never instructions.

**Built-in tools (Python, read-only, path-jailed to the pinned repo snapshot):**
`list_dir`, `read_file(path, start, end)`, `grep(pattern, glob)`, `repo_summary` (existing
`scan_repo`), `dependencies` (existing `parse_dependencies`), `git_log`, `git_blame`,
`get_artifact(id)`, `query_store(...)`, `search_code(query)` (retrieval index).

**External analyzers (CLI, run via subprocess with timeouts; versions recorded):**

| Tool | Purpose | Fills gap in | Install |
|---|---|---|---|
| `scc` or `tokei` | Accurate LOC/language/complexity | P1 A1, fixes D1 | `brew install scc` |
| Syft | Real SBOM (CycloneDX/SPDX) | P1 A1 `sbom_ref` | `brew install syft` |
| Trivy **or** OSV-Scanner / Grype | Dependency CVEs | P1 A6 `vulnerability-scan: NOT_ASSESSED` | `brew install trivy` / `osv-scanner` |
| Gitleaks | Secret detection + redaction rules | P1 A6, gateway redaction | `brew install gitleaks` |
| Semgrep (OSS rules) | SAST, framework patterns | P1 A6, P3 A4, P5 A8 | `pip install semgrep` |
| ScanCode Toolkit (optional) | License evidence beyond the LICENSE file | P1 A1/A6 | `pip install scancode-toolkit` |
| tree-sitter (`tree-sitter-language-pack`) | Multi-language import/call graphs (today: Python-only regex) | P1 A2, P3 A2 | `pip install` |
| `sqlglot` | SQL parsing, dialect transpile, schema extraction | P1 A3, P5 A3, P6 A2, D11 | `pip install sqlglot` |
| Checkov / hcl2 | IaC parsing (Dockerfile, k8s, Terraform) | P1 A4, P3 A7 | `pip install checkov` |
| endoflife.date API | LTS/EOL facts for target stacks | P3 A1 | HTTP (policy-gated) |
| OpenRewrite / language codemods | Deterministic upgrades (Java, Spring, etc.) | P5 A2 | Maven/Gradle plugin |
| Docker (or Podman) | Isolated build/test/exec sandbox | P5 A1/A2/A9, P6 A11 | Docker Desktop / Colima |
| Playwright + axe-core | Running-app journeys + accessibility | P1 A7, P5 A4 | `pip install playwright` |
| Presidio (optional) | PII detection on data samples | P6 A3 | `pip install presidio-analyzer` |
| Great Expectations / Soda (optional) | Data-quality rule execution | P6 A4/A10 | `pip install` |

A `scripts/doctor.py` (and `GET /api/health/tools`) reports which tools are installed and their
versions; missing tools produce explicit `NOT_ASSESSED` gaps, never failures that block the run.

**MCP integration (`appmod/tools/mcp_client.py`, MCP Python SDK):** consume MCP servers as
allowlisted tools — GitLab/GitHub (issues, MRs for P5 output), Jira/Linear (task export from P4),
Slack/Teams (A8 elicitation), Datadog/Prometheus/CloudWatch (P1 A4 runtime telemetry, which today
is permanently `NOT_ASSESSED`).

### D. Evidence integrity enforcement (new `appmod/kernel/evidence.py`)

Called from `orchestrator._publish` **before** `ContractValidator.validate`:

1. Each finding's `evidence_refs` must resolve to (a) a gateway evidence record from this node's
   execution, or (b) an upstream artifact `artifact_id@version` in the input manifest.
2. `OBSERVED`/`DOCUMENTED` without a resolvable ref ⇒ downgraded to `INFERRED`, `limitations`
   annotated, audit event `EVIDENCE_DOWNGRADE`.
3. `HUMAN_CONFIRMED` from a model-produced outcome ⇒ downgraded to `HYPOTHETICAL` unless it cites
   an approvals-service record (signed reviewer identity + timestamp).
4. Status sanity: `COMPLETE` with non-empty `gaps` of state `NOT_ASSESSED` ⇒ `PARTIAL`.
5. Secret scan over the whole envelope (run control *Evidence privacy*); a hit quarantines the
   artifact (`FAILED` + incident), mirroring P3 A4's "no secrets in published artifacts" criterion.

### E. Human-in-the-loop (replace simulation with real authority)

- **Gate review state.** Release gates (P1 G2, P2 G2, P3 G2, P4 G2, P5 G0/G4, P6 G1/G3) gain an
  outcome `AWAITING_REVIEW`. The orchestrator persists state and yields; the phase resumes when a
  decision arrives.
- **Approvals API** (`appmod/server/approvals.py`):
  `GET /api/approvals` (inbox), `POST /api/runs/{id}/gates/{phase}/{gate}/decision`
  `{decision, candidate_hash, conditions, comment}`. The decision must match the current candidate
  hash (stale approvals are rejected — the AH06 rule). Reviewer identity from auth;
  `simulated: false`; `audit.review()` (already implemented, unused) records it.
- **A8 Stakeholder Elicitation becomes a real async agent.** The LLM generates targeted questions
  from upstream gaps (e.g. "business criticality", "compliance scope", "data owner"); delivery via
  the console questionnaire and optionally Slack/Teams/email/Jira (MCP). Answers from authenticated
  respondents are `HUMAN_CONFIRMED`; the new A8 version triggers the **InvalidationEngine** so A10,
  A11 and G2 re-run automatically. This is the core "agent reacts to new evidence" loop.
- **Decision mode stays** as an explicit, labeled *simulation* toggle for demos and CI.
- **Auth:** OIDC (Keycloak/Entra ID/Okta) or a simple local session auth for single-user; roles
  `operator`, `reviewer:portfolio|architecture|release`, `stakeholder`, `admin`, mapped from
  `policy.reviewers` (replacing the `simulated` principals).

### F. Orchestration upgrades

- **Parallel dispatch** in `PhaseOrchestrator.step()`: `ThreadPoolExecutor(max_workers =
  policy.budgets.max_parallel_agents)` (or `asyncio`), lock around store pointer writes and audit
  appends. P4's five planners and P1's tier-0 agents gain the most.
- **Durable runs** (`appmod/server/run_store.py`): persist job state, `SchedulerState`, `published`
  map and pending reviews in SQLite (Postgres for multi-user). Server restart ⇒ runs resume.
- **Pause / resume / cancel / re-run node** endpoints; re-run publishes a new version and applies
  invalidation to descendants instead of restarting the whole pipeline.
- **Live events:** `GET /api/runs/{id}/events` (SSE) streaming audit events + agent trace (tool
  calls, model turns, token usage). Replace the 1.2 s polling in `RunnerView.tsx`.
- **Phase driver refactor:** move the hard-wired brief-building in `runner.py` into per-phase
  `handoff.py` adapters that read upstream artifacts (removes D2 and makes multi-app portfolios
  possible in P2).
- **Optional later:** Temporal/Prefect if runs must survive multi-day human waits across hosts;
  the durable SQLite store is sufficient for the pilot.

### G. Context, retrieval and memory

- **ContextBuilder** with token budgets: upstream artifacts summarized by schema (payload fields
  first, findings/gaps next, raw evidence by reference only), deterministic seed facts, and the
  agent's allowlisted tool list. Large repos are explored by tools, not stuffed into the prompt.
- **Code retrieval index** (`appmod/retrieval/`): tree-sitter symbol-aware chunking, embeddings
  (provider or local `bge`/`nomic` via Ollama), stored in `sqlite-vec` or LanceDB under the run dir,
  exposed as the `search_code` tool.
- **Cross-run memory:** the artifact store *is* the memory. Add a "prior runs" tool that lets
  P2/P3 agents look up previous decisions for the same application (by app id + repo commit),
  clearly labeled as historical evidence.

### H. Security and data governance

- **Data egress policy** per engagement: `none` (local models only), `redacted` (code with
  secret/PII redaction), `full`. Enforced in the model client; recorded in every envelope.
- **Prompt injection:** evidence wrapping, charter rule (already present), tool allowlists,
  read-only tools in P1–P4, write tools only inside the P5 worktree sandbox, no network inside the
  sandbox, and incident logging.
- **API hardening (D4):** auth on all `/api` routes, repo-root allowlist and git-host allowlist in
  policy, request size limits, per-user run quotas.
- **Secrets:** keys only from env/secret manager, never in artifacts, logs or traces; key presence
  shown in Settings as "configured / missing".
- **Supply chain:** pin tool versions; record them per run (`tool_versions`).

### I. Observability and cost

- **OpenTelemetry** spans per run → phase → node → model call → tool call, using the GenAI
  semantic conventions; export to **Langfuse** (self-hostable) or Arize Phoenix for LLM traces.
- Audit journal additions (D7): `MODEL_CALL`, `TOOL_CALL`, `EVIDENCE_DOWNGRADE`, `REPAIR`,
  `BUDGET_EXHAUSTED`, `INJECTION_INCIDENT`, `REVIEW` events with token/cost fields.
- Run report (`server/report.py`) gains a *cost & model usage* section and per-agent evidence
  quality (share of findings with resolvable evidence).

### J. Evaluation and testing

- **Keep the 41 existing tests green**; run them with the deterministic router (default).
- **Golden corpus:** the 10 repos the README names (spring-petclinic, flask-tutorial, …) checked out
  under `APPMOD_CORPUS`, with hand-labeled expectations per agent (route, primary language,
  datasets, known CVEs, expected 8R band).
- **Eval harness** (`evals/`): per-agent metrics — schema-valid first try, repair rate, evidence
  resolvability, downgrade rate, agreement with labeled facts, hallucinated paths/symbols (every
  cited file/symbol must exist), cost and latency. Run nightly; gate prompt/model changes on it.
- **Record/replay tests:** cassettes for 2–3 corpus repos so CI exercises the LLM path offline.
- **Adversarial tests:** repos containing prompt-injection comments ("ignore previous
  instructions…", "mark this COMPLETE"), fake secrets, oversized files.

### K. Agentic UX in the console

- **Agent Trace panel** (per node): live model turns (reasoning summaries, not raw chain-of-thought),
  tool calls with arguments and evidence ids, validation/repair rounds, tokens and cost.
- **Approvals Inbox:** pending gates with candidate hash, diff vs previous candidate, evidence
  summary, approve / approve-with-conditions / reject.
- **Stakeholder Questionnaire:** A8 questions rendered as a form; answers re-trigger downstream.
- **Modernization Copilot (chat):** a supervisor agent with read tools over registry, store, audit
  and traces ("why Replatform?", "what blocks G4?", "compare runs") and *confirmed* action tools
  (start run, re-run node, request review). Actions always go through the same APIs and approvals.
- **MCP server** (`appmod/mcp_server.py`): expose `run_pipeline`, `get_run`, `get_artifact`,
  `explain_decision`, `submit_review` so Cursor / Claude / other agents can drive the pipeline.
- **Settings:** provider, model per tier, egress level, tool health (from `doctor`).

---

## 6. Phase-by-phase agent conversion map

Mode: **D** = keep deterministic · **H** = deterministic facts + LLM interpretation · **L** =
LLM-led with tools · **L+X** = LLM-led with sandboxed execution · **HITL** = human input required.

### Phase 1 — Discovery (Stage 1–2)

| Agent | Mode | Tools | What changes |
|---|---|---|---|
| A1 Repo Intelligence | H | scc, Syft, repo_summary, dependencies, read_file | Real SBOM, tech-debt and doc-gap findings; fixes D1 |
| A2 Architecture | H | tree-sitter graph, read_file, search_code | Multi-language component/C4 view, inferred ADRs |
| A3 Data Intelligence | H | sqlglot, ORM model reader, grep | Entity model, data stores, integrations with evidence |
| A4 Infra & Runtime | H | Checkov/IaC parse, telemetry MCP (optional) | Runtime baseline when telemetry connector exists |
| A5 Journey | H | routes, templates, read_file | Journeys grouped and named from code, not just URL list |
| A6 Compliance | H | Trivy/OSV, Gitleaks, Semgrep, ScanCode | Real CVEs and SAST; LLM triages and maps to controls |
| A7 UX Evaluator | H | template reader, Playwright+axe (if runnable) | Heuristic review with evidence; real a11y when runnable |
| A8 Stakeholder | L + HITL | upstream gaps, questionnaire/Slack MCP | Generated questions; real answers → HUMAN_CONFIRMED |
| A9 Business Process | L | read_file, search_code, routes | Processes and business rules traced to code locations |
| A10 Synthesis | L | sealed G1 manifest only (no repo access) | Real cross-domain synthesis; contradictions preserved |
| A11 Risk Scoring | L | policy rubric, upstream artifacts | Scores justified per dimension with evidence ids; no hard-coded `3` |

**Start here:** A10 and A11 (no repo tools, highest visible value, lowest risk), then A9, A2, A6.

### Phase 2 — Portfolio (Stage 4)

| Agent | Mode | Notes |
|---|---|---|
| A1 Value & Market | L | Internal benchmarking; external market data only if policy allows web tools |
| A2 Complexity | H | Deterministic metrics (scc complexity, deps, coupling) + LLM explanation |
| A3 Cost | H | Parametric rate card stays deterministic; LLM writes assumptions/sensitivities |
| A4 Rationalization | L | Overlap via capability-map embedding similarity; proposals only |
| A5 Readiness | H | Rules from P1 scope + LLM blocker narrative |
| A6 Strategy (8R) | L | Disposition chosen from enum with rationale, rejected alternatives, evidence ids |
| A7 Consolidator | H | Deterministic manifest assembly; LLM flags disagreements |

Also: multi-app portfolio input (run P1 on N repos, then one P2), replacing the 1-app shim.

### Phase 3 — Target Architecture (Stage 4)

| Agent | Mode | Notes |
|---|---|---|
| A1 Target Architecture | L | Stack choice with endoflife.date facts; NFR targets still from policy (never invented) |
| A2 Decomposition | L | Boundaries from dependency graph clustering + code reading |
| A3 Data Architecture | L | From P1 A3 entity model; migration design per object |
| A4 Security Architecture | L | STRIDE over real trust boundaries, routes, Semgrep findings |
| A5 UI Architecture | L | Only when route = UI |
| A6 Interface Contracts | H | OpenAPI extraction/generation; Spectral lint |
| A7 Cloud & Capacity | L | Platform blueprint; capacity only with telemetry |
| A8 Consolidator | H | Implement the real consistency checks (D3) + LLM contradiction detection |

### Phase 4 — Planning (Stage 4)

A1–A8 become **L** (tasks, runbooks, resources, tools, validation, rollback generated from the
actual P3 package instead of a fixed 4-task DAG). **A9 stays D** for its checks (DAG acyclicity,
bidirectional task↔requirement coverage, identical context hash across planners, every tool/role
binding resolves) plus an LLM review. Optional export of tasks to GitLab issues / Jira via MCP.

### Phase 5 — Code Modernization, depth 2 (Stage 5)

| Agent | Mode | Notes |
|---|---|---|
| A1 Characterization | L+X | Generate characterization tests; **execute** them on the unmodified build in Docker; record observed results |
| A2 Code Transformation | L+X | Coding agent with `edit_file`/`apply_patch`/`run_build`/`run_tests` on a lane branch of a git worktree; OpenRewrite/codemods first, LLM edits second |
| A3 SQL & Data Layer | L+X | sqlglot transpile + data-access changes + tests |
| A4 UI | L+X | Template/component migration; Playwright journey checks |
| A5 Config & Secrets | L+X | Externalize config; secret refs only |
| A6 Feature Flags | L+X | OpenFeature-style flags around new paths |
| A7 Observability | L+X | OpenTelemetry instrumentation |
| A8 Security Hardening | L+X | Fix Semgrep/Trivy findings; re-scan |
| A9 Validation & Equivalence | D+X (+L explain) | Run baseline vs modernized test suites and contract replays; `runtime-differential` becomes PASS/FAIL, not `NOT_RUN` |

Gates: **G2/G3 become real git merges** of lane branches (conflicts ⇒ revision request to the
owning lane), `build_digest` = real image/artifact digest, G4 can release `READY_FOR_DOWNSTREAM`
when evidence supports it. Output: an MR/PR via GitLab/GitHub MCP for human review.

Sandbox requirements: Docker/Podman, per-run container, no network by default (allow a package
mirror if policy permits), CPU/memory/time limits, worktree mounted read-write, repo origin never
pushed to without an explicit permit.

### Phase 6 — Data Modernization (Stage 6)

Keep **A8, X1, A9 deterministic** (they are the trust anchors). Make A2 (mapping), A3 (sensitive
data, with Presidio on samples/metadata only), A4 (DQ rule generation), A5 (disposition) and A6
(ETL job synthesis, e.g. SQL/dbt) **L** with validation. Generalize X1 beyond SQLite via SQLAlchemy
connectors (Postgres, MySQL, SQL Server) with read-only source credentials from a secret store.
A11 flow tests execute against the P5 build running in the sandbox. Fix D11 (column fidelity).

### Phases 8–9 (future, out of the P1–P6 scope)

Registry already contains 22 roles. Once P5/P6 produce real builds: P8 packaging (Dockerfile/Helm
generation), IaC (Terraform), CI/CD generation, cutover runbooks — all L+X with strict HITL gates
and no production credentials in the pilot.

---

## 7. Policy bundle v2 (example)

Extend `appmod/kernel/policy.py` validation and ship `policies/pilot-agentic-1.0.0.json`:

```json
{
  "policy_version": "pilot-agentic-1.0.0",
  "kind": "engagement-policy",
  "label": "PILOT — agentic runners enabled",
  "llm": {
    "provider": "astra-azure-openai",
    "endpoint": "env:APPMOD_ASTRA_ENDPOINT",
    "api_version": "env:APPMOD_ASTRA_API_VERSION",
    "tiers": { "reasoning": "gpt-6-astra", "coding": "gpt-5.3-codex-PlayWright",
               "fast": "gpt-4.1-mini", "fallback": "gpt-5.4",
               "embedding": "text-embedding-ada-002" },
    "data_egress": "redacted",
    "cache": "record"
  },
  "budgets": {
    "max_retries_per_agent": 2, "max_revision_cycles": 3, "max_parallel_agents": 4,
    "run_cost_usd": 25.0, "agent_default": { "max_turns": 12, "max_output_tokens": 8000,
                                             "context_tokens": 60000, "cost_usd": 2.0 }
  },
  "agents": {
    "P1.A6":  { "mode": "hybrid", "tier": "fast",
                "tools": ["repo_summary", "dependencies", "trivy", "gitleaks", "semgrep", "read_file"] },
    "P1.A10": { "mode": "llm", "tier": "reasoning", "tools": ["get_artifact"] },
    "P1.A11": { "mode": "llm", "tier": "reasoning", "tools": ["get_artifact"] },
    "P5.A2":  { "mode": "llm", "tier": "coding", "max_turns": 40, "cost_usd": 8.0,
                "tools": ["read_file", "grep", "search_code", "edit_file", "apply_patch",
                          "run_build", "run_tests"], "sandbox": "docker" },
    "*":      { "mode": "deterministic" }
  },
  "access": { "repo_roots": ["~/work/repos"], "git_hosts": ["github.com", "gitlab.com"] },
  "reviewers": { "portfolio": ["role:reviewer:portfolio"], "architecture": ["role:reviewer:architecture"],
                 "release": ["role:reviewer:release"] },
  "risk_taxonomy": { "dimensions": ["technical", "security", "data", "operational", "organizational"],
                     "scale": { "min": 1, "max": 5 }, "thresholds": { "high_risk": 4, "blocker": 5 } }
}
```

`"*": deterministic` keeps today's behavior as the default — agents are switched on one by one.

---

## 8. Staged roadmap with deliverables and verification

Estimates assume 2–3 engineers; they are planning estimates, not commitments.

### Stage 0 — Foundations & fixes (≈1 week)

**Deliverables:** `pyproject.toml` (Python ≥3.12, `uv` lock), `.gitlab-ci.yml` (lint, type check,
pytest, UI build), `appmod/config.py` + `.env.example`, fixes D1–D3, D9, D12–D13, contract overlays
skeleton (D10), `scripts/doctor.py`.
**Verify:** 41 existing tests green on 3.12; new tests: primary language of this repo is `python`;
P4 A9 fails when a planner candidate is missing; P2 receives real `languages`/`tests`.

### Stage 1 — LLM connectivity + agent runtime (≈2–3 weeks)

**Deliverables:** `appmod/llm/*`, `appmod/agents/{llm_runner,router,context,repair}.py`,
`prompts/` with versions, `submit_outcome` tool, response cache with replay, audit/metadata fields
(D7), `EvidenceValidator` (workstream D), P1 overlays. Enable **P1 A10 + A11** in LLM mode.
**Verify:** with a key configured, a P1 run publishes A10/A11 envelopes whose
`execution_metadata.runner == "LLMAgentRunner"`, `model_id`/`prompt_version`/`cost_usd` present,
all schema-valid; a deliberately invalid model output is repaired or becomes `FAILED`; replay mode
reproduces the run byte-identically without network; no-key mode falls back to deterministic and
says so in the envelope.

### Stage 2 — Tool gateway + external analyzers (≈2–3 weeks)

**Deliverables:** `ToolGateway` (deny-by-default, redaction, evidence capture), built-in repo tools,
CLI adapters (scc, Syft, Trivy/OSV, Gitleaks, Semgrep, tree-sitter, sqlglot, Checkov), retrieval
index + `search_code`, MCP client. Turn all of P1 to hybrid/LLM mode.
**Verify:** on spring-petclinic and flask-tutorial: A6 lists real CVEs (`vulnerability-scan`
assessed), A1 has a CycloneDX SBOM, every `OBSERVED` finding resolves to a tool evidence id, an
injected "ignore your instructions" comment produces an incident record and no behavior change,
tool-less environments degrade to `NOT_ASSESSED` gaps.

### Stage 3 — Human-in-the-loop + durable orchestration (≈2–3 weeks)

**Deliverables:** run store, worker pool, parallel dispatch (D5, D6, D14), pause/resume/cancel/re-run,
`AWAITING_REVIEW` gates, approvals API + inbox UI, A8 questionnaire, invalidation wired (D8), SSE
events, auth + repo/git allowlists (D4).
**Verify:** a run pauses at P1 G2 awaiting review, survives a server restart, resumes on approval;
an approval against an old candidate hash is rejected; answering an A8 question re-runs A10/A11/G2
and the old versions remain in the store; P4 planners run concurrently (wall-clock drop measured);
unauthenticated `POST /api/runs` returns 401.

### Stage 4 — LLM-led reasoning for P2–P4 (≈2–3 weeks)

**Deliverables:** handoff adapters per phase, multi-app portfolio, LLM modes for the agents marked
L/H in §6, real consistency checks (P3 A8, P4 A9), task export via MCP (optional).
**Verify:** on the 10-repo corpus: dispositions vary with evidence and cite it; P3 threat models
differ per repo and reference real routes/findings; P4 task DAG derives from the P3 package and A9
fails on a seeded inconsistency; eval harness thresholds met (e.g. ≥95 % schema-valid after repair,
≥90 % evidence resolvability, 0 hallucinated file paths).

### Stage 5 — P5 depth 2: real code modernization (≈3–4 weeks)

**Deliverables:** Docker sandbox runner, git worktree + lane branches, coding-agent tools
(`edit_file`, `apply_patch`, `run_build`, `run_tests`), OpenRewrite integration for Java,
characterization tests executed, real G2/G3 merges, real A9 differential, MR/PR creation via MCP.
**Verify:** spring-petclinic dependency upgrade lane produces a buildable branch, characterization
tests pass on baseline and modernized builds, A9 `runtime-differential` is PASS or FAIL (never
NOT_RUN when the build runs), G4 can release `READY_FOR_DOWNSTREAM`; the original repo is untouched.

### Stage 6 — Agentic UX + P6 connectors (≈2–3 weeks)

**Deliverables:** Agent Trace panel, Copilot chat with confirmed actions, Settings page, MCP server,
OpenTelemetry + Langfuse, cost section in report, SQLAlchemy-based X1, sqlglot fixture parser (D11),
LLM modes for P6 A2–A6.
**Verify:** a user can ask the copilot "why was this app Replatformed?" and get an answer citing
artifact ids; Cursor can start a run via the MCP server; a Postgres→Postgres migration reconciles;
traces show per-node cost.

---

## 9. External setup checklist

| Item | Needed for | Action |
|---|---|---|
| LLM provider account + API key | Stage 1 | **Done:** Astra key in gitignored `.env` and verified live (rotate it — it was pasted in chat) |
| Model IDs per tier | Stage 1 | **Done:** `gpt-6-astra` / `gpt-5.3-codex-PlayWright` / `gpt-4.1-mini` / `gpt-5.4` / `text-embedding-ada-002` |
| Python 3.12 + `uv` | Stage 0 | Machine currently has 3.9.6 — install 3.12 (`brew install python@3.12` / `uv python install 3.12`) |
| Node 18+ | UI | Already required |
| Analyzer CLIs | Stage 2 | `brew install scc syft trivy gitleaks`; `pip install semgrep sqlglot checkov tree-sitter-language-pack` |
| Docker Desktop or Colima/Podman | Stage 5 (optional earlier) | Required for builds/tests and P6 A11 |
| Validation corpus | Stage 2+ | Clone the 10 README repos into `APPMOD_CORPUS` |
| Identity provider | Stage 3 | OIDC client (Keycloak/Entra/Okta) or local auth for single-user |
| Database | Stage 3 | SQLite (single-user) → Postgres (team) |
| Langfuse / Phoenix | Stage 1 (dev), Stage 6 (team) | Self-host via Docker or cloud project |
| MCP servers (optional) | Stages 2–6 | GitLab/GitHub, Jira/Linear, Slack/Teams, Datadog |
| GitLab project | All | Issues per stage, labels `agentic`, `stage-N`, milestone per stage, CI |

---

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Hallucinated facts presented as evidence | Evidence validator downgrades uncited claims; hybrid seeds; eval checks for non-existent paths/symbols |
| Model claims human confirmation or self-approves | `HUMAN_CONFIRMED` only from approvals service; gates stay deterministic; candidate-hash binding |
| Proprietary code leaving the network | `data_egress` policy, local-model option, redaction, per-run record of egress level |
| Prompt injection via repo content | Evidence wrapping, allowlists, read-only tools, sandbox without network, incident log |
| Cost/latency blow-up on large repos | Budgets per agent/run, hybrid seeds, retrieval instead of full files, cache, parallel dispatch |
| Non-determinism breaks reproducibility | Response cache, replay mode, versioned prompts in every envelope (Astra does not accept `temperature`) |
| Coding agent damages source | Worktree on a copy, lane branches, sandbox, no push without permit, human MR review |
| Scope creep into P8/P9 | Explicitly out of scope until P5 depth 2 produces real builds |

---

## 11. Decisions needed from you

1. ~~**LLM provider(s)**~~ — **decided: Astra** (Azure OpenAI, `gpt-6-astra` + sibling
   deployments); see [`ASTRA_STEP_BY_STEP_PLAN.md`](ASTRA_STEP_BY_STEP_PLAN.md).
2. **May repository code be sent to a cloud model?** (`none` / `redacted` / `full`)
3. **Docker allowed?** The README's AH01 stance is "no Docker"; real P5/P6 execution needs a sandbox.
4. **Single-user local tool or multi-user team service?** Decides SQLite vs Postgres and auth scope.
5. **Primary target stacks for the pilot** (e.g. Java/Spring first → OpenRewrite investment).
6. **Where should P5 output land?** GitLab MRs, GitHub PRs, or patch bundles only.

---

## Appendix A — Proposed new/changed files

```
appmod/config.py                         settings (env + policy refs)
appmod/llm/{client,budget,cache,errors}.py, providers/{anthropic,openai_compat}.py
appmod/agents/{llm_runner,router,context,repair}.py, prompts/*.md (versioned)
appmod/agents/runtime.py                 ToolSandbox → removed (replaced by ToolGateway)
appmod/tools/gateway.py                  allowlist, redaction, evidence capture
appmod/tools/builtin.py                  read_file, grep, list_dir, git_*, get_artifact, query_store
appmod/tools/analyzers/{scc,syft,trivy,osv,gitleaks,semgrep,treesitter,sqlglot,checkov}.py
appmod/tools/sandbox.py                  Docker exec, worktree management (Stage 5)
appmod/tools/mcp_client.py
appmod/retrieval/{chunker,index}.py
appmod/kernel/evidence.py                EvidenceValidator
appmod/kernel/orchestrator.py            parallel dispatch, AWAITING_REVIEW, pause/resume hooks
appmod/kernel/gates.py                   review-state outcome, real reviewer binding
appmod/kernel/policy.py                  v2 schema (llm, agents, access, reviewers)
appmod/kernel/audit.py                   MODEL_CALL / TOOL_CALL / … events
appmod/contracts/overlays/phase_*.json   item schemas, enums, field descriptions
appmod/phases/pN/handoff.py              upstream-artifact → next-phase brief adapters
appmod/server/{run_store,approvals,elicitation,events,copilot,auth}.py
appmod/mcp_server.py
policies/pilot-agentic-1.0.0.json
evals/                                   corpus labels, harness, reports
scripts/doctor.py
ui/src/views/{AgentTrace,Approvals,Questionnaire,Copilot,Settings}.tsx
pyproject.toml, uv.lock, .env.example, .gitlab-ci.yml
```

## Appendix B — Analysis evidence

- Code read in full: kernel, contracts, store, agents, tools, server and all six phase engines
  (`appmod/`, ≈9.1k lines of Python incl. the XLSX registry compiler, whose structure was reviewed
  but which only matters for recompiling workbooks), `ui/src/views/RunnerView.tsx`,
  `AgentAnatomy.tsx`, tests, `scripts/e2e_pipeline.py`, registry structure for all 8 phases.
- Test suite: `41 passed in 7.92s` (Python 3.9.6, `pytest`).
- Live run: `PipelineJob` on this repository → `COMPLETED` in 3.8 s; gate chain
  `READY_FOR_PORTFOLIO_DECISION → AUTHORIZED → READY_FOR_PLANNING → READY_FOR_PREPARATION →
  LIMITED_HANDOFF → N/A_ROUTE (no data)`; disposition `Replatform` with rationale
  `"pilot heuristic: json API_ONLY app, complexity L1"` (defect D1); all envelopes
  `execution_metadata.runner` = deterministic `P*AgentRunner`.
- Registry: 78 roles, all with payload contracts; field types 327 array / 191 string / 8 object /
  4 enum.
