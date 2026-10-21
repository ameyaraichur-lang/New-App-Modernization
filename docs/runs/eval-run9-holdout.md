# Step 33 eval — `run9-holdout` (`job-1792061425-19d0f6`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (236/236) | ≥ 95% |
| evidence resolvability | 100.0% (12855/12855) | ≥ 90% |
| hallucinated paths | 1 of 2248 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 370 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 5 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.4% | schema valid after repair 236/236 (LB 98.4%); evidence ids resolve 12855/12855 (LB 99.97%); cited paths exist 2247/2248 (LB 99.75%); A9 function names exist 370/370 (LB 98.97%) |
| C2 Factual accuracy | 79.74% | golden facts agree 378/453 (LB 79.74%) |
| C3 Claim support | 57.74% | cited claims entailed by their evidence 1475/2471 (LB 57.74%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.95% | 1 - ECE at bootstrap 95%: 155 fact confidences, ECE 0.0128, 95th percentile 0.0205 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
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
| entity | 65.06% | 83 | saleor CheckoutDelivery (got False, want True), saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 50.57% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), eshop-modernizing /uploadimage (got False, want True), saleor /static (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Claim support (`appmod/agents/verifier.py`)

2471 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1475 | 59.69% |
| INSUFFICIENT | 861 | 34.84% |
| NOT_ENTAILED | 135 | 5.46% |

Human audit sample: 116 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

155 fact confidences checked against golden facts: ECE 0.0128 (bootstrap 95th percentile 0.0205). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 155 | 0.981 | 0.994 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.928 | 0.889 |
| datastore | 20 | 0.979 | 1.0 |
| entity | 51 | 0.99 | 1.0 |
| framework | 13 | 0.98 | 1.0 |
| license | 10 | 0.989 | 1.0 |
| route | 44 | 0.982 | 1.0 |
| runtime_version | 8 | 0.969 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.928 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.941 | 0.84 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.774 | 0.7 | 0.8 | 0 |
| P3 A2 boundaries | 61 | 0.942 | 0.88 | 0.99 | 0 |
| P4 A3 task estimates | 54 | 0.827 | 0.66 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Replatform': 1, 'Retain': 2, 'Refactor': 6, 'Retire': 1}
- P3 decomposition: 7 distinct boundary sets across 7 apps

## Hallucinated paths

- `{"artifact": "P1/cargotracker/A6", "path": "docker-compose/server.xml"}`
