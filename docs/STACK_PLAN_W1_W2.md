# Stacked implementation plan — Waves 1 and 2

Scope: Wave 1 (measure) and Wave 2 (close the loops in P1–P4) of
`docs/NEXT_LEVEL_AGENTIC_ROADMAP.md`. Nothing in this stack needs a sandbox.

## Decisions recorded (2026-10-12)

| # | Decision | Answer | Consequence for this plan |
|---|---|---|---|
| 1 | Sandbox for P5–P8 | Decide later | Waves 3–5 (code, data, deploy) are out of scope; C7 execution proof stays 0 |
| 2 | Expert labels | Skipped | C4 decision correctness stays *not assessed*; no agent decision can be marked "verified correct" — see assurance rule below |
| 3 | Confidence definition | Assurance coverage; unverifiable items go to a human | New gate rule: an item crosses a release gate only if execution-verified, verifier-entailed, or human-confirmed; anything else becomes a review question and the gate waits |
| 4 | Corpus | ~30 open-source repos with a held-out split; ~40 tool-derived facts per repo, spot-checked by you | Corpus and golden-facts PRs come first; one spot-check task for you |
| 5 | Budget | No token cap; full eval on prompt/model change + weekly | Self-consistency and verifier run at full strength; no cost-optimization PR in this stack |
| 6 | Landing | Stacked PRs; agent merges each to `main` when green; live corpus run on every PR; plan approved with an added PR moving all P1–P4 roles to L2 | Merge rule below; each PR carries its live e2e + eval report |

**What decision 2 means in practice.** Because no expert labels exist, P2 routes, P3
boundaries and P4 plans can never be "verified" by the eval. Under the assurance rule they
therefore reach a release gate only through (a) the claim-support verifier entailing their
evidence and (b) self-consistency agreement — and otherwise through human review. Confidence in
*correctness* of those decisions remains unmeasured and every report will say so.

## Merge rule (applies to every PR)

A PR is merged to `main` by the agent only when all of these hold, and its description links
the evidence:

1. CI green (ruff, mypy, offline tests, UI build).
2. Its own done-when test passes.
3. A **live Astra run on the full corpus** at that PR's head: P1–P4 dispatch success > 97 %,
   Step 33 gate PASS, and no confidence component lower than on the previous merged PR.
4. Key scan of the diff and reports: 0 hits.

Stack mechanics: each PR is based on the one below it; after the bottom PR merges, the next is
retargeted to `main` and re-verified. A failed rule stops the stack at that PR; nothing above it
merges. Live runs on ~30 repos are estimated at 3–5 hours each (run4: 69 min for 10 repos).

## The stack

### PR 0 — `docs`: roadmap + this plan
Roadmap, decisions, stack plan. *Done when:* merged. (Docs-only: live run not required —
it cannot change agent behaviour.)

### Wave 1 — Measure

**PR 1 — `feat(eval)`: confidence components and Wilson bounds.**
`scripts/eval_run.py` → `appmod/evals/` package: the nine components C1–C9 with 95 % Wilson
lower bounds, assurance coverage, and `not assessed` for unmeasured components.
*Done when:* eval report shows all nine components; unit tests pin the bound maths
(e.g. 270/270 → 98.6 %).

**PR 2 — `feat(corpus)`: 30-repo corpus with pinned commits and held-out split.**
`evals/corpus.json` (URL, commit SHA, license, language family, split), `scripts/corpus_sync.py`
to clone/verify. Candidates added to the current 10, finalized after license and clone checks:
eShopModernizing (.NET Framework WebForms/MVC), eShopOnWeb (.NET), agoncal petstore-ee7
(Java EE), struts-examples (Struts), Apache OFBiz (≈1 M+ LOC Java ERP), AWS CardDemo (COBOL/CICS),
OpenCart (PHP monolith), a Rails app (Forem or similar), angular-phonecat (AngularJS 1.x),
Saleor (Django), jhipster-sample-app, and others to reach ~30. Split: ~20 tune / ~10 held-out,
every language family in both.
*Done when:* `corpus_sync.py --verify` passes for all pinned SHAs; held-out list is fixed.

**PR 3 — `feat(eval)`: ~40 golden facts per repo, tool-derived, with spot-check workflow.**
Generator from scc/syft/semgrep/repo scan + manifest parsing (entities, routes, auth, build
tool, test framework, runtime versions, integrations, CVEs, entry points);
`scripts/golden_review.py` presents a random 10 % sample to you to accept/correct; corrections
are recorded as `human_checked`.
*Done when:* ≥ 1,000 facts labelled; your spot-check done; C2 reported per fact type.
**Needs you:** ~1–2 hours of spot-checking.

**PR 4 — `feat(eval)`: stability harness.**
`scripts/stability_run.py`: N = 5 cache-off runs at one commit; route agreement, boundary
Jaccard, risk-score variance per agent → C5.
*Done when:* C5 in the report; agents below 80 % route agreement listed.

**PR 5 — `feat(agents)`: confidence on every decision, calibrated where labels exist.**
`confidence` field on routes, boundaries, risk scores, estimates and facts; calibration map
fitted against golden facts (C6 for facts) and stability agreement (decisions); confidence never
authorizes a gate.
*Done when:* C6 = 1 − ECE reported for facts; decision confidence reported as uncalibrated.

