# Step 33 eval — `run-eval-holdout` (`job-1792248896-66d376`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (219/219) | ≥ 95% |
| evidence resolvability | 100.0% (11805/11805) | ≥ 90% |
| hallucinated paths | 0 of 2293 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 382 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.28% | schema valid after repair 219/219 (LB 98.28%); evidence ids resolve 11805/11805 (LB 99.97%); cited paths exist 2293/2293 (LB 99.83%); A9 function names exist 382/382 (LB 99.0%) |
| C2 Factual accuracy | 78.32% | golden facts agree 372/453 (LB 78.32%) |
| C3 Claim support | 54.83% | cited claims entailed by their evidence 1361/2395 (LB 54.83%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.3% | 1 - ECE at bootstrap 95%: 150 fact confidences, ECE 0.0182, 95th percentile 0.027 |
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
| entity | 57.83% | 83 | saleor CheckoutDelivery (got False, want True), saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 50.57% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True), djangoproject /403 (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

4671 items released through 23 G2 gates: coverage 100.0%, of which 35.58% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 301 | 6.44% |
| entailed | 1361 | 29.14% |
| scripted-confirmed | 3009 | 64.42% |

## Claim support (`appmod/agents/verifier.py`)

2395 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1361 | 56.83% |
| INSUFFICIENT | 885 | 36.95% |
| NOT_ENTAILED | 149 | 6.22% |

Human audit sample: 132 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

150 fact confidences checked against golden facts: ECE 0.0182 (bootstrap 95th percentile 0.027). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.7-0.8 | 1 | 0.7 | 1.0 |
| 0.8-0.9 | 1 | 0.85 | 1.0 |
| 0.9-1.0 | 148 | 0.978 | 0.993 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.889 | 0.889 |
| datastore | 20 | 0.978 | 1.0 |
| entity | 45 | 0.989 | 1.0 |
| framework | 13 | 0.981 | 1.0 |
| license | 10 | 0.987 | 1.0 |
| route | 44 | 0.973 | 1.0 |
| runtime_version | 9 | 0.975 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.889 | 0.7 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.924 | 0.77 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.819 | 0.63 | 0.88 | 0 |
| P3 A2 boundaries | 51 | 0.943 | 0.85 | 0.99 | 0 |
| P4 A3 task estimates | 49 | 0.854 | 0.74 | 0.96 | 0 |

## Variation with evidence

- P2 dispositions: {'Retain': 3, 'Refactor': 6, 'Retire': 1}
- P3 decomposition: 6 distinct boundary sets across 6 apps
