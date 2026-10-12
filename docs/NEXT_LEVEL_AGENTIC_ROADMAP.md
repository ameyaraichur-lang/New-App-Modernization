# Next-level roadmap: fully agentic, measurably confident

Baseline: `main @ 891a276` (PR #1, milestones M0–M4). Every number below is measured from the
code or from run4 (`job-1791780230-52f08d`, 10 legacy repos, live Astra, 69 min wall clock,
19.6 M input / 1.0 M output tokens) unless marked *target*.

This document answers two questions: what it would take to make the pipeline **fully
agentic**, and what it would take to reach a **100 % confidence score** — and it first defines
both terms precisely, because neither is meaningful as a slogan.

---

## 1. Two scores, defined

### 1.1 Agentic Level (AL)

Each of the 78 blueprint roles sits on an autonomy ladder:

| Level | Name | The model… | Example today |
|---|---|---|---|
| L0 | Deterministic | does nothing; code computes the output | all of P5, P6 |
| L1 | Enrich | investigates with tools and adds evidence-cited findings to a seed | most of P1–P4 |
| L2 | Decide | authors a field that downstream agents or gates consume | P2.A6 route, P3.A2 boundaries, P1.A11 risk scores, P1.A8 questions |
| L3 | Act | changes the world in a sandbox (edits code, runs builds/tests, moves data, deploys) and verifies the result | none |
| L4 | Self-correct | its critique or failure re-opens upstream work (bounded loop) and the loop converges | none |
| L5 | Learn | accepted/rejected outcomes across runs change future behaviour through eval-gated updates | none |

Every role gets a **target level** (§3 lists them). Some roles are deterministic *by design* —
P6.A8 schema parity and P6.A9 reconciliation must stay exact arithmetic, and release gates stay
policy + human (`gates.py`: "model confidence cannot authorize release"). Reaching a target of
L0 counts as at target.

> **AL = Σ min(current, target) / Σ target** over the 78 roles.
> **Today: 39 / 203 = 19 %; 6 of 78 roles at target.**
> **100 % agentic** = every role at its target level, which is *not* "no humans" and *not*
> "the model replaces deterministic checks".

Per phase today (points / target points): P1 13/24 · P2 8/16 · P3 9/18 · P4 9/20 ·
P5 0/28 · P6 0/29 · P8 0/37 · P9 0/31. (P7 is skipped by blueprint finding IA05.)

### 1.2 Confidence Score (CS)

Confidence is not one number the model reports about itself. It is a set of measured
components, each reported as its **95 % Wilson lower bound** (so a small sample cannot claim
100 %), and the overall score is the **weakest component**. Following the pipeline's own rule —
`NOT_RUN` never counts as `PASS` — an **unmeasured component scores 0**.

| # | Component | What it proves | Today (95 % LB) |
|---|---|---|---|
| C1 | Integrity | outputs are schema-valid, every citation resolves, no invented paths/symbols | 98.6 % (270/270 schema), 99.6 % paths (0/860 bad), 98.9 % symbols (0/351 bad), 99.97 % evidence (14,988/14,988 resolve) |
| C2 | Factual accuracy | discovered facts match ground truth | 86.8 % (38/39 — 4 facts × 10 repos, todomvc has no framework label) |
| C3 | Claim support | cited evidence actually *supports* the claim, not merely exists | **unmeasured → 0** |
| C4 | Decision correctness | routes, boundaries, plans match an expert panel | **unmeasured → 0** |
| C5 | Stability | same inputs → same decisions across repeated runs | **unmeasured → 0** (run3 vs run4 agree on 5/10 routes, but run3 used a since-fixed biased prompt, so this is not a valid stability sample) |
| C6 | Calibration | stated confidence matches observed accuracy | **unmeasured → 0** (no confidence field exists) |
| C7 | Execution proof | changes build, tests pass, data reconciles | **0** — P5 runtime differential is `NOT_RUN`; P6 runs only on sqlite fixtures |
| C8 | Robustness | adversarial inputs do not change behaviour | partial — one prompt-injection test; no adversarial suite |
| C9 | Human acceptance | real reviewers approve with little editing | **unmeasured → 0** — reviewer and stakeholders are scripted |

> **CS today = 0 %** (weakest link), even though integrity is near-perfect.
> That is the honest reading of "the system is well-grounded, but nobody has shown its
> decisions are right".

### 1.3 What "100 %" can and cannot mean

- **Integrity (C1) and execution proof (C7) can be 100 % by construction**: make them gates,
  so anything that fails does not ship. 100 % of *shipped* changes building and passing tests
  is achievable.
- **Judgment (C4) cannot be proven 100 % correct.** With zero errors, the 95 % lower bound is
  n / (n + 3.84): 96.3 % at n = 100, 99.0 % at n = 381, 99.6 % at n = 1,000. And expert
  architects themselves disagree, so the real ceiling is *inter-expert agreement*; matching it
  is the meaningful target.
- **The achievable 100 %** is **assurance coverage**: *100 % of released claims and decisions
  are either execution-verified, verifier-entailed by an independent model, or confirmed by a
  named human — and zero unverified items cross a release gate.* The kernel can enforce this.
  This document recommends adopting that as the definition of "100 % confidence", alongside
  the statistical targets in §4.

Today's evidence strength, as a starting point for assurance coverage — share of model-authored
items classed OBSERVED/DOCUMENTED (the rest are INFERRED/UNKNOWN/HYPOTHETICAL):
P1 73 % · P2 26 % · P3 20 % · P4 72 %. P2 and P3 — the decisions that matter most — are the
least directly evidenced.

---

## 2. Gap analysis (evidence)

| Area | Current state | Evidence |
|---|---|---|
| Model loop coverage | 35 / 78 roles (P1–P4) | `appmod/agents/overlays.py` (19 reasoning, 15 fast, 1 coding tier) |
| Decision authority | Model fills overlay fields over a deterministic seed; postprocess re-derives structure; status may only get stricter | `llm_runner.py` docstring; `_pp_p2_a6` |
| Acting on the world | No write/execute tools; subprocess use limited to analyzers and `git log` | `appmod/tools/builtin.py`, `analyzers.py` |
| Feedback loops | P1.A10 `contradictions`, P3.A8 `consistency_issues`, P4.A9 `revision_requests` are written into artifacts, but **no kernel or server code acts on them** | `rg "consistency_issues\|revision_requests\|contradictions" appmod` → only schemas and the producing engines/overlays |
| Replanning | P4 `replan_triggers` are seed constants | `p4/engine.py:74` |
| Asking humans | Only P1.A8 can raise stakeholder questions | `jobs.py` `_register_questions` |
| P5 code modernization | Change manifests only; `patch_ref = manifest:<lane>`; runtime differential `NOT_RUN` → G4 `LIMITED_HANDOFF` | `p5/engine.py:73,240,389` |
| P6 data | Real row copy, but sqlite fixtures only | `p6/engine.py` |
| P8 deploy / P9 operate | Not implemented (22 roles) | `data/registry/phase_8.json`, `phase_9.json` |
| Sandbox | No container runtime on the host (docker/colima/podman absent); blueprint AH01 says local, no Docker | `README` limit 7 |
| Gate policy | `pilot-default-1.1.0` thresholds, not an approved org bundle | `kernel/policy.py` |
| Evaluation | 4 golden facts per repo, 10 repos, 2 live runs; no expert labels, no repeat runs, no claim-support check, no adversarial suite, no nightly job | `evals/golden/corpus.json`, `scripts/eval_run.py` |
| Corpus | 10 small/medium open-source apps; no enterprise-scale or mainframe code | `docs/runs/e2e-run4.md` |
| Cost / latency | 19.6 M input tokens per 10 repos; input dominates output 19:1 | `e2e-run4.json` |
| Observability | Events + traces in SQLite; no OpenTelemetry/Langfuse | Step 32 not started |
| Interfaces | Console + REST; no copilot, no MCP server | Step 31 not started |

---

## 3. Upgrades

Each upgrade lists what changes, where, and a done-when that a test or report can prove. Steps
26–33 of `ASTRA_STEP_BY_STEP_PLAN.md` are folded in where they belong.

### Track A — Measure first (confidence instrumentation)

You cannot raise a score you do not measure, so this track comes first.

**A1. Golden facts ×10.** Expand `evals/golden/corpus.json` from 4 to ~40 facts per repo,
derived from tools and hand-verified: entities/tables, routes, auth mechanism, test framework,
build tool, runtime versions, external integrations, known CVEs, entry points.
*Files:* `evals/golden/`, `scripts/eval_run.py`. *Done when:* C2 is reported per fact type on
≥ 400 labelled facts with a Wilson LB.

**A2. Expert decision labels.** Two or three architects independently label each corpus repo:
8R route (with acceptable alternates), service boundaries, top-5 risks, wave. Record
inter-rater agreement (Cohen's κ for routes, boundary Jaccard).
*Files:* `evals/expert/<repo>.json`, eval scorer. *Done when:* C4 = model agreement vs panel,
reported next to inter-rater agreement.

**A3. Stability harness.** Run the same commit, corpus and model version N = 5 times
(`--cache off`); report route agreement, boundary Jaccard, risk-score variance per agent.
*Files:* `scripts/stability_run.py`. *Done when:* C5 is in the eval report; any agent with
route agreement < 80 % is flagged.

**A4. Claim-support verifier.** An independent model (`fallback` tier, different family from
the author) checks each OBSERVED/DOCUMENTED claim against the text behind its evidence id:
entailed / not entailed / unclear. Not-entailed claims are downgraded to INFERRED before
publication; a 5 % random sample is human-audited to measure the verifier itself.
*Files:* `appmod/agents/verifier.py`, `llm_runner._check`. *Done when:* C3 reported; human
audit agrees with the verifier ≥ 90 %.

**A5. Calibrated confidence.** Every decision field (route, boundary, risk score, estimate)
carries `confidence ∈ [0,1]`; the eval computes expected calibration error against A1/A2
labels and fits a per-agent calibration map. Calibrated confidence never authorizes a gate; it
routes items to humans.
*Files:* overlays, contracts, eval. *Done when:* C6 = 1 − ECE is reported; ECE ≤ 0.05.

**A6. Adversarial suite (rest of Step 33).** Fixture repos with injected instructions in code
comments/READMEs, fake secrets, 50 MB files, binary blobs, symlink escapes, poisoned
dependency names, contradictory docs.
*Files:* `tests/adversarial/`, `evals/adversarial/`. *Done when:* C8 = pass rate on ≥ 50 cases;
zero behaviour changes, zero secret leaks.

**A7. Confidence report and badges.** `eval_run.py` emits CS with every component and its
bound; the console and outcome report show a per-artifact badge (verified by execution /
entailed / human-confirmed / inferred).
*Files:* `server/report.py`, `ui/`. *Done when:* every artifact in the UI shows its assurance
class.

**A8. Nightly and on-change eval in CI.** Scheduled job runs the corpus on Astra, publishes the
report, and fails if any component regresses; re-runs on every prompt version or model version
change (pinned `2026-09-03`).
*Files:* `.github/workflows/eval.yml`. *Done when:* a deliberately degraded prompt fails CI.

### Track B — Close the loops in P1–P4 (L1/L2 → L4)

**B1. Critique-driven re-runs.** Make the three consistency roles actionable: P1.A10
`contradictions`, P3.A8 `consistency_issues` and P4.A9 `revision_requests` become typed
requests `{target_node, problem, evidence_ids}`; the orchestrator re-runs the target with the
critique as input, at most 2 rounds, then escalates to a human question. Uses the existing
invalidation engine (reuse-by-input-hash keeps cost bounded).
*Files:* `kernel/orchestrator.py`, `kernel/invalidation.py`, `server/jobs.py`, overlays for
the three critics. *Done when:* a test injects a contradiction, the target re-runs, the
contradiction disappears, and the audit log shows the loop; on the corpus, re-runs converge in
≤ 2 rounds for ≥ 95 % of requests.

**B2. Ask-anyone tool.** Any agent may call `ask_stakeholder(question, why, blocking)`;
blocking questions park the node in `AWAITING_INPUT`; answers re-run only that node. Rate-limit
per app.
*Files:* `tools/builtin.py`, `server/jobs.py`, questions store. *Done when:* P2.A1 can ask for
business value and P3.A4 for a compliance regime, end-to-end in human mode.

**B3. Model-authored structure (seed inversion) for decision roles.** For P2.A6, P3.A1/A2/A3,
P4.A3 the model authors the structural fields; the deterministic engine becomes the
*validator* (invariants, cross-field rules) and the fallback, not the author.
*Files:* overlays (`fields` → full payload for these roles), `contracts/`. *Done when:* those
roles are at L2 with ≥ 95 % first-pass validity and no drop in C1.

**B4. Self-consistency for high-stakes decisions.** P2.A6 and P3.A2 sample k = 3 independent
candidates (different tiers or seeds of reasoning); agreement publishes, disagreement becomes a
stakeholder question with the competing options and their evidence.
*Done when:* C5 ≥ 90 % for routes on the stability harness, and every disagreement is visible
to a reviewer.

**B5. Live replanning.** P4 `replan_triggers` become predicates evaluated when new evidence
lands (answers, P5 test failures, P6 reconciliation deltas); a firing trigger invalidates and
re-runs the affected planners.
*Files:* `phases/p4/engine.py`, `kernel/invalidation.py`. *Done when:* a P5 lane failure
re-opens the P4 estimate for that lane automatically.

**B6. Large-repo memory.** Hierarchical repo map (module summaries cached by content hash) and
retrieval budgets so agents work on > 500 k LOC monoliths without blowing context; also the
main lever on the 19:1 input/output token ratio.
*Files:* `appmod/retrieval/`, `tools/builtin.py`. *Done when:* a 1 M LOC repo completes P1
with input tokens per agent ≤ 2× today's median.

**B7. Raise P2/P3 evidence strength.** Give P2/P3 agents tools that produce *observations*
rather than inferences: dependency graph extraction (jdeps, madge, pydeps), call-graph and
change-coupling from `git log`, DB schema introspection, API surface extraction (OpenAPI from
routes).
*Files:* `tools/analyzers.py`. *Done when:* OBSERVED/DOCUMENTED share rises from 26 %/20 % to
≥ 60 % for P2/P3.

### Track C — The hands: real code modernization in P5 (L0 → L3/L4)

This is the largest single jump in AL (+28 points) and the only way to make C7 non-zero.

**C0. Sandbox decision (needs your call).** Blueprint AH01 says local-only, no Docker; the host
has no container runtime. Options: (a) Colima + Docker per-run containers (reproducible,
network-off by default — recommended); (b) git worktrees + per-language toolchains with macOS
`sandbox-exec` (lighter, weaker isolation); (c) remote sandbox (e.g. a CI runner) per lane.
*Files:* `appmod/tools/sandbox.py`. *Done when:* a test proves the sandbox blocks network
egress and writes outside the worktree, enforces CPU/memory/time limits, and leaves the source
repo byte-identical after a run.

**C1. Characterization tests (Step 27, P5.A1).** Generate tests for routes/journeys found in P1;
run them on the *unmodified* build; the observed results become the oracle.
*Done when:* spring-petclinic and flask-tutorial have green baseline suites with ≥ 70 % route
coverage.

**C2. Coding agents (Step 28, P5.A2–A8).** Tools `edit_file`, `apply_patch`, `run_build`,
`run_tests`, `run_semgrep`; deterministic codemods first (OpenRewrite for Java, pyupgrade/ruff
for Python, Rector for PHP, .NET Upgrade Assistant), model edits second; loop until lane checks
pass or budget ends.
*Done when:* each lane produces a branch whose build is green.

**C3. Real integration and validation (Step 29).** Lane branches merge for real; conflicts
become revision requests to the owning lane (B1 mechanism); P5.A9 runs baseline vs modernized
tests and contract replays; G4 can release `READY_FOR_DOWNSTREAM`; a PR/MR opens for human
review.
*Done when:* 3 corpus repos get a buildable modernized branch with all characterization tests
passing and an open PR; source repos untouched.

### Track D — Data modernization in P6 (L0 → L3)

**D1. Real connectors (Step 30).** SQLAlchemy for Postgres/MySQL/SQL Server with read-only
source credentials; `sqlglot` DDL parsing; model-led A2 mapping, A3 sensitivity (metadata +
Presidio samples), A4 DQ rules, A5 disposition, A6 ETL synthesis, A7 CDC plan; A8/A9 stay
deterministic; A11 flow tests run against the P5 build in the sandbox.
*Done when:* a Postgres → Postgres-with-new-schema migration of a corpus app reconciles
counts and checksums exactly, and the app's characterization tests pass against the migrated
data.

### Track E — Deploy and operate: P8 and P9 (not built → L3/L4)

**E1. P8 deployment & cutover (12 roles).** Generate container images, IaC (Terraform/Helm),
secrets wiring, CI/CD pipeline, runbooks; deploy to an ephemeral local cluster (kind/k3d);
smoke + validation pack; rehearsed rollback; P8.A10 orchestrates cutover with go/no-go gate.
*Done when:* a corpus app is deployed, validated, rolled back and redeployed with no human
edits to generated assets, and every step is evidenced.

**E2. P9 operations (10 roles).** Dashboards and alerts from P5 instrumentation, FinOps from
resource specs, drift detection (P9.A5 compares deployed state to P3 architecture and re-opens
it — L4), decommission plan for the legacy app, closure summary.
*Done when:* injected drift in the deployed app is detected and produces a P3 revision request.

### Track F — Learn (L5)

**F1. Outcome memory.** Store reviewer edits, rejections, answers and execution outcomes per
agent (content-addressed, with the candidate hash they apply to); retrieve similar past cases
as exemplars in the agent's context.
*Files:* `appmod/memory/`, `server/rundb.py`, `llm_runner.py`. *Done when:* on a re-run of a
repo whose route a reviewer corrected, the agent cites the correction and the eval shows no
regression elsewhere.

**F2. Eval-gated prompt evolution.** Candidate prompt/overlay changes are generated from
failure clusters and adopted only if the nightly eval (A8) improves without regressions.
*Files:* `scripts/propose_overlay.py`, overlays (versioned). *Done when:* one prompt change is
proposed from data and adopted through the gate.

### Track G — Platform

**G1. Observability (Step 32).** OpenTelemetry spans run → phase → node → model call → tool
call (GenAI conventions); Langfuse; per-node tokens and latency in the report.
*Files:* `appmod/telemetry.py`, `llm/astra.py`, `tools/gateway.py`. *Done when:* one run's
full span tree is browsable in Langfuse and the report lists p50/p95 latency per agent.

**G2. Copilot and MCP server (Step 31).** Chat over registry/store/traces with
confirm-before-act tools; `run_pipeline`, `get_run`, `explain_decision`, `submit_review`
exposed over MCP so Cursor can drive runs.
*Files:* `appmod/mcp_server.py`, `server/api.py`, `ui/`. *Done when:* a run is started,
inspected and reviewed entirely from Cursor through the MCP server.

**G3. Cost and speed.** Prompt caching of instructions + seeds, context trimming via B6,
fast-tier routing where evals show no loss; per-run budget with hard stop.
*Files:* `llm/router.py`, `llm_runner.py`, overlays. *Done when:* input tokens per repo
≤ 50 % of run4's ~2 M at equal or better CS.

**G4. Approved policy bundle.** Replace `pilot-default-1.1.0` with an organization-approved
bundle (thresholds, data classes, allowed routes), versioned in every envelope.
*Files:* `kernel/policy.py`, `config/policy/`. *Done when:* gates cite the approved bundle
version and a bundle change invalidates exactly the dependent gate decisions.

**G5. Production hardening.** Secrets from a vault (no `.env` key) with rotation; durable work
queue for concurrent runs; per-tenant isolation; model canary on version change.
*Files:* `config.py`, `server/jobs.py`, deployment manifests. *Done when:* 20 concurrent runs
complete with a rotated key mid-run, and a model version change runs the canary eval before
traffic moves.

### Track H — Real-world proof

**H1. Corpus of 50+ repos, held-out split.** Add enterprise-shaped legacy — Java EE/Struts,
.NET Framework WebForms/WCF, PHP monoliths, Rails 4, a COBOL/CICS sample (e.g. AWS CardDemo),
one > 1 M LOC monolith. Tune on 30, report on a held-out 20.
*Files:* `evals/golden/`, `evals/expert/`, `scripts/e2e_agentic.py --repos`. *Done when:* §4
targets are reported on the held-out 20 only.

**H2. Human pilot.** Real reviewers and stakeholders on 3–5 internal apps; measure approval
rate, edit distance, questions answered, and hours saved vs a manual assessment.
*Files:* `evals/pilot/`, report section. *Done when:* C9 is computed from real decisions and
published with the reviewers' feedback.

---

## 4. Targets

| Component | Today | Target | Unlocked by |
|---|---|---|---|
| AL (agentic level) | 19 % | 100 % (all roles at target) | B, C, D, E, F |
| C1 integrity | ≥ 98.6 % LB | ≥ 99 % LB, 0 hallucinations | keep; scale n |
| C2 facts | 86.8 % LB (n = 39) | ≥ 95 % LB (n ≥ 400) | A1, B7 |
| C3 claim support | 0 (unmeasured) | ≥ 95 % entailed | A4 |
| C4 decisions | 0 (unmeasured) | ≥ inter-expert agreement | A2, B3, B4 |
| C5 stability | 0 (unmeasured) | ≥ 90 % route agreement over 5 runs | A3, B4 |
| C6 calibration | 0 (unmeasured) | ECE ≤ 0.05 | A5 |
| C7 execution proof | 0 | 100 % of shipped changes build + pass | C, D |
| C8 robustness | partial | 100 % of ≥ 50 adversarial cases | A6 |
| C9 human acceptance | 0 (scripted) | ≥ 80 % approved with minor edits | H2 |
| Assurance coverage | not enforced | 100 % of released items verified/entailed/confirmed | A4, A7, C, gate rule |

---

## 5. Sequenced roadmap

| Wave | Weeks | Work | Exit criterion |
|---|---|---|---|
| 1 Measure | 1–3 | A1, A2 (labelling starts), A3, A5, A7, A8 | CS reported with all 9 components; first non-zero C4/C5/C6 |
| 2 Close loops | 3–6 | B1, B2, B4, B5, A4, B7 | 3 critique loops live and converging; C3 measured; P2/P3 evidence ≥ 60 % |
| 3 Hands | 6–12 | C0 decision, C1–C3, A6 | 3 repos with green modernized branches + PRs; C7 > 0 |
| 4 Data | 12–15 | D1, B3 | real-DB migration reconciles; decision roles model-authored |
| 5 Deploy & operate | 15–21 | E1, E2, G1, G2 | deploy/rollback/drift loop on one app |
| 6 Scale & learn | 21–28 | H1, H2, F1, F2, G3–G5 | held-out CS meets §4 targets; human pilot results published |

Rules for every wave: each upgrade lands as a small PR with its done-when test; the nightly eval
(A8) must not regress; `NOT_RUN` never counts as `PASS`; gates remain policy + human.

---

## 6. Decisions needed from you

*Answered 2026-10-12 — see `docs/STACK_PLAN_W1_W2.md`: sandbox deferred, expert labels
skipped, assurance coverage adopted (unverifiable items go to a human), 30-repo open-source
corpus with tool-derived golden facts, no token cap, eval on change + weekly.*

1. **Sandbox** (C0): Colima/Docker vs worktree + `sandbox-exec` vs remote runner. This
   overrides blueprint AH01 for P5–P8 and should be recorded as a blueprint finding.
2. **Expert panel** (A2): who labels the corpus, and how many raters.
3. **Definition of "100 % confidence"**: adopt assurance coverage (§1.3) as the gate, with the
   statistical targets in §4 as release criteria.
4. **Corpus expansion** (H1): whether any internal (non-open-source) applications can be used.
5. **Budget**: today ~2 M input tokens per repo; waves 3–6 add sandboxed builds and k-sample
   decisions.