**PR 6 — `feat(agents)`: claim-support verifier.**
`appmod/agents/verifier.py`: an independent model (fallback tier, different family) checks each
OBSERVED/DOCUMENTED claim against the text behind its evidence id; not-entailed claims are
downgraded to INFERRED before publication; 5 % sample exported for human audit.
*Done when:* C3 reported; an injected unsupported claim is downgraded in a test.

**PR 7 — `feat(kernel)`: assurance-coverage gate and badges.**
Every published item gets an assurance class (execution-verified / entailed / human-confirmed /
unverified). Release gates refuse unverified items: they become review questions and the gate
waits (decision 3). Console and outcome report show badges.
*Done when:* a test shows an unverified P2 route raising a review and G2 waiting until it is
confirmed; assurance coverage of released items = 100 % on the live run.

**PR 8 — `test(adversarial)`: adversarial suite.**
≥ 50 fixture cases: injected instructions in code/README/comments, fake secrets, 50 MB and
binary files, symlink escapes, poisoned dependency names, contradictory docs.
*Done when:* C8 = 100 % pass; zero behaviour changes and zero secret leaks.

**PR 9 — `ci(eval)`: eval workflow on change + weekly.**
`.github/workflows/eval.yml` runs the corpus on Astra when overlays/prompts/model version change
and weekly; fails on any component regression; publishes the report as an artifact.
*Done when:* a deliberately degraded prompt fails the workflow.
**Needs you:** approval to store the Astra key as a GitHub Actions secret (see below).

### Wave 2 — Close the loops in P1–P4

**PR 10 — `feat(tools)`: evidence-producing analyzers for P2/P3.**
Dependency graphs (jdeps, madge, pydeps, go list), change-coupling from git history, DB schema
introspection from migrations/DDL, API surface extraction.
*Done when:* OBSERVED/DOCUMENTED share ≥ 60 % for P2 and P3 (today 26 % / 20 %).

**PR 11 — `feat(retrieval)`: large-repo memory.**
Hierarchical repo map with content-hash-cached module summaries and retrieval budgets.
*Done when:* OFBiz (≈1 M LOC) completes P1–P4 with per-agent input tokens ≤ 2× run4 median.

**PR 12 — `feat(agents)`: `ask_stakeholder` for any agent.**
Blocking questions park the node in `AWAITING_INPUT`; answers re-run only that node; per-app
rate limit.
*Done when:* P2.A1 and P3.A4 raise and consume questions end-to-end in human mode.

**PR 13 — `feat(kernel)`: critique-driven re-runs.**
P1.A10 contradictions, P2.A7 disagreements, P3.A8 consistency issues and P4.A9 revision
requests become typed requests; the orchestrator re-runs the target with the critique (≤ 2 rounds), then escalates via
PR 12.
*Done when:* injected contradiction → target re-runs → resolved, audited; ≥ 95 % of live
requests converge in ≤ 2 rounds.

**PR 14 — `feat(p4)`: live replanning.**
P4 replan triggers become predicates over new evidence (answers, critique re-runs, upstream
revisions) and invalidate the affected planners.
*Done when:* an answer that changes P3 scope re-opens exactly the dependent P4 planners.

**PR 15 — `feat(agents)`: model-authored structure for decision roles.**
P2.A6, P3.A1/A2/A3, P4.A3 author their structural fields; the deterministic engine validates
and is the fallback.
*Done when:* ≥ 95 % first-pass validity for those roles, C1 unchanged.

**PR 16 — `feat(agents)`: every P1–P4 role at L2.**
The 24 roles still at L1 get at least one model-authored decision field that a named downstream
agent or gate consumes, declared in the contract (`consumed_by`) and passed through the
consumer's inputs (e.g. P1.A3 entities → P3.A3 schemas, P1.A6 control findings → P3.A4 threats,
P4.A7 tests → P4.A9 coverage check).
*Done when:* a lineage test proves, for each of the 31 non-critic roles, that a model-authored
field reaches its declared consumer; C1 unchanged.

**PR 17 — `feat(agents)`: self-consistency for routes and boundaries.**
k = 3 independent candidates for P2.A6 and P3.A2; agreement publishes, disagreement becomes a
review question listing the options and evidence.
*Done when:* C5 route agreement ≥ 90 % on the stability harness; every disagreement reaches a
reviewer.

**PR 18 — `test(e2e)`: wave report.**
Full live corpus run + stability run; reports for tune and held-out splits; roadmap §4 updated
with measured values.
*Done when:* report merged; held-out numbers published separately.

## Expected position after the stack

| Measure | Today | After this stack |
|---|---|---|
| Agentic level | 19 % (39 / 203) | 38 % (78 / 203): all 35 P1–P4 roles at target — 4 critics at L4, 31 roles at L2; P5–P9 unchanged |
| Assurance coverage of released items | not enforced | 100 % (enforced by PR 7) |
| C1 integrity, C2 facts, C3 support, C5 stability, C6 calibration (facts), C8 robustness | partly measured | all measured with bounds |
| C4 decision correctness | unmeasured | still not assessed (decision 2) |
| C7 execution proof | 0 | still 0 (decision 1) |
| C9 human acceptance | scripted | still scripted |

## Inputs needed from you during the stack

1. PR 3: spot-check a 10 % sample of generated facts (~1–2 h).
2. PR 9: permission to put the Astra key in GitHub Actions secrets (or a different key).
3. Rotate the current Astra key (shared in chat during setup) before PR 9.
