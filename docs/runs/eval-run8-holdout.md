# Step 33 eval — `run8-holdout` (`job-1792041165-85e6b2`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (219/219) | ≥ 95% |
| evidence resolvability | 100.0% (12647/12647) | ≥ 90% |
| hallucinated paths | 0 of 2120 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 414 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 6 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.28% | schema valid after repair 219/219 (LB 98.28%); evidence ids resolve 12647/12647 (LB 99.97%); cited paths exist 2120/2120 (LB 99.82%); A9 function names exist 414/414 (LB 99.08%) |
| C2 Factual accuracy | 79.27% | golden facts agree 376/453 (LB 79.27%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.54% | 1 - ECE at bootstrap 95%: 149 fact confidences, ECE 0.0219, 95th percentile 0.0246 |
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
| entity | 60.24% | 83 | saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True), saleor InvoiceEvent (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 52.87% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Calibration of model confidence

149 fact confidences checked against golden facts: ECE 0.0219 (bootstrap 95th percentile 0.0246). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 149 | 0.978 | 1.0 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.922 | 1.0 |
| datastore | 20 | 0.982 | 1.0 |
| entity | 47 | 0.989 | 1.0 |
| framework | 13 | 0.976 | 1.0 |
| license | 6 | 0.99 | 1.0 |
| route | 46 | 0.978 | 1.0 |
| runtime_version | 8 | 0.963 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.922 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.94 | 0.85 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.756 | 0.68 | 0.84 | 0 |
| P3 A2 boundaries | 52 | 0.95 | 0.85 | 0.99 | 0 |
| P4 A3 task estimates | 51 | 0.853 | 0.77 | 0.95 | 0 |

## Variation with evidence

- P2 dispositions: {'Replatform': 2, 'Retain': 3, 'Refactor': 4, 'Retire': 1}
- P3 decomposition: 6 distinct boundary sets across 6 apps
