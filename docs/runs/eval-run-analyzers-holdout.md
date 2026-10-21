# Step 33 eval — `run-analyzers-holdout` (`job-1792321699-449172`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (202/202) | ≥ 95% |
| evidence resolvability | 100.0% (11314/11314) | ≥ 90% |
| hallucinated paths | 4 of 2349 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 409 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.13% | schema valid after repair 202/202 (LB 98.13%); evidence ids resolve 11314/11314 (LB 99.97%); cited paths exist 2345/2349 (LB 99.56%); A9 function names exist 409/409 (LB 99.07%) |
| C2 Factual accuracy | 78.32% | golden facts agree 372/453 (LB 78.32%) |
| C3 Claim support | 57.2% | cited claims entailed by their evidence 1421/2401 (LB 57.2%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.76% | 1 - ECE at bootstrap 95%: 149 fact confidences, ECE 0.0147, 95th percentile 0.0224 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | 94.42% | adversarial cases pass 65/65 (LB 94.42%) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

453 tool-derived facts over 10 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 15 | — |
| capability_route | 80.0% | 10 | spring-framework-petclinic capability_route (got API_ONLY, want UI), cargotracker capability_route (got HEADLESS_BATCH, want UI) |
| ci | 100.0% | 10 | — |
| containerized | 100.0% | 10 | — |
| datastore | 100.0% | 20 | — |
| dependency | 100.0% | 150 | — |
| entity | 55.42% | 83 | saleor CheckoutDelivery (got False, want True), saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 52.87% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

4369 items released through 21 G2 gates: coverage 100.0%, of which 39.05% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 285 | 6.52% |
| entailed | 1421 | 32.52% |
| scripted-confirmed | 2663 | 60.95% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 51.11% | 1177 | 2303 |
| P2 | 13.49% | 17 | 126 |
| P3 | 13.0% | 140 | 1077 |
| P4 | 17.16% | 87 | 507 |

## Claim support (`appmod/agents/verifier.py`)

2401 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1421 | 59.18% |
| INSUFFICIENT | 835 | 34.78% |
| NOT_ENTAILED | 137 | 5.71% |
| UNCHECKED | 8 | 0.33% |

Human audit sample: 112 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

149 fact confidences checked against golden facts: ECE 0.0147 (bootstrap 95th percentile 0.0224). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 149 | 0.979 | 0.993 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.933 | 0.889 |
| datastore | 20 | 0.979 | 1.0 |
| entity | 43 | 0.987 | 1.0 |
| framework | 13 | 0.977 | 1.0 |
| license | 10 | 0.99 | 1.0 |
| route | 46 | 0.979 | 1.0 |
| runtime_version | 8 | 0.969 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.933 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.939 | 0.83 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.8 | 0.67 | 0.86 | 0 |
| P3 A2 boundaries | 45 | 0.944 | 0.88 | 0.98 | 0 |
| P4 A3 task estimates | 41 | 0.8 | 0.66 | 0.9 | 0 |

## Variation with evidence

- P2 dispositions: {'Retire': 2, 'Retain': 3, 'Refactor': 5}
- P3 decomposition: 5 distinct boundary sets across 5 apps

## Hallucinated paths

- `{"artifact": "P1/gitea/A6", "path": "tests/mysql.ini"}`
- `{"artifact": "P1/gitea/A6", "path": "tests/mssql.ini"}`
- `{"artifact": "P1/gitea/A6", "path": "tests/sqlite.ini"}`
- `{"artifact": "P4/human-essentials/A3", "path": "app/config/db/spec/lib/docs/.devcontainer/clock.rb"}`
